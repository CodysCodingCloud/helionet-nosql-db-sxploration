# info on the type of data retrieved when parsing
class NODE_LABELS:
    anatomy='Anatomy'
    disease='Disease'
    compound='Compound'
    gene='Gene'
# meta edge relations
class EDGE_RELATIONS:
    CuG='CuG' # Compound upregulates Gene
    DuG='DuG' # Disease upregulates Gene
    DaG='DaG' # Disease associates with Gene
    CrC='CrC' # Compound resembles Compound
    DdG='DdG' # Disease downregulates Gene
    DrD='DrD' # Disease resembles Disease
    GcG='GcG' # Gene covaries with Gene
    AdG='AdG' # Anatomy downregulates Gene
    DlA='DlA' # Disease localizes to Anatomy
    CbG='CbG' # Compound binds to Gene
    GrG='Gr>G' # Gene regulates Gene (directional)
    CpD='CpD' # Compound palliates Disease
    AuG='AuG' # Anatomy upregulates Gene
    AeG='AeG' # Anatomy expresses Gene
    CtD='CtD' # Compound treats Disease
    CdG='CdG' # Compound downregulates Gene
    GiG='GiG' # Gene interacts with Gene
