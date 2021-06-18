# %%

import os, json,pickle
import pandas as pd
from langdetect import detect
from collections import Counter

# in data you will store the topic related json files
path = 'webapp/data/'

aggregating_fields = ["langMaterial","unitTitle","titleProper","scopeContent","topic"]

dataset = [["id","langMaterial","unitTitle","titleProper","scopeContent","topic","filename"]]

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

# we remove al columns that do not contain text (where we have less than 3 chars)
selected_dataset = [dataset[0]]+ [x for x in dataset[1:] if len(x[4])>3]

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

# finally we save the pickle file containing the dataframe
with open('dataset.pickle', 'wb') as f:
        pickle.dump(df, f)