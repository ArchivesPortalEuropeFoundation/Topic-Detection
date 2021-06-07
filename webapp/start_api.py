import flask
import pickle
from utils import nlp
from argparse import ArgumentParser

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

    text = flask.request.args['text']
    lang = flask.request.args['lang']
    search_type = flask.request.args['type']
    n_res = int(flask.request.args['n_res'])
    if search_type == "concept":
        query_emb = nlp.text_embedding(text,lang,model_dict)
        if query_emb:
            ranking= nlp.concept_search(index,query_emb,labels,doc_names,texts,n_res)
            response = ranking.to_html(classes='data',index=False)
        else:
            response= "Concept not found in embedding space!"

    if search_type == "entity":
        #for the moment hardcoded
        allow_partial_match = True
        ranking = nlp.entity_search(text,lang,labels,doc_names,texts,n_res,langs,allow_partial_match)
        if ranking.empty:
            response =  "Entity mentions not found in corpus!"
        else:
            response = ranking.to_html(classes='data',index=False, id = "results')

    html = html.replace("<table></table>",response)

    return html


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
    APP.run()
