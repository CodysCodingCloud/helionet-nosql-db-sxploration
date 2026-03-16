from src.hetionetDBInteraction import hetionetDBInteraction
from neo4j import GraphDatabase, Driver, Session, ManagedTransaction
from dotenv import load_dotenv
from src.parse_data import get_data_from_file, DATA_FILE_LOCATIONS
import os
load_dotenv()
HOST = os.getenv('NEO_HOST', "bolt://localhost")
PORT = int(os.getenv('NEO_PORT', 7687))
USERNAME = os.getenv('NEO_USER', "neo4j")
PASSWORD = os.getenv('NEO_PASSWORD', "your_password")
DB_NAME = os.getenv('DB_NAME', "hetionet")
DEBUG = bool(os.getenv('DEBUG', '0')=="1")
URI = f"{HOST}:{PORT}"


class Neo4jInteraction(hetionetDBInteraction):
    def db_conn_service() -> Driver:
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        # Optional: Verify connectivity
        driver.verify_connectivity()
        print("Connection successful!")
        return driver
        # session = driver.session(database=DATABASE_NAME)
        # return session

    def test_db(self):
        pass
    def populate_db(self):
        self.populate_nodes()
    def get_all_diseases(self):
        pass

    def get_disease_by_id(self, disease_id) -> dict:
        """
        Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease, and where this disease occurs? Obtain and output this information in a single query.
        """
        pass

    def get_disease_drug_interactions_by_id(self, disease_id):
        """
        We assume that a compound can treat a disease if the compound up-regulates/down-regulates a gene, but the location down-regulates/up-regulates the gene in an opposite direction where the disease occurs. Find all compounds that can treat a new disease (i.e. the missing edges between compound and disease excluding existing drugs). Obtain and output all drugs in a single query.
        """
        pass
    
    def populate_nodes(self, driver:Driver):
        try:
            node_header, node_data = get_data_from_file(DATA_FILE_LOCATIONS.node)
            if DEBUG:
                print(node_header)
            _driver=None
            if not driver:
                _driver = self.db_conn_service()
                session:Session = _driver.session(database_=DB_NAME)
            else:
                session:Session = driver.session(database_=DB_NAME)
            for node in node_data:
                session.execute_write(create_node_tx, id=node[0], name=node[1], kind=node[2])
                # records, summary, keys = session.execute_query(insert_query,
                #                                             id=node[0], name=node[1]
                #                                             )
            session.close()
            if _driver:
                _driver.close()
        except Exception as e:
            print(e)
        finally:
            print("populate_nodes completed")
    def populate_edges(self, driver:Driver):
        try:
            node_header, node_data = get_data_from_file(DATA_FILE_LOCATIONS.edge)
            if DEBUG:
                print(node_header)
            _driver=None
            if not driver:
                _driver = self.db_conn_service()
                session:Session = _driver.session(database_=DB_NAME)
            else:
                session:Session = driver.session(database_=DB_NAME)
            for node in node_data:
                insert_query = f"""
                MERGE (a:{node[2]} {{id:$id, name: $name}})
                """
                records, summary, keys = session.execute_query(insert_query,
                                                            id=node[0], name=node[1], kind=node[2],
                                                            )
            session.close()
            if _driver:
                _driver.close()
        except Exception as e:
            print(e)
    def erase_db(self):
        driver:Driver = self.db_conn_service()
        session:Session = driver.session(database_=DB_NAME)
        # drop all nodes
        del_query = """
        DROP CONSTRAINT
        MATCH (n)
        DETACH DELETE n
        """
        records, summary, keys = session.execute_query(del_query)
        # get all constrains
        result = session.execute_query(
            "SHOW CONSTRAINTS YIELD name",
            database_=DB_NAME
        )
        constraint_names = [record["name"] for record in result.records]
        # drop all constrains
        for name in constraint_names:
            driver.execute_query(
                f"DROP CONSTRAINT {name}",
                database_=DB_NAME
            )
            print(f"Dropped constraint: {name}")
        
        session.close()
        driver.close()

def add_constraints(tx:ManagedTransaction):
    query="""
    CREATE CONSTRAINT FOR (n:Gene) REQUIRE n.id IS UNIQUE;
    CREATE CONSTRAINT FOR (n:Compound) REQUIRE n.id IS UNIQUE;
    CREATE CONSTRAINT FOR (n:Disease) REQUIRE n.id IS UNIQUE;
    CREATE CONSTRAINT FOR (n:Anatomy) REQUIRE n.id IS UNIQUE;
    """
    tx.run(query)
def create_node_tx(tx:ManagedTransaction,id:str,name,kind):
    id=id.split("::")[1]
    insert_query = f"""
    CREATE (a:{kind} {{id:$id, name: $name}})
    """
    result = tx.run(insert_query, id=id, name=name)
    if DEBUG:
        print(result)
def create_edge_tx(tx:ManagedTransaction,source:str, edge,target:str):
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