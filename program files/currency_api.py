import requests
import json
from dataclasses import dataclass

@dataclass
class Currency:
    symbol: str
    name: str
    conversion_rate: float


"""def test_get_currencies():
    with open('json files/symbol_test.json', 'r') as temp:
        currency_validation_dict = json.load(temp)
    
    return currency_validation_dict"""

def get_currencies():

    with open('json files/currency_validation_dict.json', 'r') as temp:
        currency_validation_dict = json.load(temp)

    url = "https://api.exchangerate.host/"
    arg = "symbols"

    r = requests.get(url+arg)
    print(f"Status code: {r.status_code}")
    if r.status_code == 200:
        invalid_currencies = r.json()
    else:
        print(f"Failed to retrieve data. Status code: {r.status_code}")

    valid_symbol_dict = {key: invalid_currencies["symbols"][key] for key in currency_validation_dict if key in invalid_currencies["symbols"]}
    return valid_symbol_dict

def get_currency_conversion(valid_symbol_dict):
    url = "https://api.exchangerate.host/"
    arg = "latest"

    r = requests.get(url+arg)
    print(f"Status code: {r.status_code}")
    if r.status_code == 200:
        invalid_conversion_dict = r.json()
    else:
        print(f"Failed to retrieve data. Status code: {r.status_code}")
        
    valid_conversion_dict = {currency: rate for currency, rate in invalid_conversion_dict['rates'].items() if currency in [v['code'] for v in valid_symbol_dict.values()]}

    return valid_conversion_dict
