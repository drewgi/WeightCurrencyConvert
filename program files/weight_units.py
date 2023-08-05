import json
from dataclasses import dataclass

@dataclass
class Weight:
    unit: str
    name: str
    conversion_rate: float

def get_weight_units():

    with open('json files/units.json', 'r') as temp:
        weights_dict = json.load(temp)
        return weights_dict