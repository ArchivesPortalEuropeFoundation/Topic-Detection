import os
import json
import pickle
import flask
import bcrypt
from utils import nlp
from random import randint
from urllib.parse import unquote
from configparser import SafeConfigParser


# Create the application.
APP = flask.Flask(__name__)

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')


@APP.route('/my-form')
def my_form():

    return flask.render_template('my-form.html',langs=langs,message="")

@APP.route('/query', methods=['GET'])
def query_api():

    # we load the dataset

    query = flask.request.args['text']
    lang = flask.request.args['lang']
    search_type = flask.request.args['type']
    n_res = int(flask.request.args['n_res'])
    broad_entity_search = flask.request.args['broad_entity_search']
    boolean_search = flask.request.args['boolean_search']
    in_quote_query = nlp.check_quotation(query)
    
    if in_quote_query:
        query = in_quote_query
        search_type = "entity"
        add_note = f'The concept "{query}" correspond to an entry in Wikipedia. '
    else:
        add_note = ""

    if search_type == "concept":
        query_emb = nlp.build_query_vector(query,lang,model_dict,boolean_search)
        if query_emb:
            ranking= nlp.concept_search(index,query_emb,labels,doc_names,texts,all_word_embs,startDate,endDates,altDates,countries,n_res,boolean_search)
            response = ranking.to_html(classes='data',index=False, table_id = 'results', escape=False)
        else:
            if boolean_search == "True":
                response =  'There is an issue with your query: maybe this is not a boolean search?'

            else:
                response= f'Concept "{query}" not found in embedding space!'

    if search_type == "entity":
        ranking, page = nlp.entity_search(query,lang,labels,doc_names,texts,n_res,langs,startDate,endDates,altDates,countries,broad_entity_search,boolean_search)
        if ranking is None:
            response =  add_note+ f'There is an issue with your query: maybe this is not a boolean search?'
        
        elif ranking.empty:
            response =  add_note+ f'Mentions of "{query}" not found in corpus!'
        else:
            if boolean_search == "True":
                operator = list(page.keys())[0]
                first_page = unquote(page[operator][0])
                first_title = first_page.split("/")[-1].replace("_"," ")
                if first_page in wiki2viaf:
                    first_viaf = wiki2viaf[first_page] 

                    viaf_first_note = f'The first entity also appears in <a href="{first_viaf}">VIAF</a>. '
                else:
                    viaf_first_note = ''

                second_page = unquote(page[operator][1])
                second_title = second_page.split("/")[-1].replace("_"," ")

                if second_page in wiki2viaf:
                    second_viaf = wiki2viaf[second_page] 
                    viaf_second_note = f'The second entity also appears in <a href="{second_viaf}">VIAF</a>.'
                else:
                    viaf_second_note = ''

                response = add_note+ f'We have found results for the entity <a href="{first_page}">{first_title}</a> {operator} the entity <a href="{second_page}">{second_title}</a>. ' + viaf_first_note + viaf_second_note

            else:
                page = unquote(page)
                title = page.split("/")[-1].replace("_"," ")
                if page in wiki2viaf:
                    viaf = wiki2viaf[page] 
                    viaf_note = f'This entity also appears in <a href="{viaf}">VIAF</a>.'
                else:
                    viaf_note = ""
                response = add_note + f'We have found results for the entity <a href="{page}">{title}</a>. ' + viaf_note
            response += ranking.to_html(classes='data',index=False, table_id = 'results', escape=False)

    query_string = query.replace(" ","+") +"_"+search_type+"_"+lang+"_"+"boolean_search:"+boolean_search+"_"+"broad_entity_search:"+broad_entity_search

    download_button = open("../interface/templates/download_button.txt","r").read()

    download_button= download_button.replace("query_name",query_string)

    return response


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

@APP.route('/registration', methods=['GET'])
def registration():
    f = open('../cred.json',"r")
    cred = json.load(f)
    f.close()
    
    # we load the dataset
    user = flask.request.args['user']
    email = flask.request.args['email']
    pw = flask.request.args['pw']
    pw = get_hashed_password(pw)
    code = randint(100000, 999999)  
    
    if email not in cred:
        cred[email] = {"user":user,"pw":pw, "code":code}
        with open('../cred.json', 'w') as f:
            json.dump(cred, f)



        return True
    else:
        return False


@APP.route('/login', methods=['GET'])
def login():
    f = open('../cred.json',"r")
    cred = json.load(f)
    f.close()
    # we load the dataset
    email = flask.request.args['email']
    pw = flask.request.args['pw']

    print (email)
    print (pw)
    
    if email in cred and check_password(pw, cred[email]["pw"]):
        return True
    else:
        return False
    

if __name__ == '__main__':
    parser = SafeConfigParser()
    parser.read('../config/config.env')

    test = parser.get('default', 'TEST_DATA')
    print (test)

    if test == "True":
        print ('test mode: on!')

        with open('data/sample_wiki2viaf.json') as f:
            wiki2viaf = json.load(f)

        # we load the dataset
        with open('data/sample_dataset.pickle', 'rb') as f:
            df = pickle.load(f) 
            print (len(df),set(df["langMaterial"])) 
        model_dict = nlp.load_models(test=True)
    
    else:
        print ('test mode: off.')

        with open('data/wiki2viaf.json') as f:
            wiki2viaf = json.load(f)

        with open('data/dataset.pickle', 'rb') as f:
            df = pickle.load(f)  
            print (len(df)) 
        model_dict = nlp.load_models(test=False)

    embs,labels,doc_names,langs,texts,all_word_embs,startDate,endDates,altDates,countries = nlp.prepare_collection(df,model_dict)
    index = nlp.build_index(embs,300)
    
    APP.debug=False
    APP.run(port=5000, host='0.0.0.0')
