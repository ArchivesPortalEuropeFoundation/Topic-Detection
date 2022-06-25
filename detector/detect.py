import os
import sys

import pandas as pd
from flair.data import Sentence
from flair.models import SequenceTagger

# Add "../" to path to import utils
sys.path.insert(0, os.path.abspath(os.path.pardir))
from utils import nlp


# load tagger
def load_tagger(test=False):
    if test is True:
        en_tagger = SequenceTagger.load("flair/ner-english-fast")
        return {"en": en_tagger}

    en_tagger = SequenceTagger.load("flair/ner-english")
    de_tagger = SequenceTagger.load("flair/ner-german")
    fr_tagger = SequenceTagger.load("flair/ner-french")
    nl_tagger = SequenceTagger.load("flair/ner-dutch")

    ner_dict = {"en": en_tagger, "de": de_tagger, "fr": fr_tagger, "nl": nl_tagger}
    return ner_dict


def tag_string(ner_dict: dict, text: str, lang: str) -> [str]:
    """
    Given a string and a language returns the urls of the identified entities

    Args:
        ner_dict (dict): A dict with the loaded models
        text (str): A string of text
        lang (str): a language (either en,de,fr,nl - only en for test)
    Returns:
        [str]: A list containing the urls of the identified entities
    """
    if lang not in ner_dict:
        return f'The language "{lang}" is not currently supported. The languages available are: en,de,fr,nl'

    sentence = Sentence(text)
    tagger = ner_dict[lang]

    # predict NER tags
    tagger.predict(sentence)

    ents = []

    for entity in sentence.get_spans("ner"):
        print(entity.text)
        url = nlp.get_url(entity.text, lang)
        str_url = "<a href=" + url + ">" + entity.text + "</a>"
        ents.append(str_url)
    headers = ["Content", "Entities"]
    df = pd.DataFrame([[text, ents]], columns=headers)

    return df
