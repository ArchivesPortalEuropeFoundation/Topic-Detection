import json
import os
import pickle
import sys
from configparser import SafeConfigParser
from urllib.parse import unquote

import flask

# Add "../" to path to import utils
sys.path.insert(0, os.path.abspath(os.path.pardir))
from utils import nlp, detect

# Create the application.
APP = flask.Flask(__name__)


@APP.route("/")
def index():
    """Displays the index page accessible at '/'"""
    return flask.render_template("index.html")


@APP.route("/my-form")
def my_form():

    return flask.render_template("my-form.html", langs=langs, message="")


@APP.route("/query", methods=["GET"])
def query_api():
    """
    query_api _summary_

    Returns:
        _type_: _description_
    """
    # we load the dataset

    query = flask.request.args["text"]
    lang = flask.request.args["lang"]
    search_type = flask.request.args["type"]
    n_res = int(flask.request.args["n_res"])
    broad_entity_search = flask.request.args["broad_entity_search"]
    boolean_search = flask.request.args["boolean_search"]
    in_quote_query = nlp.check_quotation(query)

    # currently hardcoded cutoff
    if n_res > 100:
        n_res = 100

    if in_quote_query:
        query = in_quote_query
        search_type = "entity"
        add_note = f'The concept "{query}" correspond to an entry in Wikipedia. '
    else:
        add_note = ""

    if search_type == "concept":
        query_emb = nlp.build_query_vector(query, lang, model_dict, boolean_search)
        if query_emb:
            ranking = nlp.concept_search(
                index,
                query_emb,
                labels,
                doc_names,
                texts,
                all_word_embs,
                startDate,
                endDates,
                altDates,
                countries,
                n_res,
                boolean_search,
            )
            response = ranking.to_html(
                classes="data", index=False, table_id="results", escape=False
            )
        else:
            if boolean_search == "True":
                response = "There is an issue with your query: maybe this is not a boolean search?"

            else:
                response = f'Concept "{query}" not found in embedding space!'

    if search_type == "entity":
        ranking, page = nlp.entity_search(
            query,
            lang,
            labels,
            doc_names,
            texts,
            n_res,
            langs,
            startDate,
            endDates,
            altDates,
            countries,
            broad_entity_search,
            boolean_search,
        )
        if ranking is None:
            response = (
                add_note
                + f"There is an issue with your query: maybe this is not a boolean search?"
            )

        elif ranking.empty:
            response = add_note + f'Mentions of "{query}" not found in corpus!'
        else:
            if boolean_search == "True":
                operator = list(page.keys())[0]
                first_page = unquote(page[operator][0])
                first_title = first_page.split("/")[-1].replace("_", " ")
                if first_page in wiki2viaf:
                    first_viaf = wiki2viaf[first_page]

                    viaf_first_note = (
                        f'The first entity also appears in <a href="{first_viaf}">VIAF</a>. '
                    )
                else:
                    viaf_first_note = ""

                second_page = unquote(page[operator][1])
                second_title = second_page.split("/")[-1].replace("_", " ")

                if second_page in wiki2viaf:
                    second_viaf = wiki2viaf[second_page]
                    viaf_second_note = (
                        f'The second entity also appears in <a href="{second_viaf}">VIAF</a>.'
                    )
                else:
                    viaf_second_note = ""

                response = (
                    add_note
                    + f'We have found results for the entity <a href="{first_page}">{first_title}</a> {operator} the entity <a href="{second_page}">{second_title}</a>. '
                    + viaf_first_note
                    + viaf_second_note
                )

            else:
                page = unquote(page)
                title = page.split("/")[-1].replace("_", " ")
                if page in wiki2viaf:
                    viaf = wiki2viaf[page]
                    viaf_note = f'This entity also appears in <a href="{viaf}">VIAF</a>.'
                else:
                    viaf_note = ""
                response = (
                    add_note
                    + f'We have found results for the entity <a href="{page}">{title}</a>. '
                    + viaf_note
                )
            response += ranking.to_html(
                classes="data", index=False, table_id="results", escape=False
            )

    query_string = (
        query.replace(" ", "+")
        + "_"
        + search_type
        + "_"
        + lang
        + "_"
        + "boolean_search:"
        + boolean_search
        + "_"
        + "broad_entity_search:"
        + broad_entity_search
    )

    download_button = open("../interface/templates/download_button.txt", "r").read()

    download_button = download_button.replace("query_name", query_string)

    return response


@APP.route("/detect", methods=["GET"])
def detector():
    query = flask.request.args["query"]
    lang = flask.request.args["lang"]
    response = detect.tag_string(ner_models, query, lang)
    if type(response) is str:
        return response
    response = response.to_html(classes="data", index=False, table_id="results", escape=False)
    return response


if __name__ == "__main__":
    parser = SafeConfigParser()
    parser.read("../config/config.env")

    test = parser.get("default", "TEST_DATA")
    print(test)

    if test == "True":
        print("test mode: on!")

        with open("data/sample_wiki2viaf.json") as f:
            wiki2viaf = json.load(f)

        # we load the dataset
        with open("data/sample_dataset.pickle", "rb") as f:
            df = pickle.load(f)
            print(len(df), set(df["langMaterial"]))
        model_dict = nlp.load_models(test=True)

        ner_models = detect.load_tagger(test=True)

    else:
        print("test mode: off.")

        with open("data/wiki2viaf.json") as f:
            wiki2viaf = json.load(f)

        with open("data/dataset.pickle", "rb") as f:
            df = pickle.load(f)
            print(len(df))

        ner_models = detect.load_tagger(test=False)

        model_dict = nlp.load_models(test=False)

    (
        embs,
        labels,
        doc_names,
        langs,
        texts,
        all_word_embs,
        startDate,
        endDates,
        altDates,
        countries,
    ) = nlp.prepare_collection(df, model_dict)
    index = nlp.build_index(embs, 300)

    APP.debug = False
    APP.run(port=5000, host="0.0.0.0")
