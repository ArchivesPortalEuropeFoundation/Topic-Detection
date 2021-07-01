import json
import pickle
import flask
import bcrypt
from utils import nlp
from argparse import ArgumentParser
from random import randint


parser = ArgumentParser()
parser.add_argument("-t", "--test", dest="test",
                    help="select True for testmode, else False", default=False)

args = parser.parse_args()

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

    html = open('../interface/index.html','r').read()

    # we load the dataset

    query = flask.request.args['text']
    lang = flask.request.args['lang']
    search_type = flask.request.args['type']
    n_res = int(flask.request.args['n_res'])
    broad_entity_search = flask.request.args['broad_entity_search']
    boolean_search = flask.request.args['boolean_search']
    
    if search_type == "concept":
        query_emb = nlp.build_query_vector(query,lang,model_dict,boolean_search)
        if query_emb:
            ranking= nlp.concept_search(index,query_emb,labels,doc_names,texts,n_res,boolean_search)
            response = ranking.to_html(classes='data',index=False, table_id = 'results')
        else:
            response= f'Concept "{query}" not found in embedding space!'

    if search_type == "entity":
        #for the moment hardcoded
        ranking = nlp.entity_search(query,lang,labels,doc_names,texts,n_res,langs,broad_entity_search,boolean_search)
        if ranking.empty:
            response =  f'Mentions of "{query}" not found in corpus!'
        else:
            response = ranking.to_html(classes='data',index=False, table_id = 'results')

    download_button = open("../interface/templates/download_button.txt","r").read()

    html = html.replace(" SELECTED ","")
    html = html.replace('placeholder="Your query"','placeholder="Your query was: '+query+'"')
    html = html.replace('<option value= "'+search_type+'">'+search_type+'</option>','<option value= "'+search_type+'" SELECTED >'+search_type+'</option>')
    html = html.replace('<option value= "'+lang+'">'+lang+'</option>','<option value= "'+lang+'" SELECTED >'+lang+'</option>')
    
    html = html.replace("<query></query>",download_button)
    
    html = html.replace("<table></table>",response)

    return html


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

    test = args.test
    if test == "True":
        print ('test mode: on!')

        # we load the dataset
        with open('data/sample_dataset.pickle', 'rb') as f:
            df = pickle.load(f)  
        model_dict = nlp.load_models(test=True)
    
    else:
        print ('test mode: off.')

        with open('data/dataset.pickle', 'rb') as f:
            df = pickle.load(f)  
        model_dict = nlp.load_models(test=False)

    embs,labels,doc_names,langs,texts = nlp.prepare_collection(df,model_dict)
    index = nlp.build_index(embs,300)
    
    APP.debug=False
    APP.run(port=6000)
