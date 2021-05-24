import flask
import pickle
from utils import nlp
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

@APP.route('/my-form', methods=['POST'])
def my_form_post():

    # we load the dataset

    text = flask.request.form['text']
    lang = flask.request.form['lang']
    search_type = flask.request.form['type']
    n_res = int(flask.request.form['n_res'])
    if search_type == "concept":
        query_emb = nlp.text_embedding(text,lang)
        if query_emb:
            ranking= nlp.concept_search(index,query_emb,labels,doc_names,texts,n_res)
        else:
            return flask.render_template('my-form.html',langs=langs,message="Concept not found in embedding space!")

    if search_type == "entity":
        #for the moment hardcoded
        allow_partial_match = True
        ranking = nlp.entity_search(text,lang,labels,doc_names,texts,n_res,langs,allow_partial_match)
        if ranking.empty:
            return flask.render_template('my-form.html',langs=langs,message="Entity mentions not found in corpus!")
    return flask.render_template('my-form.html',  tables=[ranking.to_html(classes='data',index=False)], titles=ranking.columns.values,langs=langs)



@APP.route('/query', methods=['GET'])
def query_api():

    # we load the dataset

    text = flask.request.args['text']
    lang = flask.request.args['lang']
    search_type = flask.request.args['type']
    n_res = int(flask.request.args['n_res'])
    if search_type == "concept":
        query_emb = nlp.text_embedding(text,lang)
        if query_emb:
            ranking= nlp.concept_search(index,query_emb,labels,doc_names,texts,n_res)
        else:
            return "Concept not found in embedding space!"

    if search_type == "entity":
        #for the moment hardcoded
        allow_partial_match = True
        ranking = nlp.entity_search(text,lang,labels,doc_names,texts,n_res,langs,allow_partial_match)
        if ranking.empty:
            return "Entity mentions not found in corpus!"
    return ranking.to_html(classes='data',index=False)



if __name__ == '__main__':

    # we load the dataset
    with open('data/sample_dataset.pickle', 'rb') as f:
#    with open('../dataset.pickle', 'rb') as f:
        df = pickle.load(f)  
    embs,labels,doc_names,langs,texts = nlp.prepare_collection(df)
    index = nlp.build_index(embs,300)
    
    APP.debug=False
    APP.run()