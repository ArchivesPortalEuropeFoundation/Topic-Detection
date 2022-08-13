import os.path as path
import sys

level_up = path.abspath(path.join(__file__, "../../../"))

sys.path.insert(0, level_up)

from utils import nlp


def test_get_url():
    page, url, site = nlp.get_url("Barack Obama", "en")
    assert url == "https://en.wikipedia.org/wiki/Barack_Obama"


def test_get_candidates():
    cands, url = nlp.get_candidates("Barack Obama", "en", "en", False)
    assert len(cands) > 0 and url == "https://en.wikipedia.org/wiki/Barack_Obama"


def test_get_redirect():
    page, url, site = nlp.get_url("Coriolanus", "de")
    assert nlp.check_redirect(page, "de", site) != False

    page, url, site = nlp.get_url("sajlaksdjalkds", "de")
    assert nlp.check_redirect(page, "de", site) == False


def test_get_entity():
    url = nlp.get_entity("Barack Obama", "en")
    assert url == "https://en.wikipedia.org/wiki/Barack_Obama"

    url = nlp.get_entity("asjdkasdhakd", "en")
    assert url == None
