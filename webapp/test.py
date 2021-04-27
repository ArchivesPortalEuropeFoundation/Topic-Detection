import faiss                   # make faiss available
import pickle
import numpy as np
import pandas as pd
from utils import nlp

# we load the dataset
with open('data/sample_dataset.pickle', 'rb') as f:
#with open('../dataset.pickle', 'rb') as f:
    df = pickle.load(f)  
embs,labels,doc_names,selected_langs,texts = nlp.prepare_collection(df)

def build_index(embs,d):
    d = 300                           # dimension
    nb = len(embs)                      # database size
    xb = np.array(embs).astype('float32')
    query_emb = nlp.text_embedding("and","en")
    xq = np.array([query_emb]).astype('float32')
    index = faiss.IndexFlatL2(d)   # build the index
    index.add(xb)                  # add vectors to the index
    print(index.ntotal)

def search(query_emb,embs,labels,doc_names,selected_langs,texts,how_many_results):

    k = 4                          # we want to see 4 nearest neighbors

    D, I = index.search(xq, k)     # actual search
    res = {I[0][i]:D[0][i] for i in range(len(I[0]))}
    ranking = [[doc_names[i],labels[i],texts[i],d] for i,d in res.items()]
    df = pd.DataFrame(ranking, columns=["Filename", "Labels", "Content", "Score"])
    print (df)

def search(query_emb,embs,labels,doc_names,selected_langs,texts,how_many_results):
    ranking = [[doc_names[x],labels[x],texts[x],cossim(embs[x],query_emb)] for x in range(len(embs))]
    ranking.sort(key=lambda x: x[3],reverse=True)

    ranking = ranking[:how_many_results]
    df = pd.DataFrame(ranking, columns=["Filename", "Labels", "Content", "Score"])
    return df