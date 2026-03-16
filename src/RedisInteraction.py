from hetionetDBInteraction import hetionetDBInteraction
import redis
from dotenv import load_dotenv
import os
import csv



class RedisInteraction(hetionetDBInteraction):
    def db_conn_service(self):
        load_dotenv()

        self.r = redis.Redis(
            host = os.getenv('REDIS_HOST'),
            port = int(os.getenv('REDIS_PORT')),
            password = os.getenv('REDIS_PASSWORD'),
            decode_responses = True
        )

        response = self.r.ping()

        try:
            if response:
                print ("Success")
        except Exception as e:
            print(f"Something was down :( check it out: {e}" )
            
    def populate_db(self, nodes_path, edge_path):
        
        with open(nodes_path, 'r') as f:
            data = csv.DictReader(f, delimiter ='\t')
            for row in data:
                node_id = row['id']
                self.r.hset(f"node:{node_id}", mapping=row)

        with open(edge_path, 'r') as f:
            data = csv.DictReader(f, delimiter = '\t')
            for row in data:
                source = row['source']
                rel = row['metaedge']
                target = row['target']
                
                self.r.sadd(f"links:{target}:{rel}", source)
                self.r.sadd(f"links:{source}:{rel}", target)


    def get_all_diseases(self):
        pass
        
    def get_disease_by_id(self, disease_id):
        """
        Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease, and where this disease occurs? Obtain and output this information in a single query.
        """
        batch = self.r.pipeline()
        
        batch.hgetall(f"node: {disease_id}")

        batch.smembers(f"links: {disease_id}:CtD") 
        batch.smembers(f"links: {disease_id}:CpD")
        batch.smembers(f"links: {disease_id}:DaG")
        batch.smembers(f"links: {disease_id}:DlA")

        results = batch.execute()

        return {
                "disease_name": results[1].get("name"),
                "compounds that treat": list(results[1]),
                "compounds that palliate": list(results[2]),
                "associated genes": list(results[3]),
                "locations": list(results[4])
            }

        
