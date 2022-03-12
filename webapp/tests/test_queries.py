import datatetime
import git
import requests
import pandas as pd
from pandarallel import pandarallel
from tqdm.notebook import tqdm
from pathlib import Path

try:
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
except Exception:
    sha = str(datetime.datetime.now())

tqdm.pandas()
pandarallel.initialize()

def query_tool(lang,type,text,n_res,broad_entity_search,boolean_search):
    r = requests.get('http://0.0.0.0:5000/query?lang='+lang+'&type='+type+'&text='+text+'&n_res='+n_res+'&broad_entity_search='+broad_entity_search+'&boolean_search='+boolean_search)
    return r.status_code

def test_queries():
    df = pd.read_csv('tests/test_data/20220211_ATDWorkshop_LogResults_OverviewByType.tsv', sep='\t')
    df = df.drop('Time of query (in UTC)', 1)
    df = df.drop_duplicates(keep=False, inplace=False)
    df['status'] = df.parallel_apply(lambda row: query_tool(
                                                    lang=row['Language of search term'],
                                                    type=row["Type of search"],
                                                    text=row["Query text"],
                                                    n_res=str(row["No of results"]),
                                                    broad_entity_search=row['broad entity search'],
                                                    boolean_search=row['boolean search']
                                                    ), axis=1)

    errors = df[df['status']!=200]
    if not errors.empty:
        output_dir = Path('tests/test_log')
        output_dir.mkdir(parents=True, exist_ok=True)
        errors.to_csv(str(output_dir)+'/failedqueries_'+sha+'.tsv', sep='\t')

    assert all(status == 200 for status in df['status']) == True
