from src.hetionetDBInteraction import hetionetDBInteraction
import redis
from dotenv import load_dotenv
import os
import csv



class RedisInteraction(hetionetDBInteraction):
    def __init__(self):
        self.db_conn_service()
        
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
            
    # def populate_db(self, nodes_path, edge_path):
        
    #     with open(nodes_path, 'r') as f:
    #         data = csv.DictReader(f, delimiter ='\t')
    #         for row in data:
    #             node_id = row['id']
    #             self.r.hset(f"node:{node_id}", mapping=row)

    #     with open(edge_path, 'r') as f:
    #         data = csv.DictReader(f, delimiter = '\t')
    #         for row in data:
    #             source = row['source']
    #             rel = row['metaedge']
    #             target = row['target']
                
    #             self.r.sadd(f"links:{target}:{rel}", source)
    #             self.r.sadd(f"links:{source}:{rel}", target)


    # Mapping edges of interest to query about diseases
    DISEASE_EDGE_MAP = {
        "CtD": {"disease_end": "target", "field": "drugs"},      # Compound treats Disease
        "CpD": {"disease_end": "target", "field": "drugs"},      # Compound palliates Disease
        "DaG": {"disease_end": "source", "field": "genes"},      # Disease associates Gene
        "DlA": {"disease_end": "source", "field": "locations"},  # Disease localizes Anatomy
        "DuG": {"disease_end": "source", "field": "genes"},  # Disease upregulates Gene
        "DdG": {"disease_end": "source", "field": "genes"},  # Disease downregulates Gene
    }

    # redis will only be used to lookup information about diseases, a hash will be created per disease that connects the disease to all related nodes to allow for a single query using the disease id as the key
    def load_hetionet_to_redis(self, nodes_path, edges_path):
        
        nodes = {}
        with open(nodes_path) as f:
            for row in csv.DictReader(f, delimiter="\t"):
                nodes[row["id"]] = {"name": row["name"], "kind": row["kind"]}


        #data will be saved as follows
        disease_data = {}  # { "DOID:10652": {name, drugs:[], genes:[], locations:[]} }

        #parsing relevant edges to diseases
        with open(edges_path) as f:
            for row in csv.DictReader(f, delimiter="\t"):
                meta = row["metaedge"]
                if meta not in self.DISEASE_EDGE_MAP:
                    continue  

                cfg = self.DISEASE_EDGE_MAP[meta]

                # figure out disease position
                dicease_id_full = row[cfg["disease_end"]]   
                other_id        = row["target"] if cfg["disease_end"] == "source" else row["source"]

                
                disease_id = dicease_id_full.replace("Disease::", "")

                # create new instances if new disease
                if disease_id not in disease_data:
                    disease_data[disease_id] = {"drugs": [], "genes": [], "locations": []}

                # else append data to existing node
                if other_id in nodes:
                    disease_data[disease_id][cfg["field"]].append(nodes[other_id]["name"])

        # hash inserted data
        for disease_id, fields in disease_data.items():
            full_id = f"Disease::{disease_id}"
            self.r.hset(f"disease:{disease_id}", mapping={
                "name":      nodes.get(full_id, {}).get("name"),
                "drugs":     ",".join(set(fields["drugs"])),  
                "genes":     ",".join(set(fields["genes"])),
                "locations": ",".join(set(fields["locations"])),
            })




    def get_all_diseases(self):
        pass

    def get_disease_by_id(self, disease_id):
        """
        Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease, and where this disease occurs? Obtain and output this information in a single query.
        """

        data = self.r.hgetall(f"disease:{disease_id}")


        return {
            "id":        disease_id,
            "name":      data.get("name"),
            "drugs":     data.get("drugs", "").split(",") if data.get("drugs") else [],
            "genes":     data.get("genes", "").split(",") if data.get("genes") else [],
            "locations": data.get("locations", "").split(",") if data.get("locations") else [],
        }

