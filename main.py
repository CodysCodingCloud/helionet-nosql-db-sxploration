# test_redis.py
from RedisInteraction import RedisInteraction

# 1. Connect
db = RedisInteraction()
db.db_conn_service()

# 2. Load data
db.load_hetionet_to_redis("nodes.tsv", "edges.tsv")

# 3. Query a disease
result = db.get_disease_by_id("DOID:10652")
print(result)