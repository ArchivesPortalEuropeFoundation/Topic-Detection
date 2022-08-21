from flask_table import Table, Col
class Results(Table):
    filename = Col('filename', show=False)
    texts = Col('texts', show=False)
    cs = Col('cossim', show=False)
