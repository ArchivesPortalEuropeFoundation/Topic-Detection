### 1. Add Taxonomies
Download the taxonomies for each topic from [here](https://drive.google.com/drive/folders/14t87V9MImkowDxGd0MGNMURz_KKpnrOR?usp=sharing) and add them to a `Taxonomies/` folder.

### 2. Topic Classification
Open the notebook named `CrossLingualClassification.ipynb`. To retrain the model, run each cell following the inline comments. If you plan to use the pretrained model for classifying new texts, you can use the last cell. You need to have a trained_topic_classifier.model in the same folder, that can be downloaded from here.

### 3. Information Retrieval
Open the notebook named `InformationRetrieval.ipynb`. Run all cells to load the dataset, the embeddings and to be able to match a query in a given language to documents and topic-words in other languages.
