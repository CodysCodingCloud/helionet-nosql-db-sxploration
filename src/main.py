from RedisInteraction import RedisInteraction
if __name__ == "__main__":

    db = RedisInteraction()
    

    db.db_conn_service()
    
    node_file = "nodes.tsv"
    edge_file = "edges.tsv"
    
    print("Starting data injection...")
    

    db.populate_db(node_file, edge_file)
    
    print("Complete!")
    
