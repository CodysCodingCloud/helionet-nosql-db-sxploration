class hetionetDBInteraction:
    def db_conn_service():
        pass
    def populate_db():
        pass
    def get_all_diseases():
        pass
    def get_disease_by_id(disease_id)->dict:
        """
        Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease, and where this disease occurs? Obtain and output this information in a single query.
        """
        pass
    def get_disease_drug_interactions_by_id(disease_id):
        """
        We assume that a compound can treat a disease if the compound up-regulates/down-regulates a gene, but the location down-regulates/up-regulates the gene in an opposite direction where the disease occurs. Find all compounds that can treat a new disease (i.e. the missing edges between compound and disease excluding existing drugs). Obtain and output all drugs in a single query.
        """