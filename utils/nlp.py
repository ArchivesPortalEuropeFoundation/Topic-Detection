import re
import string

import faiss
import nltk
import numpy as np
import pandas as pd
import pywikibot
import requests
from gensim.models import KeyedVectors
from pandarallel import pandarallel
from sklearn.metrics.pairwise import cosine_similarity as cs

pandarallel.initialize(use_memory_fs=False)


def load_models(test=False):

    if test:
        # for each language under study you need to download its related cross-lingual embeddings from here: https://github.com/facebookresearch/MUSEœ
        de_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.de.vec")
        fr_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.fr.vec")
        en_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.en.vec")
        it_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.it.vec")
        fi_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.fi.vec")
        pl_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.pl.vec")
        lv_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.lv.vec")
        sl_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.sl.vec")
        es_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.es.vec")
        he_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.he.vec")
        ru_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.ru.vec")
        sv_model = KeyedVectors.load_word2vec_format("word-embs/1000_wiki.multi.sv.vec")
    else:
        # for each language under study you need to download its related cross-lingual embeddings from here: https://github.com/facebookresearch/MUSEœ
        de_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.de.vec")
        fr_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.fr.vec")
        en_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.en.vec")
        it_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.it.vec")
        fi_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.fi.vec")
        pl_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.pl.vec")
        lv_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.lv.vec")
        sl_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.sl.vec")
        es_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.es.vec")
        he_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.he.vec")
        ru_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.ru.vec")
        sv_model = KeyedVectors.load_word2vec_format("word-embs/wiki.multi.sv.vec")

    # we just map the language with the word embeddings model

    model_dict = {
        "es": es_model,
        "heb": he_model,
        "he": he_model,
        "lv": lv_model,
        "sv": sv_model,
        "rus": ru_model,
        "ru": ru_model,
        "fr": fr_model,
        "en": en_model,
        "english": en_model,
        "de": de_model,
        "it": it_model,
        "fi": fi_model,
        "pl": pl_model,
        "sl": sl_model,
        "German": de_model,
        "English": en_model,
        "Finnish": fi_model,
        "French": fr_model,
        "Italian": it_model,
    }
    # model_dict = {"it":it_model}
    return model_dict


def build_query_vector(text, lang, model_dict, boolean_search, query=True):

    if boolean_search == "True":
        if boolean_operation(text):
            first_concept, operator, second_concept = boolean_operation(text)
        else:
            return None
        first_vector, first_word_embs = text_embedding(first_concept, lang, model_dict, query=True)
        second_vector, second_word_embs = text_embedding(
            second_concept, lang, model_dict, query=True
        )

        if first_vector and second_vector:
            return {operator: [first_vector, second_vector]}
    else:
        vector, word_embs = text_embedding(text, lang, model_dict, query=True)
        if vector:
            return vector


exclude = set(string.punctuation)
exclude.add("-")
exclude.remove("*")


class RegexDict(dict):
    def get_matching(self, event):
        return (self[key] for key in self if re.match(key, event))


def text_embedding(text, lang, model_dict, query):

    model = model_dict[lang]

    text = text.lower()

    text = "".join(ch for ch in text if ch not in exclude)

    if "*" in text and query == True:
        # split on whitespaces
        star_words = [word for word in text.split(" ") if "*" in word]
        dot_star_words = [word.replace("*", ".*") for word in star_words]

        for w in range(len(dot_star_words)):
            dot_star_word = dot_star_words[w]
            star_word = star_words[w]
            r = re.compile(dot_star_word)
            matched_words = list(filter(r.match, list(model.key_to_index)))
            text = text.replace(star_word, "")
            text = text + " " + " ".join(matched_words)

    text = nltk.word_tokenize(text)

    text = [token for token in text if token.isalpha()]

    doc_embedd = []
    word_embs = {}

    for word in text:
        try:
            embed_word = model[word]
            doc_embedd.append(embed_word)
            word_embs[word] = embed_word
        except KeyError:
            continue
    if len(doc_embedd) > 0:
        avg = [float(sum(col)) / len(col) for col in zip(*doc_embedd)]
        return avg, word_embs
    else:
        return None, None


def cossim(v1, v2):
    v1 = np.array(v1).reshape(1, -1)
    v2 = np.array(v2).reshape(1, -1)
    score = cs(v1, v2)[0][0]
    return score


