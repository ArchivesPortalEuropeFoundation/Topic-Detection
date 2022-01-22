import json

wiki2viaf = {}

# download the file from here http://viaf.org/viaf/data/
with open("viaf-20210802-links.txt", "r") as r:
    for line in r:
        if "wiki" in line.lower():
            try:
                viaf = line.split("\t")[0].strip().replace("\n","").replace("\t","").replace("\r","")
                wiki = line.split("\t")[1].split("@")[1].strip().replace("\n","").replace("\t","").replace("\r","")
                wiki2viaf[wiki] = viaf
            except Exception as e:
                print (e,line)

with open('../webapp/data/wiki2viaf.json', 'w') as fp:
    json.dump(wiki2viaf, fp)