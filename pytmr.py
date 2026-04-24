import time
import sys
from src.SparkAggregator import SparkAggregator
from src.parse_data import create_data_subset
# from src.Neo4jInteraction import Neo4jInteraction

if len(sys.argv) > 1:
    STEP = int(sys.argv[1])
else:
    STEP = 1


def main():
    s = SparkAggregator()
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
    match(STEP):
        case 0:
            create_data_subset(DEBUG=True)
        case _:
            start = time.time()
            main()
            end = time.time()
            print("diff: ", end-start)

# python -c "from pyspark.sql import SparkSession; SparkSession.builder.remote('sc://localhost:15002').getOrCreate().range(10).show()"

# q1_ans = [('Compound::DB08865', (585, 1)),
#           ('Compound::DB01254', (564, 1)),
#           ('Compound::DB00997', (532, 17)),
#           ('Compound::DB00570', (523, 7)),
#           ('Compound::DB00390', (522, 2))]
# q2_ans = [(1, 10), (2, 7), (11, 6), (9, 6), (3, 6)]
# q3_ans = [('Compound::DB08865', (585, 'Crizotinib')),
#           ('Compound::DB01254', (564, 'Dasatinib')),
#           ('Compound::DB00997', (532, 'Doxorubicin')),
#           ('Compound::DB00570', (523, 'Vinblastine')),
#           ('Compound::DB00390', (522, 'Digoxin'))]


# q1 = [
#     ('DB08865', (585, 1)),
#     ('DB01254', (564, 1)),
#     ('DB00997', (532, 17)),
#     ('DB00570', (523, 7)),
#     ('DB00390', (522, 2))]
# q2 = [(1, 10), (2, 7), (9, 6), (11, 6), (3, 6)]
# q3 = [
#     ('DB08865', (585, 'Crizotinib')),
#     ('DB01254', (564, 'Dasatinib')),
#     ('DB00997', (532, 'Doxorubicin')),
#     ('DB00570', (523, 'Vinblastine')),
#     ('DB00390', (522, 'Digoxin'))]
# diff:  8.148232221603394
