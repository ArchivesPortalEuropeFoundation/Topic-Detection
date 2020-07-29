# Topic-Detection
Using machine learning approaches for automatic topic detection in a multilingual environment.

## Installation

### 1. Setup Environment

Clone the repository to a dedicated folder.

Download and Install [Anaconda](https://www.anaconda.com/products/individual). [Jupyter](https://jupyter.org/) will come directly with it.

Open Jupyter (as described in [here](https://jupyter.readthedocs.io/en/latest/running.html)) and browse to the cloned folder.

### 2. Download Cross-Lingual Word Embeddings

Download all the cross-lingual word embeddings of the languages you are planning to work with from [here](https://github.com/facebookresearch/MUSE#multilingual-word-embeddings). The current size is 4GB for seven languages. Move them inside the word-embs folder (its content is not synced with github to avoid storing large word embeddings).

### 3. Build a Machine Readable Dataset.

The script `AggregateJsons.ipynb` will combine all jsons derived from the database in a single dataset.pickle file. To 
run, you need to put the .json files in a common `data\` folder. A version of the .pickle file is downloadable from [here}(https://drive.google.com/file/d/1EQ8Ci3zzLZf9vpKz0tHt5o7moI4gtWrZ/view?usp=sharing).


## Topic Classification

Open the notebook named `CrossLingualClassification.ipynb`. To retrain the model, run each cell following the inline comments. If you plan to only use the model for classifying new texts, just go to the last cell.
