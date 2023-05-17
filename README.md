# OpenScienceGroupWork
Repo for Open Science subject: Group Work
Objective: Advanced data analysis on research publications: Given a corpus of 30
papers, group them according common themes, link them in a Research Knowledge
Graph (RKG) together with their metadata and funding information. Use
HuggingFace as an open platform for models.
- Data processing 
- Topic modeling on your chosen papers
- Similarity score between papers (based on abstract)
- NER models in the Acknowledgements section
- Experiment as a Research Object
This software will run mostly in Python, so you should have installed python and pip
# Data processing 
Execute the file func.py on https://github.com/aloncrack7/OpenScienceGroupWork/blob/main/func/func.py
For this part you need to install via pip:
-Pyspark
-bs4
-matplotlib
-pandas
And get all the 30 papers in the same directory as the script.
# Topic Modeling and similarity score
Execute the file process.py on https://github.com/aloncrack7/OpenScienceGroupWork/blob/main/sparkProcesing/process.py
For this part you need to install via pip:
-Pyspark
-ntlk
-sklearn
-gensim
-matplotlib
-pandas
All the papers will be processed using clustering techniques in order to know their similarity
#  NER models in the Acknowledgements section
We have processed the papers with the Roberta NER Model https://huggingface.co/Jean-Baptiste/roberta-large-ner-english, and you have the results on https://github.com/aloncrack7/OpenScienceGroupWork/blob/main/Name%20Entity%20Recognition/NER%20model%20Task.pdf
You can use the API just like is done in the PDF.
# Experiment as a Research Object
We have used this repo in order to process and create a Research Object:
dgarijo(17/05/2023). ya2ro [Generator of Research Object]. doi:10.5281/zenodo.7803628
We have used https://github.com/aloncrack7/OpenScienceGroupWork/tree/main/ya2ro .yaml files to configure and create the Research Object, you can follow the same steps looking the repo attached.

# Run it
**Make sure all the files are in LF insted of CRLF**
- Change the name of ./ya2ro/propertiesWithOutKey.yaml to ./ya2ro/properties.yaml and add your personal access key.
- Add your papers to ./pdfs folder
- Build and run, -d flag is optional.
```bash
docker compose up --build
```

- Run, -d flag is optional.
```bash
docker compose up 
```

- The outputs would appear in out_container
  - The information about the papers.
  - The research object.
