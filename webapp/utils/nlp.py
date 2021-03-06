import faiss                  
import pickle
import pywikibot
import wikipedia
import nltk, string
import numpy as np
import pandas as pd
from utils import nlp
from bs4 import BeautifulSoup
from pandarallel import pandarallel
from urllib.request import urlopen
from urllib.parse import unquote,quote
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity as cs
from sklearn.feature_extraction.text import TfidfVectorizer

pandarallel.initialize()


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

# def rank_by_freq(query,doc,allow_partial_match):
#     if allow_partial_match == "True":
#         query = query.lower()
#         doc = doc.lower()
#         tfidf=tfidf_vectorizer.fit_transform([query,doc])
#         score = cs(tfidf)[0][1]
#         return score
#     else:
#         n = doc.lower().count(query.lower())
#         n = n/len(doc.split(" "))
#         return n

def rank_by_freq(candidates,doc):
    candidates = set([x.lower() for x in candidates])
    n = [doc.lower().count(query) for query in candidates]
    n = sum(n)/len(doc.split(" "))
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
    langs = []
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
                langs.append(lang)
                doc_names.append(title)
                texts.append(text)
    return embs,labels,doc_names,langs,texts

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

def entity_search(entity,lang,labels,doc_names,texts,how_many_results,selected_langs,broad_entity_search):

    set_selected_langs = set(selected_langs)

    site = pywikibot.Site(lang, "wikipedia")
    page = pywikibot.Page(site, entity)
    item = pywikibot.ItemPage.fromPage(page)
    item_dict = item.get()

    wiki_labels = item_dict["labels"]
    aliases = item_dict["aliases"]

    langs = set(list(wiki_labels.keys()) + list(aliases.keys()))

    candidates = set()
    candidates.add(entity)

    for lang in langs:
        if broad_entity_search == "False" and lang not in set_selected_langs:
            continue
        if lang in wiki_labels:
            candidates.add(wiki_labels[lang])
        if lang in aliases:
            for al in aliases[lang]:
                candidates.add(al)

    print (candidates)

    ranking = [[doc_names[id_],labels[id_],texts[id_],selected_langs[id_]] for id_ in range(len(texts))]
    ranking = pd.DataFrame(ranking, columns=["Filename", "Labels", "Content", "Lang"])
    ranking["Score"] = ranking.parallel_apply(lambda x: rank_by_freq(candidates, x['Content']), axis=1)
    ranking = ranking.sort_values('Score', ascending=False)
    ranking = ranking.head(how_many_results)
    ranking = ranking[ranking["Score"]>0.0]

    return ranking
    
