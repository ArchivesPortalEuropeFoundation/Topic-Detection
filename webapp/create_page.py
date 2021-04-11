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
    return flask.render_template('my-form.html')

@APP.route('/my-form', methods=['POST'])
def my_form_post():
    text = flask.request.form['text']
    lang = flask.request.form['lang']
    n_res = flask.request.form['n_res']
    emb = nlp.text_embedding(text,lang)
    emb = " ".join([str(x) for x in emb])
    return emb

if __name__ == '__main__':

    # we load the dataset
    with open('data/dataset.pickle', 'rb') as f:
        df = pickle.load(f) 
    
    APP.debug=False
    APP.run()