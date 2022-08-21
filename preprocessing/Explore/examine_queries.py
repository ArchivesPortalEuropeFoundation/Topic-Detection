import pandas as pd

QUERY_PATH = "test_log/missing_queries.tsv"
df = pd.read_csv(QUERY_PATH, sep="\t")

query_types = {"Mentions": [], "Concept": []}

for idx, row in df.iterrows():
    if "Concept " in row["status"]:
        query_types["Concept"].append(row)
    elif "Mentions of " in row["status"]:
        query_types["Mentions"].append(row)
    else:
        print(row["status"])
# for q_type, queries in query_types.items():
# print(q_type)
# for query in queries:
#    print(query)
# print(" ")
import os

# Add "../" to path to import utils
import sys

sys.path.insert(0, os.path.abspath(os.path.pardir))

from utils import nlp

res = nlp.get_candidates("Churchill", "en", "en", False)
print(res)