rx = r"\w+(?:'\w+)?|[^\w\s]"


def find_match(query, doc):
    # tokenize each query using a regex
    doc = re.findall(rx, doc)
    return doc.count(query)


def count_mentions(candidates, doc):
    # we don't lowercase anymore
    #    candidates = set([x.lower() for x in candidates])
    #    found = {query:doc.lower().count(query) for query in candidates}
    candidates = set([x for x in candidates])
    found = {query: find_match(query, doc) for query in candidates}
    found = {x: y for x, y in found.items() if y > 0}
    n = [y for x, y in found.items()]
    found = [x for x, y in found.items()]
    n = sum(n) / len(doc.split(" "))
    return n, found


def rank_by_freq(candidates, doc, boolean_search):
    if boolean_search == "True":
        operator = list(candidates.keys())[0]
        first_cand, second_cand = candidates[operator]
        first_n, first_count = count_mentions(first_cand, doc)
        second_n, secound_count = count_mentions(second_cand, doc)
        # maybe this is the only bit to modify
        if operator == "AND" and ((first_n > 0.0) and (second_n > 0.0)):
            return [(first_n + second_n) / 2, first_count + secound_count]
        if operator == "OR" and ((first_n > 0.0) or (second_n > 0.0)):
            return [(first_n + second_n) / 2, first_count + secound_count]
        if operator == "ANDNOT" and ((first_n > 0.0) and (second_n == 0.0)):
            return [first_n, first_count]
        else:
            return [0.0, []]

    else:
        n, n_count = count_mentions(candidates, doc)
        return [n, n_count]


def entity_processing(entity):
    entity = entity.split("(")[0]
    entity = entity.translate(str.maketrans("", "", string.punctuation))
    entity = entity.strip()
    return entity


# for each document we create a document embedding and collect its topic label
def prepare_collection(df, model_dict):
    embs = []
    labels = []
    doc_names = []
    langs = []
    texts = []
    startDates = []
    endDates = []
    altDates = []
    countries = []
    all_word_embs = []

    for index, row in df.iterrows():
        lang = row["langMaterial"]
        label = row["filename"].replace(".json", "").title()
        # remove file identifier from the title
        title = "".join(row["titleProper"].split(":")[:-1])

        startDate = row["startDate"].split("-")[0]
        endDate = row["endDate"].split("-")[0]
        altDate = row["alternateUnitdate"]
        country = row["country"].split(":")[0].title()

        if lang in model_dict:
            text = row["unitTitle"] + " " + row["titleProper"] + " " + row["scopeContent"]
            emb, word_embs = text_embedding(text, lang, model_dict, query=False)
            if emb:
                embs.append(emb)
                labels.append(label)
                langs.append(lang)
                doc_names.append(title)
                texts.append(text)
                all_word_embs.append(word_embs)
                startDates.append(startDate)
                endDates.append(endDate)
                altDates.append(altDate)
                countries.append(country)
    return (
        embs,
        labels,
        doc_names,
        langs,
        texts,
        all_word_embs,
        startDates,
        endDates,
        altDates,
        countries,
    )


