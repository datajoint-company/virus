import datajoint as dj

schema = dj.schema('virus', locals())

@schema
class ConstructSource(dj.Lookup):
    # source of the construct
    definition = """
    construct_source : varchar(64) # source of the construct
    """
    contents = [['Addgene'], ['Constomly made']]

@schema
class Construct(dj.Manual):
    # information of the construct
    definition = """
    construct_name : varchar(255)    # name of a construct
    ---
    -> ConstructSource
    construct_notes = null : varchar(255)   # notes of the construct
    """

@schema
class GeneElementType(dj.Lookup):
    # type of the gene element type
    definition = """
    type : varchar(64)  # type of the gene element
    """
    contents = [['promoter'], ['opsin'], ['calcium indicator'], ['voltage indicator'], ['reporter']]

@schema
class GeneElement(dj.Lookup):
    # list of gene elements
    definition = """
    gene_name : varchar(32)  # identifier of the gene
    ---
    -> GeneElementType
    function_description = null : varchar(1024)  # description of the function of the gene
    dna_source = null  : varchar(256)   # source of the DNA
    risk = "no known risk" : varchar(256)  # known risk to human beings
    """

@schema
class ConstructGene(dj.Manual):
    # membership table of Construct and GeneElement
    definition = """
    -> Construct
    -> GeneElement
    """

@schema
class VirusType(dj.Lookup):
    # type of virus
    definition = """
    virus_type : varchar(32)  # type of virus
    ---
    virus_type_description = null : varchar(256)  # description of the virus type
    """

@schema
class Serotype(dj.Lookup):
    # serotype of the virus
    definition = """
    serotype : varchar(32)   # serotype
    ---
    description = null : varchar(256)  # description of serotype
    """
    contents = [
        ['AAV2/1', ''],
        ['AAV2', ''], 
        ['AAV2/5', ''],
        ['AAV2/8', ''], 
        ['AAV2/9', ''],
        ['AAV-DJ', ''],
        ['Other', '']
    ]

@schema
class VirusSource(dj.Lookup):
    # list of the sources of virus
    definition = """
    virus_source: varchar(64)  # name of the virus source
    """
    contents = [['UPenn'], ['UNC'], ['MIT'], ['Stanford'], ['Addgene']]

@schema
class Virus(dj.Manual):
    # information of virus
    definition = """
    virus_name : varchar(256) # nickname of a virus
    ---
    -> Construct
    -> VirusType
    -> Serotype
    -> VirusSource
    virus_catlog = null :  varchar(64)  # catlog number of the virus
    virus_lot = null    :  varchar(64)  # lot number of the virus
    virus_titer = null  :  varchar(64)  # titer of the virus
    virus_date = null   :  date         # date the virus made
    virus_notes = null  :  varchar(256) # notes
    """