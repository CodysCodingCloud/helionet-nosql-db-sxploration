import sys
from src.Neo4jInteraction import Neo4jInteraction

option=0
if len(sys.argv)>1:
    option=int(sys.argv[1])

match option:
    case 1:
        inst = Neo4jInteraction()
        inst.populate_db()
    case 2:
        inst = Neo4jInteraction()
        inst.populate_nodes()
    case 3:
        inst = Neo4jInteraction()
        inst.populate_edges()