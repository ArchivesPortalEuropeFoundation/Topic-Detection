import flask

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
    processed_text = text.upper()
    return processed_text

if __name__ == '__main__':
    APP.debug=False
    APP.run()