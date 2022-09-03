# %%

import os, json,pickle
import pandas as pd
from langdetect import detect
from collections import Counter

# in data you will store the topic related json files
path = 'exportedJsons/'

# "langMaterial","unitTitle","titleProper","scopeContent","topic",

aggregating_fields = ['langMaterial','parentId', 'unitId', 'otherUnitId', 'duplicateUnitId', 'scopeContent', 'spell', 'unitTitle', 'levelName', 'startDate', 'endDate', 'alternateUnitdate', 'dateType', 'country', 'repositoryCode', 'ai', 'recordId', 'dao', 'numberOfDao', 'numberOfDaoBelow', 'numberOfDescendents', 'numberOfAncestors', 'daoType', 'other', 'titleProper', 'recordType', 'topic', 'F0_s', 'FID0_s', 'F1_s', 'FID1_s', 'F2_s', 'FID2_s', 'F3_s', 'FID3_s', 'F4_s', 'FID4_s', 'AID2_s', 'AID1_s', 'AID0_s', 'A1_s', 'A2_s', 'A0_s', 'orderId', 'openData', 'timestamp']

dataset = [['id', 'langMaterial','parentId', 'unitId', 'otherUnitId', 'duplicateUnitId', 'scopeContent', 'spell', 'unitTitle', 'levelName', 'startDate', 'endDate', 'alternateUnitdate', 'dateType', 'country', 'repositoryCode', 'ai', 'recordId', 'dao', 'numberOfDao', 'numberOfDaoBelow', 'numberOfDescendents', 'numberOfAncestors', 'daoType', 'other', 'titleProper', 'recordType', 'topic', 'F0_s', 'FID0_s', 'F1_s', 'FID1_s', 'F2_s', 'FID2_s', 'F3_s', 'FID3_s', 'F4_s', 'FID4_s', 'AID2_s', 'AID1_s', 'AID0_s', 'A1_s', 'A2_s', 'A0_s', 'orderId', 'openData', 'timestamp',"filename"]]

for filename in [x for x in os.listdir(path) if x.endswith(".json")]:
    
    with open(path+filename) as json_file:
        data = json.load(json_file)
    
    for i in range(len(data["response"]["docs"])):
        element = data["response"]["docs"][i]
        
        line = [element["id"]]
        for field in aggregating_fields:
            if field in element:
                line.append(element[field])
            else:
                line.append(" ")
        line.append(filename)
        dataset.append(line)
print ("we have loaded",len(dataset),"entries")

# %%
print (dataset[0][6],dataset[0][8],dataset[0][25])
# we remove al columns that do not contain text (where we have less than 3 chars)
selected_dataset = [dataset[0]]+ [x for x in dataset[1:] if len(x[8]+ x[25]+ x[6])>3]

print ("we have ",len(selected_dataset),"entries with a textual descriptive unit")


column_names = selected_dataset.pop(0)

# we structure it in a dataframe
df = pd.DataFrame(selected_dataset[1:], columns=column_names)

# as the language is often missing we add it using langdetect (note that the name of the language might diverge, e.g., ger and de)
langs = []

check = set()

for index, row in df.iterrows():
    if len(row["langMaterial"])==3:
        langs.append(row["langMaterial"])
        if row["langMaterial"] not in check:
            print(row["langMaterial"])
            check.add(row["langMaterial"])
        
    else:
        try:
            l = detect(row["unitTitle"] +" "+ row["titleProper"]+" "+ row["scopeContent"])
            row["langMaterial"] = l
            langs.append(row["langMaterial"])
        except Exception as e:
            print (e)
            continue
        
# %%

        
from collections import Counter

print (Counter(langs).most_common())

# to fix it we use this dictionary, that you would need to expand if you are dealing with other languages

langs_dict = {"de":"de","ger":"de","fr":"fr","fre":"fr","it":"it","en":"en","sl":"sl","pl":"pl","pol":"pl","fi":"fi","sv":"sv","heb":"heb","es":"es","rus":"rus"}
df['langMaterial'] = df['langMaterial'].map(langs_dict)

print (len(df))

# finally we save the pickle file containing the dataframe
with open('test_dataset.pickle', 'wb') as f:
        pickle.dump(df, f)

sample = df[df["langMaterial"] == "fr"]
sample = sample.head(100)

# finally we save the pickle file containing the dataframe
with open('sample_test_dataset.pickle', 'wb') as f:
        pickle.dump(sample, f)