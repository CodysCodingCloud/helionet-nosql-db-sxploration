# info on the type of data retrieved when parsing the hetionet tsv files

# Nodes
# ['id', 'name', 'kind']
# ['Anatomy::UBERON:0000011', 'parasympathetic nervous system', 'Anatomy']
# id is composed of {kind}::{unique_id}
class NODE_LABELS:
    # options for kind
    anatomy = 'Anatomy'
    disease = 'Disease'
    compound = 'Compound'
    gene = 'Gene'


# Edges
# ['source', 'metaedge', 'target']
# ['Gene::2099', 'GiG', 'Gene::6206']
# source and target format = {kind}::{unique_id}
class EDGE_RELATIONS:
    # options for meta_edge
    CuG = 'CuG'  # Compound upregulates Gene
    DuG = 'DuG'  # Disease upregulates Gene
    DaG = 'DaG'  # Disease associates with Gene
    CrC = 'CrC'  # Compound resembles Compound
    DdG = 'DdG'  # Disease downregulates Gene
    DrD = 'DrD'  # Disease resembles Disease
    GcG = 'GcG'  # Gene covaries with Gene
    AdG = 'AdG'  # Anatomy downregulates Gene
    DlA = 'DlA'  # Disease localizes to Anatomy
    CbG = 'CbG'  # Compound binds to Gene
    GrG = 'Gr>G'  # Gene regulates Gene (directional)
    CpD = 'CpD'  # Compound palliates Disease
    AuG = 'AuG'  # Anatomy upregulates Gene
    AeG = 'AeG'  # Anatomy expresses Gene
    CtD = 'CtD'  # Compound treats Disease
    CdG = 'CdG'  # Compound downregulates Gene
    GiG = 'GiG'  # Gene interacts with Gene


class DB_USAGE_TYPE_ENUMS:
    neo = 1
    redis = 2
    both = 3
