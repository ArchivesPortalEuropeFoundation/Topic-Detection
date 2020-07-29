# Topic-Detection
Using machine learning approaches for automatic topic detection in a multilingual environment.

Two main goals:

tagging documents that have no topic associated, with one of the pre-defined topics
given a user query, retrieve documents relevant for it

## Installation

### 1. Setup Environment

Clone the repository to a dedicated folder.

Download and Install [Anaconda](https://www.anaconda.com/products/individual). [Jupyter](https://jupyter.org/) will come directly with it.

Open Jupyter (as described in [here](https://jupyter.readthedocs.io/en/latest/running.html)) and browse to the cloned folder.

### 2. Download Cross-Lingual Word Embeddings

Download all the cross-lingual word embeddings of the languages you are planning to work with from [here](https://github.com/facebookresearch/MUSE#multilingual-word-embeddings). The current size is 4GB for seven languages. Move them inside the word-embs folder (its content is not synced with github to avoid storing large word embeddings).

### 3. Build a Machine Readable Dataset.

The script `AggregateJsons.ipynb` will combine all jsons derived from the database in a single dataset.pickle file. You can collect the .jsons we used from [here](https://drive.google.com/drive/folders/1U9jZIhS-yyoqfPea4rG1kcnc37bNk3vK?usp=sharing). To 
run, you need to put the .json files in a common `data/` folder. A version of the .pickle file is downloadable from [here](https://drive.google.com/file/d/1EQ8Ci3zzLZf9vpKz0tHt5o7moI4gtWrZ/view?usp=sharing). To use the pickle file, just position it in the same cloned folder.

### 4. Add Taxonomies

Download the taxonomies for each topic from [here](https://drive.google.com/drive/folders/14t87V9MImkowDxGd0MGNMURz_KKpnrOR?usp=sharing) and add them to a `Taxonomies/` folder.

## Topic Classification

Open the notebook named `CrossLingualClassification.ipynb`. To retrain the model, run each cell following the inline comments. If you plan to use the pretrained model for classifying new texts, you can use the last cell. You need to have a `trained_topic_classifier.model` in the same folder, that can be downloaded from here.

## Information Retrieval

Open the notebook named  `InformationRetrieval.ipynb`. Run all cells to load the dataset, the embeddings and to be able to match a query in a given language to documents and topic-words in other languages.

