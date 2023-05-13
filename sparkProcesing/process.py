import pyspark
from pyspark import SparkContext
import os
import nltk
stopwords=nltk.corpus.stopwords.words('english')
from nltk import PorterStemmer
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from gensim.models import LdaMulticore, CoherenceModel
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
from gensim.similarities import MatrixSimilarity
import matplotlib.pyplot as plt
import pandas as pd

def remove_punct(text):
    return ("".join([ch for ch in text if ch not in string.punctuation]))

def tokenize(text):
    text = re.split('\s+' ,text)
    return [x.lower() for x in text]

def remove_stopwords(text, stopwords):
    return [word for word in text if word not in stopwords]

def process_document(doc):
    doc = [documents for documents in doc if documents!=["None"]]
    doc = remove_punct(doc)
    tokens = tokenize(doc)
    tokens = [word for word in tokens if len(word) > 3]
    tokens = remove_stopwords(tokens, stopwords)
    return tokens

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = LdaMulticore(corpus=corpus, num_topics=num_topics, id2word=dictionary, random_state=100)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values

def main():
    sc = SparkContext("local", "CargarArchivos")
    folerPath=os.popen(f"ls | grep \"out_\" | tail -n 1").read().replace("\n", "")
    abstracts=sc.textFile(f"{folerPath}/*_abstract.txt", minPartitions=30)

    documents = abstracts.map(process_document)

    documentList=documents.collect()
    documents_str_list = [' '.join(doc) for doc in documentList]

    vectorizer=TfidfVectorizer()
    documentsAsVectors=vectorizer.fit_transform(documents_str_list)

    similarity_matrix = cosine_similarity(documentsAsVectors)

    clustering = AgglomerativeClustering(n_clusters=3, affinity='cosine', linkage='complete')
    labels = clustering.fit_predict(similarity_matrix)

    df = pd.DataFrame({'document': documents_str_list, 'cluster': labels})
    print(df)
    
    id2word = Dictionary(documentList)
    corpus = [id2word.doc2bow(text) for text in documentList]

    lda_model = LdaMulticore(
        corpus=corpus,             # Suministra el corpus
        id2word=id2word,           # Suministra el diccionario
        num_topics=3,              # Define el número de temas
        random_state=100,          # Establece una semilla para la reproducibilidad
        chunksize=100,             # Número de documentos a considerar en cada iteración
        passes=10,                 # Número de pasadas a través del corpus durante el entrenamiento
        per_word_topics=True       # Calcula las distribuciones de tema por palabra
    )

    # Imprimir los temas y sus palabras más representativas
    coherence_model_lda = CoherenceModel(
        model=lda_model, 
        texts=documentList, 
        dictionary=id2word, 
        coherence='c_v')

    coherence_lda = coherence_model_lda.get_coherence()
    i=0
    for idx, topic in lda_model.print_topics(-1):
        print('Tema: {}: \nPalabras: {}'.format(idx, topic))
        i+=1

    print(similarity_matrix)

if __name__=="__main__":
    main()