import pandas as pd
from utils import nlp
import pickle
with open('data/sample_dataset.pickle', 'rb') as f:
    df = pickle.load(f)  
model_dict = nlp.load_models(test=True)
    
embs,labels,doc_names,langs,texts = nlp.prepare_collection(df,model_dict)

text = "Napoleon"
lang = "en" 
n_res = 10 
allow_partial_match = False
ranking = nlp.entity_search(text,lang,labels,doc_names,texts,n_res,langs,allow_partial_match)