import pandas
import nltk, string
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity as cs

# for each language under study you need to download its related cross-lingual embeddings from here: https://github.com/facebookresearch/MUSEœ
#de_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.de.vec')
#fr_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.fr.vec')
#en_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.en.vec')
it_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.it.vec')
#fi_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.fi.vec')
#pl_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.pl.vec')
#sl_model = KeyedVectors.load_word2vec_format('word-embs/wiki.multi.sl.vec')

# we just map the language with the word embeddings model

#model_dict = {"fr":fr_model,"en":en_model,"english":en_model,"de":de_model,"it":it_model,"fi":fi_model,"pl":pl_model,"sl":sl_model,"German":de_model,"English":en_model,"Finnish":fi_model,"French":fr_model,"Italian":it_model}
model_dict = {"it":it_model}


def text_embedding(text,lang):
    
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
    else:
        return None

def cossim(v1,v2):
    v1 = np.array(v1).reshape(1, -1)
    v2 = np.array(v2).reshape(1, -1)
    score = cs(v1,v2)[0][0]
    return score

# for each document we create a document embedding and collect its topic label
def prepare_collection(df):
    embs = []
    labels = []
    doc_names = []
    selected_langs = []
    texts = []

    for index, row in df.iterrows():
        lang = row["langMaterial"]
        label = row["filename"].replace(".json","")    
        title = row["titleProper"]

        if lang in model_dict:
            model = model_dict[lang]
            text = row["unitTitle"] +" "+ row["titleProper"]+" "+ row["scopeContent"]
            emb = text_embedding(text,model)
            if emb != None:
                embs.append(emb)
                labels.append(label)
                selected_langs.append(lang)
                doc_names.append(title)
                texts.append(text)
    return embs,labels,doc_names,selected_langs,texts