import faiss                  
import pickle
import wikipedia
import pandas as pd
from utils import nlp
import nltk, string
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import unquote,quote
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity as cs
from sklearn.feature_extraction.text import TfidfVectorizer

def load_models(test=False):

    if test:
        # for each language under study you need to download its related cross-lingual embeddings from here: https://github.com/facebookresearch/MUSEœ
        de_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.de.vec')
        fr_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.fr.vec')
        en_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.en.vec')
        it_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.it.vec')
        fi_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.fi.vec')
        pl_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.pl.vec')
        sl_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.sl.vec')
        es_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.es.vec')
        he_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.he.vec')
        ru_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.ru.vec')
        sv_model = KeyedVectors.load_word2vec_format('word-embs/1000_wiki.multi.sv.vec')
    else:
        # for each language under study you need to download its related cross-lingual embeddings from here: https://github.com/facebookresearch/MUSEœ
        de_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.de.vec')
        fr_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.fr.vec')
        en_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.en.vec')
        it_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.it.vec')
        fi_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.fi.vec')
        pl_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.pl.vec')
        sl_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.sl.vec')
        es_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.es.vec')
        he_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.he.vec')
        ru_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.ru.vec')
        sv_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.sv.vec')

    # we just map the language with the word embeddings model

    model_dict = {"es":es_model,"heb":he_model,"sv":sv_model,"rus":ru_model,"fr":fr_model,"en":en_model,"english":en_model,"de":de_model,"it":it_model,"fi":fi_model,"pl":pl_model,"sl":sl_model,"German":de_model,"English":en_model,"Finnish":fi_model,"French":fr_model,"Italian":it_model}
    #model_dict = {"it":it_model}
    return model_dict

def text_embedding(text,lang,model_dict):
    
    exclude = set(string.punctuation)
    exclude.add("-")

    model = model_dict[lang]

    
    text = text.lower()
    
    text = ''.join(ch for ch in text if ch not in exclude)
    
    text = nltk.word_tokenize(text)
        
    text = [token for token in text if token.isalpha()]
    
    doc_embedd = []
    
    for word in text:
            try:
                embed_word = model[word]
                doc_embedd.append(embed_word)
            except KeyError:
                continue
    if len(doc_embedd)>0:
        avg = [float(sum(col))/len(col) for col in zip(*doc_embedd)]
        return avg

def cossim(v1,v2):
    if v1 and v2:
        v1 = np.array(v1).reshape(1, -1)
        v2 = np.array(v2).reshape(1, -1)
        score = cs(v1,v2)[0][0]
        return score
    else:
        return 0.0


tfidf_vectorizer=TfidfVectorizer()

def rank_by_freq(query,doc,allow_partial_match):
    if allow_partial_match:
        query = query.lower()
        doc = doc.lower()
        tfidf=tfidf_vectorizer.fit_transform([query,doc])
        score = cs(tfidf)[0][1]
        return score
    else:
        n = doc.lower().count(query.lower())
        n = n/len(doc.split(" "))
        return n

def entity_processing(entity):
    entity = entity.split("(")[0]
    entity = entity.translate(str.maketrans('', '', string.punctuation))
    entity = entity.strip()
    return entity



# for each document we create a document embedding and collect its topic label
def prepare_collection(df,model_dict):
    embs = []
    labels = []
    doc_names = []
    selected_langs = set()
    texts = []

    for index, row in df.iterrows():
        lang = row["langMaterial"]
        label = row["filename"].replace(".json","")    
        title = row["titleProper"]

        if lang in model_dict:
            text = row["unitTitle"] +" "+ row["titleProper"]+" "+ row["scopeContent"]
            emb = text_embedding(text,lang,model_dict)
            if emb:
                embs.append(emb)
                labels.append(label)
                selected_langs.add(lang)
                doc_names.append(title)
                texts.append(text)
    selected_langs = list(selected_langs)
    return embs,labels,doc_names,selected_langs,texts

def concept_search(index,query_emb,labels,doc_names,texts,how_many_results):
    xq = np.array([query_emb]).astype('float32')
    D, I = index.search(xq, how_many_results)     # actual search
    res = {I[0][i]:D[0][i] for i in range(len(I[0]))}
    ranking = [[doc_names[i],labels[i],texts[i],1.0-d] for i,d in res.items()]
    df = pd.DataFrame(ranking, columns=["Filename", "Labels", "Content", "Score"])
    return df

def build_index(embs,d):
    d = 300                           # dimension
    nb = len(embs)                      # database size
    xb = np.array(embs).astype('float32')

    index = faiss.IndexFlatL2(d)   # build the index
    index.add(xb)                  # add vectors to the index
    return index

def entity_search(entity,lang,labels,doc_names,texts,how_many_results,selected_langs,allow_partial_match):
    wikipedia.set_lang(lang)
    res = wikipedia.search(entity)[0]
    wiki_url = "https://"+lang+".wikipedia.org/wiki/"+quote(res.replace(" ","_"))
    resource = urlopen(wiki_url)
    content =  resource.read()

    soup = BeautifulSoup(content,features="html.parser")

    translations = {el.get('lang'): unquote(el.get('href')).split("/")[-1].replace("_"," ") for el in soup.select('li.interlanguage-link > a')}

    translations[lang] = entity.strip()


    translations = {x:entity_processing(y) for x,y in translations.items() if x in selected_langs}

    ranking = [[[doc_names[id_],labels[id_],texts[id_], rank_by_freq(query,texts[id_],allow_partial_match)] for id_ in range(len(selected_langs)) if selected_langs[id_]==lang] for lang,query in translations.items() ]
    ranking = [y for x in ranking for y in x if y[3]>0.0]
    print ("Documents mentioning the entity '",entity,"' :", len(ranking),"among",len(labels),".")

    ranking.sort(key=lambda x: x[3],reverse=True)
    ranking = ranking[:how_many_results]
    df = pd.DataFrame(ranking, columns=["Filename", "Labels", "Content", "Score"])
    return df
    
