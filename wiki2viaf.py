# import bs4 as bs
# import requests

# query = "http://viaf.org/viaf/search?query=local.names%20all%20%22napoleon%22&sortKeys=holdingscount&recordSchema=BriefVIAF"

# sauce = requests.get(query)
# soup = bs.BeautifulSoup(sauce.content,'html.parser')
# table = soup.find_all('table')[0] # it's the only table we get back
# rows = table.find_all("tr")[1:] #exclude header
# top_result = rows[0].find_all("td")[1].find("a")["href"] #top prediction, given query
# page = requests.get(top_result)
# soup = bs.BeautifulSoup(sauce.content,'html.parser')
# print (top_result)
import json

wiki2viaf = {}

with open("/Users/fnanni/Downloads/viaf-20210802-links.txt", "r") as r:
    for line in r:
        if "wiki" in line.lower():
            try:
                viaf = line.split("\t")[0].strip().replace("\n","").replace("\t","").replace("\r","")
                wiki = line.split("\t")[1].split("@")[1].strip().replace("\n","").replace("\t","").replace("\r","")
                wiki2viaf[wiki] = viaf
            except Exception as e:
                print (e,line)

with open('webapp/data/wiki2viaf.json', 'w') as fp:
    json.dump(wiki2viaf, fp)