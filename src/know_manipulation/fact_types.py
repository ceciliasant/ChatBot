FACT_TYPES = {
    "is in": ["where"],      #  Location-based
    "is a": ["who", "what"], #  Identity-based
    "is": ["what"],          #  Adjective-based
    "has": ["have"],         #  Possession-based
    "owns": ["own"],         #  Ownership
    "knows": ["know"],       #  Relationship
    "likes": ["like"],      #  Preference
    "works at": ["work"],    #  Employment
    "lives in": ["live"],    #  Residence
    "was born in": ["born"], # nascimento
    "created": ["create"],   #  Creation
    "studies at": ["study"], #  Studies
    "uses": ["use", "utilize"], # tool or resouce
    "speaks": ["speak", "talk", "communicate"], # Language
}

RELATION_KEYS = FACT_TYPES.keys()
RELATION_VALUES = set(value for values in FACT_TYPES.values() for value in values)

def get_relation_key(fact_type_value):

    rels = []

    for key, values in FACT_TYPES.items():
        if fact_type_value in values:
            rels.append(key)
    
    return rels