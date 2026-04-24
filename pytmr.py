from src.SparkAggregator import SparkAggregator
# from src.Neo4jInteraction import Neo4jInteraction


def main():
    s = SparkAggregator()
    # s.read_data()
    q1 = s.get_drug_by_num_genes_with_num_diseases()
    q2 = s.get_disease_by_drugs()
    q3 = s.get_drug_by_genes()
    print("q1")
    print(q1)
    print("q2")
    print(q2)
    print("q3")
    print(q3)
    # s.check_file_exists()


if __name__ == "__main__":
    main()
# python -c "from pyspark.sql import SparkSession; SparkSession.builder.remote('sc://localhost:15002').getOrCreate().range(10).show()"

# q1_ans = [('Compound::DB08865', (585, 1)),
#           ('Compound::DB01254', (564, 1)),
#           ('Compound::DB00997', (532, 17)),
#           ('Compound::DB00570', (523, 7)),
#           ('Compound::DB00390', (522, 2))]
# q2_ans = [(1, 117), (3, 103), (2, 103), (5, 91), (4, 75)]
# q3_ans = [('Compound::DB08865', (585, 'Crizotinib')),
#           ('Compound::DB01254', (564, 'Dasatinib')),
#           ('Compound::DB00997', (532, 'Doxorubicin')),
#           ('Compound::DB00570', (523, 'Vinblastine')),
#           ('Compound::DB00390', (522, 'Digoxin'))]
