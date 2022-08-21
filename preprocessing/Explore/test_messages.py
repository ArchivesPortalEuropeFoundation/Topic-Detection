import pandas as pd
import requests
from pandarallel import pandarallel

# import swifter

pandarallel.initialize()


def query_tool(lang, q_type, text, n_res, broad_entity_search, boolean_search):
    r = requests.get(
        "http://0.0.0.0:5000/query?lang="
        + lang
        + "&type="
        + q_type
        + "&text="
        + text
        + "&n_res="
        + n_res
        + "&broad_entity_search="
        + broad_entity_search
        + "&boolean_search="
        + boolean_search
    )
    return r.content


QUERY_PATH = "tests/test_data/20220211_ATDWorkshop_LogResults.tsv"
df = pd.read_csv(QUERY_PATH, sep="\t")
df = df.drop("Time of query (in UTC)", 1)
df = df.drop_duplicates(keep=False, inplace=False)
print(len(df))
# df = df[:100]
df["status"] = df.parallel_apply(
    lambda row: query_tool(
        lang=row["Language of search term"],
        q_type=row["Type of search"],
        text=row["Query text"],
        n_res=str(row["No of results"]),
        broad_entity_search=row["broad entity search"],
        boolean_search=row["boolean search"],
    ),
    axis=1,
)

out_df = pd.DataFrame()

for idx, row in df.iterrows():
    if (
        "<table" in str(row["status"][:6])
cd ..        #        or "Mentions" in str(row["status"])
        or "We have found results for the entity" in str(row["status"])
    ):
        continue
    out_df = out_df.append(row)

print(len(df), len(out_df), len(df) / len(out_df))
out_df.to_csv("tests/test_log/missing_queries.tsv", sep="\t")
