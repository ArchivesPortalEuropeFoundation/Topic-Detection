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

    return flask.render_template('my-form.html',langs=langs)

@APP.route('/my-form', methods=['POST'])
def my_form_post():

    # we load the dataset

    text = flask.request.form['text']
    lang = flask.request.form['lang']
    n_res = int(flask.request.form['n_res'])
    query_emb = nlp.text_embedding(text,lang)
    ranking= nlp.search(index,query_emb,labels,doc_names,texts,n_res)
    if query_emb:
        query_emb = " ".join([str(x) for x in query_emb])
    else:
        query_emb = "nope"
    return flask.render_template('my-form.html',  tables=[ranking.to_html(classes='data')], titles=ranking.columns.values)

if __name__ == '__main__':

    # we load the dataset
    with open('data/sample_dataset.pickle', 'rb') as f:
#    with open('../dataset.pickle', 'rb') as f:
        df = pickle.load(f)  
    embs,labels,doc_names,langs,texts = nlp.prepare_collection(df)
    index = nlp.build_index(embs,300)
    
    APP.debug=False
    APP.run()