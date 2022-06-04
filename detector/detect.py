import os
import sys

from flair.data import Sentence
from flair.models import SequenceTagger

# Add "../" to path to import utils
sys.path.insert(0, os.path.abspath(os.path.pardir))
from utils import nlp

# load tagger
en_tagger = SequenceTagger.load("flair/ner-english")
de_tagger = SequenceTagger.load("flair/ner-german")
fr_tagger = SequenceTagger.load("flair/ner-french")
nl_tagger = SequenceTagger.load("flair/ner-dutch")

ner_dict = {'en':en_tagger,'de':de_tagger,'fr':fr_tagger,'nl':nl_tagger}

def tag_string(text:str,lang:str)->[str]:
    """
    Given a string and a language returns the urls of the identified entities

    Args:
        text (str): A string of text
        lang (str): a language (either en,de,fr,nl)
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
        url = nlp.get_url(entity.text,lang)
        ents.append(url)
    return ents
# make example sentence
text = "Berlin ist eine schöne Stadt mit dem Deutschen Bundestag"
lang = 'de'
print (tag_string(text,lang))
