import os
from neo4j import ManagedTransaction
from dotenv import load_dotenv

from src.constants import EDGE_RELATIONS
load_dotenv()
dd=os.getenv('DEBUG', '0')
print(dd)
DEBUG = bool(os.getenv('DEBUG', '0') == "1")
ALL_EDGES = bool(os.getenv('ALL_EDGES', '0') == "1")
required_edges = ['DuG','DdG','CdG','CuG','CtD']

def get_all_diseases(tx: ManagedTransaction):
    query = f"""
    MATCH (a:Disease)
    RETURN a
    """
    result = tx.run(query)
    if DEBUG:
        print(result)
    return result
def get_disease_by_id(tx: ManagedTransaction,disease_id):
    query = f"""
    MATCH (a:Disease id: $disease_id)
    RETURN a
    """
    result = tx.run(query,disease_id=disease_id)
    if DEBUG:
        print(result)
    return result
def get_disease_drug_interactions_by_id(tx: ManagedTransaction,disease_id):
    query = """
        MATCH (d:Disease {id: $disease_id})-[:DuG|DdG]-(:Gene)-[:DuG|DdG]-(c:Compound)
        WHERE (
        ((d)-[:DuG]->(:Gene)<-[CdG]-(c)) OR 
        ((d)-[:DdG]->(:Gene)<-[:CuG]-(c))
        )
        AND NOT (c)-[:CtD]->(d)
        RETURN DISTINCT c
    """
    result = tx.run(query)
    if DEBUG:
        print(result)
    return result

def add_constraints(tx: ManagedTransaction):
    query = """
    CREATE CONSTRAINT FOR (n:Gene) REQUIRE n.id IS UNIQUE;
    CREATE CONSTRAINT FOR (n:Compound) REQUIRE n.id IS UNIQUE;
    CREATE CONSTRAINT FOR (n:Disease) REQUIRE n.id IS UNIQUE;
    CREATE CONSTRAINT FOR (n:Anatomy) REQUIRE n.id IS UNIQUE;
    """
    tx.run(query)


def create_node_batch_dict(data) -> dict:
    node_dict = {}
    for row in data:
        id = row[0].split("::")[1]
        name = row[1]
        kind = row[2]
        elem_value = {"id": id, "name": name}
        node_dict.setdefault(kind, [])
        node_dict[kind].append(elem_value)
    return node_dict


def create_node_batch_tx(tx: ManagedTransaction, data):
    batch_data = create_node_batch_dict(data)
    res = []
    for (kind), kind_node_data in batch_data.items():
        unwind_node_query = f"""
        UNWIND $rows AS row
        CREATE (a:{kind} {{id:row.id, name: row.name}})
        RETURN count(a) AS created_count
        """
        result = tx.run(unwind_node_query, rows=kind_node_data)
        if DEBUG:
            summary = result.consume()
            res.append((kind, len(kind_node_data), {
                       summary.counters.nodes_created}))
            print(kind, len(kind_node_data), {
                  summary.counters.nodes_created}, result)
    return res


def create_edge_batch_data(data) -> dict:
    try:
        edge_dict = {}
        count=0
        skipped=0
        for row in data:
            source = row[0]
            edge = row[1]
            target = row[2]
            [source_label, source_id] = source.split("::")
            [target_label, target_id] = target.split("::")
            if not ALL_EDGES:
                if edge not in required_edges:
                    skipped+=1
                    continue
            count+=1
            key = (source_label, target_label, edge)
            elem_value = {"src": source_id, "tgt": target_id}
            edge_dict.setdefault(key, [])
            edge_dict[key].append(elem_value)
        if DEBUG:
            print(f"num to add edges = {count}, skipped = {skipped}")
    except Exception as e:
        print(e)
        edge_dict = {}
    return edge_dict


def create_edge_batch_tx(tx: ManagedTransaction, data: dict):
    batch_data = create_edge_batch_data(data)
    for (src_label, tgt_label, rel_type), rel_data in batch_data.items():
        if DEBUG:
            print(src_label, rel_type, tgt_label, len(rel_data))
        match rel_type:
            case EDGE_RELATIONS.GrG:
                rel_dir = '>'
                rel_type = 'GrG'
                print(rel_type, rel_dir)
            case _:
                rel_dir = ""

        unwind_query = f"""
        UNWIND $rows AS row
        MATCH (s:{src_label} {{id: row.src}})
        MATCH (t:{tgt_label} {{id: row.tgt}})
        MERGE (s)-[r:{rel_type}]-{rel_dir}(t)
        """

        result = tx.run(unwind_query, rows=rel_data)
        if DEBUG:
            summary = result.consume()
            print(rel_type, summary, result)
    return

# OLD Version that do one query at a time


def create_node_tx(tx: ManagedTransaction, id: str, name, kind):
    id = id.split("::")[1]
    insert_query = f"""
    CREATE (a:{kind} {{id:$id, name: $name}})
    """
    result = tx.run(insert_query, id=id, name=name)
    if DEBUG:
        print(result)


def create_edge_tx(tx: ManagedTransaction, source: str, edge, target: str):
    # example data
    # Anatomy::UBERON:0000007	AuG	Gene::83480
    [source_label, source_id] = source.split("::")
    [target_label, target_id] = target.split("::")
    insert_query = f"""
    MATCH (s:{source_label} {{id: $source_id}})
    MATCH (t:{target_label}  {{id: $target_id}})
    MERGE (s)-[:{edge}]->(t)
    """
    result = tx.run(insert_query, source_id=source_id, target_id=target_id)
    if DEBUG:
        print(result)
