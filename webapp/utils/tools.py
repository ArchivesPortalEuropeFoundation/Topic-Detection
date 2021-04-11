from bs4 import BeautifulSoup
import requests
from collections import Counter


def Wikipedia_search(text,lang):
    url = "https://"+lang+".wikipedia.org/w/index.php?cirrusUserTesting=control&search="+text+"&title=Sp%C3%A9cial%3ARecherche&fulltext=1&ns0=1"
    
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data)
    try:
        tabledata = soup.find("ul", attrs={"class": "mw-search-results"})
        first_res = tabledata.findAll("li", attrs={"class": "mw-search-result"})[0]
        first_entity = first_res.find("a")["href"]
        return first_entity
    except AttributeError:
        return None

import nltk

def check_stop(text,stopwords):
    text = text.split(" ")
    for w in text:
        if w not in stopwords:
            return False
    return True


ngram_up_to = 3

import string

exclude = set(string.punctuation)

def strip_punct(text):
    s = ''.join(ch for ch in text if ch not in exclude)
    return s

def get_all_ngrams(text,ngram_up_to):
    """Returns all ngrams from a text up to a certain number.
    
    Args:
        text: a string.
        ngram_up_to: a integer.
    Returns:
        A list of ngrams.
    """
    
    tokens = nltk.word_tokenize(text)
    ngrams = [" ".join(x) for n in range(1,ngram_up_to+1) for x in nltk.ngrams(tokens,n)]        
    return ngrams
 


def remove_substrings(candidate_mentions,stopwords,cutoff):
    """Removes very short candidate mentions (<2 chars) 
    and ngrams that are substrings of a more popular one.
    
    Args:
        candidate_mentions: list of tuples (candidate_mention (str), probability score (float)).
    Returns:
        A final list of mentions as strings.      
    """
    candidate_mentions = Counter(candidate_mentions).most_common()
    
    stopwords = [x for x,y in candidate_mentions if len(x.split(" "))<2][:stopwords]

    candidate_mentions = [(cand,score) for cand,score in candidate_mentions if len(cand)>3 and cand not in stopwords][:cutoff]
    
    one_word_cand_mentions = [(cand,score) for cand,score in candidate_mentions if len(cand.split(" "))<2]

    longer_cand_mentions = [(cand,score) for cand,score in candidate_mentions if (cand,score) not in one_word_cand_mentions and check_stop(cand,stopwords) is False]
        
    longer_cand_mentions.sort(key=lambda cand: cand[1], reverse=True)
    one_word_cand_mentions.sort(key=lambda cand: cand[1], reverse=True)
    
    resorted_cand_mentions = longer_cand_mentions + one_word_cand_mentions
    
    mentions = []
    for cand,score in resorted_cand_mentions:
        if not any([cand in mention for mention in mentions]):
            mentions.append(cand)
    return mentions
     
