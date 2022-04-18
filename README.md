# Topic-Detection
Using machine learning approaches for automatic topic detection and retrieval in a multilingual environment.

Two main goals:
* tagging documents that have no topic associated, with one of the pre-defined topics
* given a user query, retrieve documents relevant for it

A public version of the tool in its current alpha state is available [here](http://topicdetection.archivesportaleurope.net/).


## Installation

### 0. Setup on our dedicated server

The `dev` branch of the repository currently sit inside this folder: `/data/containerdata/topic-detection` in our dedicated server. In the same folder we have the `volumes` folder, which host the full versions of the `data` and `word-embs` folders (instead of only the sample data that we host in the repo).

We have two Docker images, one for the web interface (we call it `webapp`) and one for the python code (we call it `backend`). To deploy the full version of the tool, you need to change in the [config file](config/config.env) the test flag to `False`. In the same file you can change the endpoint to `http://topic-detection-webapp:5000`.

To build the `backend` image you should run: 
```
docker build -t topic-detection:prod .
```
Then you can start the container as:
```
docker run -d --name topic-detection-backend -p 10.32.34.167:8091:5000 -v /data/containerdata/topicdetection/volumes/data:/webapp/data -v /data/containerdata/topicdetection/volumes/word-embs:/webapp/word-embs --network=ape --restart unless-stopped topic-detection:prod
```
The container will take some time to run - you can test that all runs properly by running `pytest`.

We deploy the second image, for the `webapp` as following:
```
docker run -d --name topic-detection-webapp -p 10.32.34.167:8090:80 -v /data/containerdata/topicdetection/Topic-Detection/interface:/var/www/html --network=ape --restart unless-stopped php:7.3-apache
```

The name of the container is topic-detection-webapp and is exposes the internal port of `80` to the external port `8090` on the host machine. Finally we map the port to `http://topicdetection2.archivesportaleurope.net/` 

### 1. Setup Environment

Clone the repository to a dedicated folder.

### 2. Docker Setup

Download and Install [Anaconda](https://www.anaconda.com/products/individual).

Open the terminal and go to the repository folder (using `cd` and the path to the folder). For instance: `cd /Users/fnanni/Projects/Topic-Detection/`

Create a dedicated Python environment:

`conda create -n py37ape python=3.7`
`conda activate py37ape`

Run `pip install -r requirements.txt`

### 2. Download Cross-Lingual Word Embeddings

Download all the cross-lingual word embeddings of the languages you are planning to work with from [here](https://github.com/facebookresearch/MUSE#multilingual-word-embeddings). Move them inside the `webapp/word-embs` folder (its content is not synced with github to avoid storing large word embeddings). Note that if a multilingual word embedding is not available for a specific language you can generate it using the available [bilingual dictionary](https://github.com/facebookresearch/MUSE#ground-truth-bilingual-dictionaries) and following the documentation for [supervised learning](https://github.com/facebookresearch/MUSE#align-monolingual-word-embeddings), however bear in mind that the process is not straightforward.

---

Below you can also find the installation instructions for the previous proof-of-concept version of the tool.

## Installation of the proof-of-concept version of tool
### 1. Setup Environment
Clone the repository to a dedicated folder.

Download and install [Anaconda](https://www.anaconda.com/products/individual). [Jupyter](https://jupyter.org/) will come directly with it.

Open the terminal and go to the repository folder (using `cd` and the path to the folder). For instance: `cd /Users/fnanni/Projects/Topic-Detection/`

Run `pip install -r requirements.txt`

Open Jupyter (as described in [here](https://jupyter.readthedocs.io/en/latest/running.html)) and browse to the cloned folder.

### 2. Download Cross-Lingual Word Embeddings
Download all the cross-lingual word embeddings of the languages you are planning to work with from [here](https://github.com/facebookresearch/MUSE#multilingual-word-embeddings). The current size is 4GB for seven languages. Move them inside the word-embs folder (its content is not synced with github to avoid storing large word embeddings).

### 3. Build a Machine Readable Dataset.
The script`AggregateJsons.ipynb` will combine all jsons derived from the database in a single dataset.pickle file. You can collect the .jsons we used from [here](https://drive.google.com/drive/folders/1U9jZIhS-yyoqfPea4rG1kcnc37bNk3vK?usp=sharing). To run, you need to put the .json files in a common `data/` folder. A version of the .pickle file is downloadable from [here](https://drive.google.com/file/d/1EQ8Ci3zzLZf9vpKz0tHt5o7moI4gtWrZ/view?usp=sharing). To use the pickle file, just position it in the same cloned folder.

### 4. Add Taxonomies
Download the taxonomies for each topic from [here](https://drive.google.com/drive/folders/14t87V9MImkowDxGd0MGNMURz_KKpnrOR?usp=sharing) and add them to a `Taxonomies/` folder.

### 5. Topic Classification
Open the notebook named CrossLingualClassification.ipynb. To retrain the model, run each cell following the inline comments. If you plan to use the pretrained model for classifying new texts, you can use the last cell. You need to have a trained_topic_classifier.model in the same folder, that can be downloaded from here.

### 6. Information Retrieval
Open the notebook named InformationRetrieval.ipynb. Run all cells to load the dataset, the embeddings and to be able to match a query in a given language to documents and topic-words in other languages.