def concept_search(
    index,
    query_emb,
    labels,
    doc_names,
    texts,
    all_word_embs,
    startDate,
    endDate,
    altDate,
    country,
    how_many_results,
    boolean_search,
):
    if boolean_search == "True":
        operator = list(query_emb.keys())[0]
        first_vector, second_vector = query_emb[operator]
        ext_how_many_results = how_many_results * 10
        # results first element
        xq = np.array([first_vector]).astype("float32")
        D, I = index.search(
            xq, ext_how_many_results
        )  # we need to retrieve more results to check the overlap
        res = {I[0][i]: D[0][i] for i in range(len(I[0]))}
        first_ranking = [
            [
                doc_names[i],
                labels[i],
                make_concept_bold(texts[i], all_word_embs[i], np.array(first_vector)),
                startDate[i],
                endDate[i],
                altDate[i],
                country[i],
                1.0 - d,
            ]
            for i, d in res.items()
        ]
        # results second element
        xq = np.array([second_vector]).astype("float32")
        D, I = index.search(
            xq, ext_how_many_results
        )  # we need to retrieve more results to check the overlap
        res = {I[0][i]: D[0][i] for i in range(len(I[0]))}
        second_ranking = [
            [
                doc_names[i],
                labels[i],
                make_concept_bold(texts[i], all_word_embs[i], np.array(second_vector)),
                startDate[i],
                endDate[i],
                altDate[i],
                country[i],
                1.0 - d,
            ]
            for i, d in res.items()
        ]
        second_ranking_dict = {x[0]: x[-1] for x in second_ranking}
        # aggregation
        if operator == "AND":
            ranking = [
                [
                    x[0],
                    x[1],
                    x[2],
                    x[3],
                    x[4],
                    x[5],
                    x[6],
                    (x[-1] + second_ranking_dict[x[0]]) / 2,
                ]
                for x in first_ranking
                if x[0] in second_ranking_dict
            ][:how_many_results]
        if operator == "OR":
            ranking = [
                x for x in first_ranking if x[0] not in second_ranking_dict
            ] + second_ranking
            ranking.sort(key=lambda x: x[-1], reverse=True)
            ranking = ranking[:how_many_results]
        if operator == "ANDNOT":
            second_ranking = {x[0]: x[-1] for x in second_ranking}
            ranking = [
                [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[-1]]
                for x in first_ranking
                if x[0] not in second_ranking_dict
            ][:how_many_results]

    else:
        xq = np.array([query_emb]).astype("float32")
        D, I = index.search(xq, how_many_results)  # actual search
        res = {I[0][i]: D[0][i] for i in range(len(I[0]))}
        ranking = [
            [
                doc_names[i],
                labels[i],
                make_concept_bold(texts[i], all_word_embs[i], np.array(query_emb)),
                startDate[i],
                endDate[i],
                altDate[i],
                country[i],
                1.0 - d,
            ]
            for i, d in res.items()
        ]

    df = pd.DataFrame(
        ranking,
        columns=[
            "Filename",
            "Topic",
            "Content",
            "startDate",
            "endDate",
            "altDate",
            "Country",
            "Score",
        ],
    )

    df = check_dataframe(df)

    return df


def check_dataframe(df):

    # create period using either Start / End or altDate
    period = [
        df["startDate"].iloc[x] + "-" + df["endDate"].iloc[x]
        if (len(df["startDate"].iloc[x]) > 0 and len(df["endDate"].iloc[x]) > 0)
        else df["altDate"].iloc[x]
        for x in range(len(df["startDate"]))
    ]
    df["Period"] = period

    # remove specific dates
    df = df.drop("endDate", 1)
    df = df.drop("startDate", 1)
    df = df.drop("altDate", 1)

    # move score as last column
    score = df.pop("Score")
    df["Score"] = score

    return df


def make_concept_bold(content, word_embs, query_emb):
    most_rel_words = [
        [word, cossim(query_emb, wemb)] for word, wemb in word_embs.items() if len(word) > 3
    ]  # ignoring very short words
    most_rel_words.sort(key=lambda x: x[1], reverse=True)
    most_rel_words = [x[0] for x in most_rel_words[:5]]  # top 5 words
    tok_content = re.findall(rx, content)
    for w in range(len(most_rel_words)):
        word = most_rel_words[w]
        if word in tok_content:
            content = content.replace(
                word, '<span class="relevance_' + str(w + 1) + '">' + word + "</span>"
            )
        elif word.title() in tok_content:
            content = content.replace(
                word.title(),
                '<span class="relevance_' + str(w + 1) + '">' + word.title() + "</span>",
            )
        elif word.upper() in tok_content:
            content = content.replace(
                word.upper(),
                '<span class="relevance_' + str(w + 1) + '">' + word.upper() + "</span>",
            )

    content += " ".join(most_rel_words)
    return content


def build_index(embs, d):
    d = 300  # dimension
    nb = len(embs)  # database size
    xb = np.array(embs).astype("float32")

    index = faiss.IndexFlatL2(d)  # build the index
    index.add(xb)  # add vectors to the index
    return index


def get_redirect(lang, page, site):
    r = requests.get(
        "https://"
        + lang
        + ".wikipedia.org/w/api.php?action=query&titles="
        + page.title()
        + "&&redirects&format=json"
    )
    entity = r.json()["query"]
    if "redirects" in entity.keys():
        entity = r.json()["query"]["redirects"][0]["to"]
        page = pywikibot.Page(site, entity)
        url = page.full_url()
        item = pywikibot.ItemPage.fromPage(page)
        return item, url
    else:
        return None, None


