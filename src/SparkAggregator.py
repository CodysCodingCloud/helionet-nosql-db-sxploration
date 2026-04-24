import os

import sys
from dotenv import load_dotenv

from pyspark.sql import SparkSession, DataFrame
from operator import add
from src.constants import EDGE_RELATIONS
from src.Neo4jInteraction import Neo4jInteraction

load_dotenv()
DEBUG = os.getenv('DEBUG', '0')
DATA_RETRIEVAL = os.getenv('DATA_RETRIEVAL', 0) 
class DataRetrieval:
    tsv=0
    neo=1

# from src.parse_data import get_data_from_file, DATA_FILE_LOCATIONS
# edges_fp = DATA_FILE_LOCATIONS.edge
# edges_fp = "/opt/spark/data/edges.tsv"
nodes_fp = "nodes.tsv"
edges_fp = "edges_subset.tsv"
compound_gene_edges = [EDGE_RELATIONS.CuG,
                       EDGE_RELATIONS.CdG, EDGE_RELATIONS.CbG]
compound_disease_edges = [EDGE_RELATIONS.CpD,
                          EDGE_RELATIONS.CpD, EDGE_RELATIONS.CtD]


class SparkAggregator():
    spark: SparkSession = None
    df: DataFrame = None
    df_nodes: DataFrame = None

    def __init__(self):
        # spark = SparkSession.builder.appName("MapReduceBasics").getOrCreate()
        # spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
        spark = SparkSession.builder \
            .master("local[*]") \
            .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
            .getOrCreate()
        print(f"spark session created {spark}")
        self.spark = spark
        self.set_data()
    def set_data(self):
        match DATA_RETRIEVAL:
            case DataRetrieval.neo:
                self.get_neo_data()
            case DataRetrieval.tsv:
                self.read_tsv_data()
            case _:
                self.read_tsv_data()
        pass
    def get_neo_data(self):
        neo_inst = Neo4jInteraction()
        edge_data = neo_inst.get_compound_gd_edges(compound_disease_edges+compound_gene_edges)
        disease_data = neo_inst.get_disease_list(compound_disease_edges+compound_gene_edges)
        spark = self.spark
        self.df=spark.createDataFrame(edge_data)
        self.df_nodes=spark.createDataFrame(disease_data)
    def read_tsv_data(self):
        # Standard way to read a TSV
        print(f"reading {edges_fp}")
        spark = self.spark
        df = spark.read.csv(edges_fp,
                            sep="\t", header=True, inferSchema=False)
        df_nodes = spark.read.csv(nodes_fp,
                                  sep="\t", header=True, inferSchema=False)
        # print(f"df created")
        # df.show(5)
        self.df = df
        self.df_nodes = df_nodes
        # print(f"done reading")

        # print(df[0:5])
    def check_file_exists(self):
        try:
            # Try to read just the header/first line
            self.spark.read.text(edges_fp).limit(1).collect()
            print(f"Success: Cluster can see {edges_fp}")
            return True
        except Exception as e:
            print(f"Error: Cluster cannot access file at {edges_fp}")
            print(f"Details: {e}")
            return False

    def get_drug_by_num_genes_with_num_diseases(self, top=5):
        """
        For each drug, compute the number of genes and the number of diseases associated with the drug. Output results with top 5 number of genes in a descending order.
        """
        rdd = self.df.rdd
        # 3. The MAP Phase
        # We take each row and emit a tuple: (metaedge_name, 1)

        def rdd_map(row):
            metaedge_type = row["metaedge"]
            gene_num = 1 if metaedge_type in compound_gene_edges else 0
            disease_num = 1-gene_num
            row = (row["source"], (gene_num, disease_num))
            return row

        def rdd_reducer(a, b):
            return (a[0] + b[0], a[1] + b[1])

        def rdd_sort(rdd):
            return rdd[1][0]

        mapped_rdd = rdd.map(rdd_map)

        # The REDUCE Phase
        # We group by the key and sum (gene, diseases)
        counts_rdd = mapped_rdd.reduceByKey(rdd_reducer)

        # sort results back to Python
        # sorted_results = counts_rdd.sortBy(lambda x: x[1][0], ascending=False)
        sorted_results = counts_rdd.sortBy(rdd_sort, ascending=False)

        top_res = []
        count = 0
        for item in sorted_results.collect():
            if count < top:
                count += 1
                top_res.append(item)
            else:
                break
        return top_res

    def get_disease_by_drugs(self, top=5):
        """
        Compute the number of diseases associated with 1, 2, 3, …, n drugs. Output results with the top 5 number of diseases in a descending order.
        """
        rdd = self.df.rdd

        def rdd_map(row):
            row = (row["target"], 1)
            return row

        def rdd_sort(rdd):
            return rdd[1]

        filtered_rdd = rdd.filter(
            lambda row: row["metaedge"] in compound_gene_edges)
        mapped_rdd = filtered_rdd.map(lambda row: (row["source"], 1))
        counts_rdd = mapped_rdd.reduceByKey(lambda a, b: a+b)
        reversed_rdd = counts_rdd.map(lambda x: (x[1], 1))
        counted_by_frequency = reversed_rdd.reduceByKey(lambda a, b: a+b)
        sorted_results = counted_by_frequency.sortBy(
            lambda rdd: rdd[1], ascending=False)
        print(">>>>>>. sorted_results")
        # print(sorted_results)

        top_res = []
        count = 0
        for item in sorted_results.collect():
            if count < top:
                count += 1
                top_res.append(item)
            else:
                break
        return top_res

    def get_drug_by_genes(self, top=5):
        """
        Get the name of drugs that have the top 5 number of genes. Out put the results.
        """
        # the data
        rdd = self.df.rdd
        rdd_nodes = self.df_nodes.rdd

        # the computation
        filtered_rdd = rdd.filter(
            lambda row: row["metaedge"] in compound_gene_edges)
        mapped_rdd = filtered_rdd.map(lambda row: (row["source"], 1))
        counts_rdd = mapped_rdd.reduceByKey(lambda a, b: a+b)

        rdd_nodes_mapped = rdd_nodes.filter(lambda row: row["kind"] == "Compound").map(
            lambda row: (row["id"], row["name"]))

        joined_rdd = counts_rdd.join(rdd_nodes_mapped)
        sorted_results = joined_rdd.sortBy(
            lambda rdd: rdd[1][0], ascending=False)

        top_res = []
        count = 0
        for item in sorted_results.collect():
            if count < top:
                count += 1
                top_res.append(item)
            else:
                break
        return top_res
