import pyspark
from pyspark import SparkContext
import os
import nltk
stopwords=nltk.corpus.stopwords.words('english')
from nltk import PorterStemmer
import string
import re

def remove_punct(text):
    return ("".join([ch for ch in text if ch not in string.punctuation]))

def tokenize(text):
    text = re.split('\s+' ,text)
    return [x.lower() for x in text]

def remove_stopwords(text, stopwords):
    return [word for word in text if word not in stopwords]

def main():
    sc = SparkContext("local", "CargarArchivos")
    folerPath=os.popen(f"ls | grep \"out_\" | tail -n 1").read().replace("\n", "")
    abstracts=sc.textFile(f"{folerPath}/*abstract.txt", minPartitions=30)
    abstractsNoPuntuation=abstracts.map(lambda x: remove_punct(x))
    abstractsTokens=abstractsNoPuntuation.map(lambda x: tokenize(x))
    abstractsNoSmallWords=abstractsTokens.map(lambda x: [word for word in x if len(word)>3])
    abstractsNoStopWords=abstractsNoSmallWords.map(lambda x: remove_stopwords(x, stopwords))

    for content in abstractsNoStopWords.collect():
        print(content)

if __name__=="__main__":
    main()