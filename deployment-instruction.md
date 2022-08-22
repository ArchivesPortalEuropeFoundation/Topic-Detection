# Deployment & Development Instructions

## Overview

The code base has three main components:
- the NLP backend 
- the interface
- the preprocessing scripts.

### The Preprocessing Scripts

The [`preprocessing`](preprocessing/) folder contains a series of scripts used at the beginning of the project to produce the dataset and to explore the collection.

### The interface

The [interface](interface/) folder contains the element for setting up the front-end, which relies on php to collect the query of the user.

### The NLP backend

The tool has been developed as a Flask webapp, which communicates at port `5000` and given a user query returns a HTML table with the results. The tool offers two main options:
- `query_api`: this is the cross-lingual information retrieval tool. The main functions are inside [utils/nlp.py](utils/nlp.py)
- `detector`:  this is the multi-lingual entity and concept detection tool. The main functions are inside [utils/detect.py](utils/detect.py)


## Deployment

### Docker

Remember to update `config.env` inside `volumes` folder.

```
./docker-build-backend.sh
./docker-run-backend.sh
docker logs -f topic-detection-backend
```

## Development

If you want to extend the functionalities, the Python backend can be set up using the following instructions.

#### 1. The Environment

To start, download and Install [Anaconda](https://www.anaconda.com/products/individual).

Create a dedicated Python environment:

`conda create -n py37ape python=3.7`

`conda activate py37ape`

Run `pip install -r requirements.txt`

#### 2. Download Cross-Lingual Word Embeddings

Download all the cross-lingual word embeddings of the languages you are planning to work with from [here](https://github.com/facebookresearch/MUSE#multilingual-word-embeddings). Move them inside the `webapp/word-embs` folder (its content is not synced with github to avoid storing large word embeddings). Note that if a multilingual word embedding is not available for a specific language you can generate it using the available [bilingual dictionary](https://github.com/facebookresearch/MUSE#ground-truth-bilingual-dictionaries) and following the documentation for [supervised learning](https://github.com/facebookresearch/MUSE#align-monolingual-word-embeddings), however bear in mind that the process is not straightforward.
