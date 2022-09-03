# Cross-lingual Search and Multi-Lingual Topic Detection on Archives Portal Europe

This repository contains the resources and code used to build:
- [a cross-lingual search tool](https://www.archivesportaleurope.net/topicdetection/) and
- [a multi-lingual topic detection tool](https://www.archivesportaleurope.net/topicdetection/detect.html)

for [Archives Portal Europe](https://www.archivesportaleurope.net/). It relies on the use of cross-lingual word embeddings and entity linking technologies.

-----

## Codebase overview

The code base has three main components:

- the preprocessing scripts
- the interface
- the NLP backend 

### The Preprocessing Scripts

The [`preprocessing`](preprocessing/) folder contains a series of scripts used at the beginning of the project to produce the dataset and to explore the collection.

### The interface

The [interface](interface/) folder contains the element for setting up the front-end, which relies on php to collect the query of the user.

### The NLP backend

The tool has been developed as a Flask webapp, which communicates at port `5000` and given a user query returns a HTML table with the results. The tool offers two main options:
- `query_api`: this is the cross-lingual information retrieval tool. The main functions are inside [utils/nlp.py](utils/nlp.py)
- `detector`:  this is the multi-lingual entity and concept detection tool. The main functions are inside [utils/detect.py](utils/detect.py)

-----

## Development

If you want to extend the functionalities of the NLP tool, the Python backend can be set up locally using the following instructions.

### The Environment

To start, download and Install [Anaconda](https://www.anaconda.com/products/individual).

Create a dedicated Python environment:

`conda create -n py37ape python=3.7`

`conda activate py37ape`

Run `pip install -r requirements.txt` to install the requirements.

### Download Cross-Lingual Word Embeddings

Download all the cross-lingual word embeddings of the languages you are planning to work with from [here](https://github.com/facebookresearch/MUSE#multilingual-word-embeddings). Move them inside the `webapp/word-embs` folder (its content is not synced with github to avoid storing large word embeddings). Note that if a multilingual word embedding is not available for a specific language you can generate it using the available [bilingual dictionary](https://github.com/facebookresearch/MUSE#ground-truth-bilingual-dictionaries) and following the documentation for [supervised learning](https://github.com/facebookresearch/MUSE#align-monolingual-word-embeddings), however bear in mind that the process is not straightforward.

### Start the API   

In the [webapp/data/](`webapp/data/`) folder we have added sample versions of the resources needed. Full version of them are available on the project server and scripts to recreate them are available inside the [preprocessing/generateDataset/](preprocessing/generateDataset/) folder.

When the embeddings have been downloaded, to start the API you should run `start_api.py` inside the `webapp` folder. To test that the API is running properly you can send a `curl` request at the `5000` port, for instance: 

```
curl -s -X GET 'http://0.0.0.0:5000/detect?lang=en&query=Mark+lives+in+Washington+with+his+family
```
You should receive as a response an HTML table with the result of the `detect` tool.

-----

## Server Deployment

### Docker

The `dev` branch of the repository currently sits inside this folder: `/data/containerdata/topic-detection` in our dedicated server. In the same folder we have the `volumes` folder, which host the full versions of the `data` and `word-embs` folders (instead of only the sample data that we host in the repo).

We have two Docker images, one for the web interface (we call it `webapp`) and one for the python code (we call it `backend`). To deploy the full version of the tool, you need to copy the the [config folder](config/) to the `volumes` folder and change the test flag to `False` in the copied `config.env` file. In the same file you can change the endpoint to `http://topic-detection-webapp:5000`.

After that, to build and start the docker containers, you should run the scripts inside the [deployment](deployment/) folder in the following order:

```
./docker-build-backend.sh
./docker-run-backend.sh
./docker-run-webapp.sh
```
To check the status of the running script you can use `docker logs -f topic-detection-backend`
