import requests

def test_basic_query():

    lang = 'fr'
    type = 'concept'
    text = 'et'
    n_res = '10'
    broad_entity_search = 'False'
    boolean_search = 'False'

    r = requests.get('http://0.0.0.0:8091/query?lang='+lang+'&type='+type+'&text='+text+'&n_res='+n_res+'&broad_entity_search='+broad_entity_search+'&boolean_search='+boolean_search)
    assert r.status_code == 200
