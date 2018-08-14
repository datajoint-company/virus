import datajoint as dj

schema = dj.schema('virus')

@schema
class ConstructSource(dj.Lookup):
    # source of the construct
    definition = """
    construct_source : varchar(64) # source of the construct
    """
    contents = [['Addgene'], ['Custom']]

@schema
class Construct(dj.Manual):
    # a construct containing multiple genetic elements
    definition = """
    construct_nickname:     varchar(255)    # nickname of the construct
    ---
    construct_fullname:     varchar(255)    # full name of the construct 
    -> ConstructSource
    construct_notes = null: varchar(255)    # notes about the construct
    """

@schema
class GeneticElementType(dj.Lookup):
    definition = """
    genetic_element_type : varchar(64)  # type of the genetic element 
    """
    contents = [
        ['Promoter'],
        ['Recombinase or activator'],
        ['Conditional element'],
        ['Optogenetics'],
        ['DREADDS'],
        ['Calcium indicator'],
        ['Voltage indicator'],
        ['Fluorescent protein'],
        ['Other']
    ]

@schema
class GeneticElement(dj.Lookup):
    # list of gene elements
    definition = """
    genetic_element_name:           varchar(32)    # name of the genetic element, such as GFP 
    ---
    genetic_element_fullname:       varchar(256)   # full name of a genetic element, such as green fluorescent protein
    -> GeneticElementType
    function_description = null:    varchar(1024)  # description of the function of the gene
    genetic_element_source = null:  varchar(256)   # source of the genetic element
    """

@schema
class ConstructGeneticElement(dj.Manual):
    # membership table of Construct and GeneElement
    definition = """
    -> Construct
    -> GeneticElement
    """

@schema
class VirusType(dj.Lookup):
    # type of virus
    definition = """
    virus_type:                     varchar(32)               # type of virus
    ---
    virus_type_full_name:           varchar(64)               # full name of a virus type
    virus_type_description = null:  varchar(256)              # description of the virus type
    virus_bsl:                      enum('1', '2', '3', '4')  # biosafety level of the virus type
    """
    contents = [
        ['AAV', 'Adeno-associated virus', '', '1'],
        ['Rabies', 'Glycoprotein deleted Rabies virus', '', '2'],
        ['HSV', 'Herpes Simplex virus', '', '2'],
        ['Lenti', 'Lentivirus', '', '2']
    ]

@schema
class Serotype(dj.Lookup):
    # serotype of the virus
    definition = """
    serotype : varchar(32)   # serotype
    ---
    serotype_description = null : varchar(256)  # description of serotype
    """
    contents = [
        ['AAV2/1', ''],
        ['AAV2', ''],
        ['AAV2/3', ''],
        ['AAV2/4', ''],
        ['AAV2/5', ''],
        ['AAV2/6', ''],
        ['AAV2/8', ''], 
        ['AAV2/7', ''],
        ['AAV2/9', ''],
        ['AAV-DJ', 'Hybid capsid from 8 AAV serotypes, high infection rate across a broad range of cells and tissues.'],
        ['AAV-DJ8', 'A mutant of AAV-DJ that exhibits increased uptake in brain tissues in vivo.'],
        ['AAV2-Retro', 'Retrograde tracing AAV'],
        ['Standard Rabies', 'G deleted rabies, unpseudotyped'],
        ['EnvA Rabies', 'G deleted rabies pseudotyped with EnvA'],
        ['EnvB Rabies', 'G deleted rabies pseudotyped with EnvB'],
        ['HSV-1', ''],
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
    virus_id:               int          # virus identifier
    ---
    virus_name:             varchar(256) # nickname of the virus
    -> Construct
    -> VirusType
    -> Serotype
    -> VirusSource
    virus_catalog = null:   varchar(64)  # catalog number of the virus
    virus_lot = null:       varchar(64)  # lot number of the virus
    virus_volume = null:    smallint     # volume of the virus, in uL
    virus_titer = null:     varchar(64)  # titer of the virus
    virus_date = null:      date         # date the virus made
    virus_notes = null:     varchar(256) # notes
    """

@schema
class Aliquoting(dj.Manual):
    # information of aliquot
    definition = """
    -> Virus
    aliquoting_date:            date            # date when the aliquoting was performed
    ---
    aliquoting_person:          varchar(64)     # person that aliquoted the virus
    amount_per_aliquot:         smallint        # in uL
    aliquoting_number:          smallint        # number of aliquots
    aliquoting_notes = null:    varchar(256)    # notes
    """

@schema
class Aliquot(dj.Manual):
    definition = """
    -> Aliquoting
    aliquot_idx:                smallint         # idx of this aliquot
    ---
    aliquot_thaw_date = null:   date             # date the aliquot is thawed
    aliquot_notes = null:       varchar(256)     # notes
    """ 