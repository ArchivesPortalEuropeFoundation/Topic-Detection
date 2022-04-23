import requests
from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read("config/config.env")

backend = parser.get("default", "URI_API_BACKEND")

def test_basic_query():

    lang = 'fr'
    type = 'concept'
    text = 'et'
    n_res = '10'
    broad_entity_search = 'False'
    boolean_search = 'False'

    r = requests.get(backend+'/query?lang='+lang+'&type='+type+'&text='+text+'&n_res='+n_res+'&broad_entity_search='+broad_entity_search+'&boolean_search='+boolean_search)
    assert r.status_code == 200
