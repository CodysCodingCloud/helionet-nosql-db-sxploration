import sys
import os
from dotenv import load_dotenv
from src.Neo4jInteraction import Neo4jInteraction
from src.RedisInteraction import RedisInteraction
from src.parse_data import DATA_FILE_LOCATIONS

dd = os.getenv('DEBUG', '0')
print(dd)
option = 0
if len(sys.argv) > 1:
    option = int(sys.argv[1])
# default id or retrieve from arguments
disease_id = "DOID:0050742"
if len(sys.argv) > 2:
    disease_id = sys.argv[2]
data = "nodata retrieved"
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
    case 4:
        inst = Neo4jInteraction()
        inst.populate_db()
    case 5:
        inst = Neo4jInteraction()
        inst.check_counts()
    case 7:
        import src.GUI as gui
        gui.root.mainloop()
    case 11:
        inst = Neo4jInteraction()
        data = inst.get_all_diseases()
    case 12:
        inst = Neo4jInteraction()
        data = inst.get_disease_by_id(disease_id)
    case 13:
        inst = Neo4jInteraction()
        data = inst.get_disease_drug_interactions_by_id(disease_id)
    case 14:
        inst = Neo4jInteraction()
        data = inst.get_all_diseases()
        for d in data:
            data = inst.get_disease_drug_interactions_by_id(d['id'])
            print(data)
    case 21:
        inst = RedisInteraction()
        # data = inst.db_conn_service()
    case 24:
        inst = RedisInteraction()
        nodes_path = DATA_FILE_LOCATIONS.node
        edges_path = DATA_FILE_LOCATIONS.edge
        data = inst.load_hetionet_to_redis(nodes_path,edges_path)
    case 27:
        inst = RedisInteraction()
        data = inst.get_disease_by_id(disease_id)
    case 666:
        inst = Neo4jInteraction()
        inst.erase_db()
print(data)
