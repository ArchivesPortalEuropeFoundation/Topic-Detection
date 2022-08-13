# Deployment & Development Instructions

## Docker

Remember to update `config.env` inside `volumes` folder.

```
./docker-build-backend.sh
./docker-run-backend.sh
docker logs -f topic-detection-backend
```

## Python

### 1. Setup Environment

Clone the repository to a dedicated folder.

Download and Install [Anaconda](https://www.anaconda.com/products/individual).

Open the terminal and go to the repository folder (using `cd` and the path to the folder). For instance: `cd /Users/fnanni/Projects/Topic-Detection/`

Create a dedicated Python environment:

`conda create -n py37ape python=3.7`

`conda activate py37ape`

Run `pip install -r requirements.txt`

### 2. Download Cross-Lingual Word Embeddings

Download all the cross-lingual word embeddings of the languages you are planning to work with from [here](https://github.com/facebookresearch/MUSE#multilingual-word-embeddings). Move them inside the `webapp/word-embs` folder (its content is not synced with github to avoid storing large word embeddings). Note that if a multilingual word embedding is not available for a specific language you can generate it using the available [bilingual dictionary](https://github.com/facebookresearch/MUSE#ground-truth-bilingual-dictionaries) and following the documentation for [supervised learning](https://github.com/facebookresearch/MUSE#align-monolingual-word-embeddings), however bear in mind that the process is not straightforward.
