from importlib.util import source_from_cache
from socket import create_server

from src.hetionetDBInteraction import hetionetDBInteraction
from neo4j import GraphDatabase, Driver, Session, ManagedTransaction
from dotenv import load_dotenv
from src.parse_data import get_data_from_file, DATA_FILE_LOCATIONS
from src.constants import EDGE_RELATIONS
import src.neoTransactions as neoTransactions
import os
load_dotenv()
HOST = os.getenv('NEO_HOST', "bolt://localhost")
PORT = int(os.getenv('NEO_PORT', 7687))
USERNAME = os.getenv('NEO_USER', "neo4j")
PASSWORD = os.getenv('NEO_PASSWORD', "your_password")
DB_NAME = os.getenv('DB_NAME', "neo4j")  # default db name in Community edition
DEBUG = bool(os.getenv('DEBUG', '0') == "1")
URI = f"{HOST}:{PORT}"


class Neo4jInteraction(hetionetDBInteraction):
    def db_conn_service(self) -> Driver:
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
        _driver: Driver = self.db_conn_service()
        # db cannot be created in Community Edition
        # _driver:Driver = self.db_conn_service(database_="system")
        # records, summary, keys= _driver.execute_query(
        #     f"CREATE DATABASE {DB_NAME} IF NOT EXISTS")
        # if DEBUG:
        #     print(records, summary, keys)
        self.populate_nodes(_driver)
        self.populate_edges(_driver)
        _driver.close()
        if DEBUG:
            print("populated db")

    def get_all_diseases(self):
        try:
            _driver = self.db_conn_service()
            session: Session = _driver.session(database=DB_NAME)
            res = session.execute_read(neoTransactions.get_all_diseases)
            session.close()
            _driver.close()
        except Exception as e:
            print(e)
            res=[]
        finally:
            print("get_all_diseases completed")
        return res
    def get_disease_by_id(self, disease_id) -> dict:
        """
        Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease, and where this disease occurs? Obtain and output this information in a single query.
        """
        try:
            _driver = self.db_conn_service()
            session: Session = _driver.session(database=DB_NAME)
            res = session.execute_read(neoTransactions.get_disease_by_id,disease_id)
            session.close()
            _driver.close()
        except Exception as e:
            print(e)
            res={}
        finally:
            print("get_all_diseases completed")
        return res

    def get_disease_drug_interactions_by_id(self, disease_id):
        """
        We assume that a compound can treat a disease if the compound up-regulates/down-regulates a gene, but the location down-regulates/up-regulates the gene in an opposite direction where the disease occurs. Find all compounds that can treat a new disease (i.e. the missing edges between compound and disease excluding existing drugs). Obtain and output all drugs in a single query.
        """
        try:
            _driver = self.db_conn_service()
            session: Session = _driver.session(database=DB_NAME)
            res = session.execute_read(neoTransactions.get_disease_drug_interactions_by_id,disease_id)
            session.close()
            _driver.close()
        except Exception as e:
            print(e)
            res={}
        finally:
            print("get_all_diseases completed")
        return res
        # pass

    def populate_nodes(self, driver: Driver = None):
        try:
            node_header, node_data = get_data_from_file(
                DATA_FILE_LOCATIONS.node)
            if DEBUG:
                print(node_header)
            _driver = None
            if not driver:
                _driver = self.db_conn_service()
                session: Session = _driver.session(database=DB_NAME)
            else:
                session: Session = driver.session(database=DB_NAME)
            session.execute_write(neoTransactions.create_node_batch_tx, node_data)
            # for node in node_data:
            #     session.execute_write(
            #         create_node_tx, id=node[0], name=node[1], kind=node[2])
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

    def populate_edges(self, driver: Driver = None):
        try:
            node_header, node_data = get_data_from_file(
                DATA_FILE_LOCATIONS.edge)
            if DEBUG:
                print(node_header)
            _driver = None
            if not driver:
                _driver = self.db_conn_service()
                session: Session = _driver.session(database=DB_NAME)
            else:
                session: Session = driver.session(database=DB_NAME)
            session.execute_write(neoTransactions.create_edge_batch_tx, node_data)

            # for node in node_data:
            #     session.execute_write(
            #         create_edge_tx, node[0], node[1], node[2])
            session.close()
            if _driver:
                _driver.close()
        except Exception as e:
            print(f"edge err: {e}")

    def erase_db(self):
        driver: Driver = self.db_conn_service()
        # session: Session = driver.session(database=DB_NAME)
        # drop all nodes
        del_query = """
        MATCH (n)
        DETACH DELETE n
        """
        records, summary, keys = driver.execute_query(
            del_query, database_=DB_NAME)
        # get all constrains
        print("node removal:", records, summary, keys)
        result = driver.execute_query(
            "SHOW CONSTRAINTS YIELD name",
            database_=DB_NAME
        )
        print("get constraints:", result)
        constraint_names = [record["name"] for record in result.records]
        # drop all constrains
        for name in constraint_names:
            driver.execute_query(
                f"DROP CONSTRAINT {name} IF EXISTS",
                database_=DB_NAME
            )
            print(f"Dropped constraint: {name}")

        # session.close()
        driver.close()

    def check_counts(self):
        driver = self.db_conn_service()
        query = """
        RETURN 
            COUNT { MATCH (n) } AS total_nodes, 
            COUNT { MATCH ()-[]->() } AS total_relationships
        """
        records, summary, keys = driver.execute_query(query, database_=DB_NAME)
        print(records, summary, keys)
        print(records)
        # print(f"nodeCount: {records[0].nodeCount}")
        # print(f"relCount: {records[0].relCount}")
        # record = result.records[0]
        # print(f"Nodes: {record['nodeCount']}")
        # print(f"Relationships: {record['relCount']}")