def get_url(entity, lang):
    site = pywikibot.Site(lang, "wikipedia")
    page = pywikibot.Page(site, entity)
    url = page.full_url()
    return page, url, site


def get_entity(entity, lang):
    page, url, site = get_url(entity, lang)
    if check_redirect(page, "de", site) != False:
        return url


def check_redirect(page, lang, site):
    try:
        item = pywikibot.ItemPage.fromPage(page)
        return item
    except pywikibot.exceptions.NoPageError:
        try:
            item, page = get_redirect(lang, page, site)
            if item is None:
                return False
            return item
        except pywikibot.exceptions.NoPageError:
            return False


def get_candidates(entity, lang, selected_langs, broad_entity_search):
    page, url, site = get_url(entity, lang)
    candidates = set()
    item = check_redirect(page, lang, site)

    if item == False:
        return candidates, ""

    item_dict = item.get()

    wiki_labels = item_dict["labels"]
    aliases = item_dict["aliases"]
    langs = set(list(wiki_labels.keys()) + list(aliases.keys()))

    candidates.add(entity)

    set_selected_langs = set(selected_langs)

    for lang in langs:
        if broad_entity_search == "False" and lang not in set_selected_langs:
            continue
        if lang in wiki_labels:
            candidates.add(wiki_labels[lang])
        if lang in aliases:
            for al in aliases[lang]:
                # hardcoded cutoff for the moment to avoid timeout given too many cands
                if len(candidates) < 50:
                    candidates.add(al)
    return candidates, url


def boolean_operation(query):
    operators = ["ANDNOT", "OR", "AND"]
    for op in operators:
        if op in query:
            first_el, second_el = query.split(" " + op + " ")
            return first_el, op, second_el


def check_quotation(query):
    if '"' in query:
        query = re.findall(r'"([^"]*)"', query)[0]
        if len(query) > 1:
            return query


def make_entity_bold(mentions, content):
    for mention in mentions:
        content = content.replace(mention, '<span class="relevance_1">' + mention + "</span>")
    return content


def entity_search(
    entity,
    lang,
    labels,
    doc_names,
    texts,
    how_many_results,
    selected_langs,
    startDate,
    endDates,
    altDate,
    countries,
    broad_entity_search,
    boolean_search,
):

    ranking = [
        [
            doc_names[id_],
            labels[id_],
            texts[id_],
            selected_langs[id_],
            startDate[id_],
            endDates[id_],
            altDate[id_],
            countries[id_],
        ]
        for id_ in range(len(texts))
    ]
    ranking = pd.DataFrame(
        ranking,
        columns=[
            "Filename",
            "Topic",
            "Content",
            "Lang",
            "startDate",
            "endDate",
            "altDate",
            "Country",
        ],
    )

    if boolean_search == "True":

        if boolean_operation(entity):
            first_entity, operator, second_entity = boolean_operation(entity)
        else:
            return None, None
        first_cand, first_page = get_candidates(
            first_entity, lang, selected_langs, broad_entity_search
        )
        second_cand, second_page = get_candidates(
            second_entity, lang, selected_langs, broad_entity_search
        )
        candidates = {operator: [first_cand, second_cand]}
        page = {operator: [first_page, second_page]}
    else:
        candidates, page = get_candidates(entity, lang, selected_langs, broad_entity_search)
        print(len(candidates))

    ranking["Results"] = ranking.parallel_apply(
        lambda x: rank_by_freq(candidates, x["Content"], boolean_search), axis=1
    )
    ranking[["Score", "Mentions"]] = ranking["Results"].tolist()
    ranking = ranking.drop("Results", 1)
    ranking = ranking.sort_values("Score", ascending=False)
    ranking = ranking.head(how_many_results)
    ranking = ranking[ranking["Score"] > 0.0]
    print(ranking)
    try:
        ranking["Content"] = ranking.parallel_apply(
            lambda x: make_entity_bold(x["Mentions"], x["Content"]), axis=1
        )
    except ValueError as e:
        print(e)
    ranking = ranking.drop("Mentions", 1)
    ranking = ranking.drop("Lang", 1)

    ranking = check_dataframe(ranking)

    return ranking, page
