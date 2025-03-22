FACT_TYPES = {
    "is in": ["where"],         #  Location-based
    "is a": ["who", "what"],    #  Identity-based
    "has": ["have"],            #  Possession-based
    "owns": ["own"],           #  Ownership
    "knows": ["know"],           #  Relationship
    "likes": ["likes"],   #  Preference
    "works at": ["work"],      #  Employment
    "lives in": ["live"],      #  Residence
    "created": ["create"],        #  Creation
    "studies at": ["study"],    #  Studies
}

RELATION_KEYS = FACT_TYPES.keys()
RELATION_VALUES = set(value for values in FACT_TYPES.values() for value in values)

def get_relation_key(fact_type_value):
    for key, values in FACT_TYPES.items():
        if fact_type_value in values:
            return key
    return None