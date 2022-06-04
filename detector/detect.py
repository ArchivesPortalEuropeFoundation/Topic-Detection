import os
import sys

from flair.data import Sentence
from flair.models import SequenceTagger

# Add "../" to path to import utils
sys.path.insert(0, os.path.abspath(os.path.pardir))
from utils import nlp

# load tagger
tagger = SequenceTagger.load("flair/ner-english")

# make example sentence
sentence = Sentence("George Washington went to Washington")

# predict NER tags
tagger.predict(sentence)

for entity in sentence.get_spans("ner"):
    print(entity)
