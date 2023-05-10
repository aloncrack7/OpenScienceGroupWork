import os
try:
    from grobid_client_python.grobid_client.grobid_client import GrobidClient
except:
    if not os.path.isdir("grobid_client_python"):
        os.system("git clone git@github.com:kermitt2/grobid_client_python.git")
    
    os.system("python3 grobid_client_python/setput install") 

    from grobid_client_python.grobid_client.grobid_client import GrobidClient
from grobid_client_python.grobid_client.grobid_client import GrobidClient 
import re
from datetime import datetime
import pandas as pd
import numpy as np
import grobid_tei_xml as gtx
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs 

# Inicialize client and get the output folder for the .tei
client = GrobidClient(config_path="./config.json")
print('Conection')
date=datetime.date(datetime.now())
time=datetime.time(datetime.now())
folderPath=f'out_{date}_{time}'

def prepareFolder(dir=folderPath, inPath="papers"):
    oldDircetory=os.popen(f"ls | grep \"out_\" | tail -n 1").read().replace("\n", "")
    os.system(f"mkdir {dir}")
    loadedPapers=[]

    if oldDircetory!='' and oldDircetory!='out_container':
        with open(f"{oldDircetory}/loadedPapers.txt") as file:
            loadedPapers = [line.rstrip() for line in file]

    for requestPaper in os.listdir(inPath):
        fileName=re.sub(r"\.[^$]*", "", requestPaper)
        # TODO USE symbolic links
        # if fileName in loadedPapers:
        #     print(f"ln -s ./{oldDircetory}/{fileName}.tei.xml ./{folderPath}/{fileName}.tei.xml")
        #     os.system(f"ln -s ./{oldDircetory}/{fileName}.tei.xml ./{folderPath}/{fileName}.tei.xml")
        # else: 

        filePath=re.sub(r" ", "\\ ", f"{inPath}/{requestPaper}", 0)
        os.system(f"cp {filePath} {dir}")

        os.system(f"echo {fileName} >> {dir}/loadedPapers.txt")

    print('Prepare folder')

# Ask the server to process the .pdf  
def extractInfo(dir=folderPath):
    client.process("processFulltextDocument", dir, n=10)
    os.system(f"rm {dir}/*.pdf")
    print('extract info')

# Get the abstract of every paper
def extractAbstract(dir=folderPath):
    teis=os.listdir(dir)

    for i in teis:
        if not i.endswith(".txt"):
            filePath=f'{dir}/{i}'
            with open(filePath, 'r') as xmlFile:
                doc=gtx.parse_document_xml(xmlFile.read())

                with open(f"{filePath}_abstract.txt", 'w') as abstractFile:
                    abstractFile.write(str(doc.abstract))

    print('Extract abstract')

# Generates word cloud 
def generateWordCloud(text):
    wordCloud = WordCloud(collocations = False, background_color = 'white').generate(text)
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('./out/wordcloud.png')
    plt.close()
    print('WordCloud')

def countFigures(dir=folderPath):
    teis=os.listdir(f"{dir}")

    counts=[0]*(len(teis)-1)
    pos=0
    for i in range(0, len(teis)):
        if not teis[i].endswith(".txt"):
            counts[pos]=int(os.popen(f"grep -o '<figure xmlns=' {dir}/{teis[i]} | wc -l").read().replace('\n', ''))
            pos+=1

    print('count figures')
    return counts

def genHistogram(numFigures, dir=folderPath):
    plt.hist(numFigures, density=False)
    plt.ylabel("Number of figures")
    plt.xticks(numFigures, os.listdir(f"{dir}").remove("loadedPapers.txt"))
    plt.savefig('./out/histogram.png')
    print('Histogram')

def getCitations(dir=folderPath):
    teis=os.listdir(dir)

    for i in teis:
        if not i.endswith(".txt"):
            content = []
            with open(f"{dir}/{i}", "r", encoding="utf8") as file:
                content = file.readlines()
                content = "".join(content)
            #For some reason it only works using the html parser instead of lxml
            bs_content = bs(content, features="xml")

            references = bs_content.find_all("ptr")

            links=[]
            for j in references:
                links.append(j.get("target"))

            with open(f"{dir}/{i}_reference.txt", 'w') as referenceFile:
                referenceFile.write(str(links))

    print("Citations")

def getAuthors(dir=folderPath):
    teis=os.listdir(dir)

    for i in teis:
        if not i.endswith(".txt"):
            content = []
            with open(f"{dir}/{i}", "r", encoding="utf8") as file:
                content = file.readlines()
                content = "".join(content)
            #For some reason it only works using the html parser instead of lxml
            bs_content = bs(content, features="xml")

            authorsList = bs_content.find_all("author")

            authors=[]
            for j in authorsList:
                author=re.findall(r">(.*?)<", str(j.find("forename")))[0] +' '+re.findall(r">(.*?)<", str(j.find("surnname")))[0]
                
                authorWithOrgs=[]
                orgList=j.find_all("orgname")
                for k in orgList:
                    authorWithOrg=author+": "+re.findall(r">(.*?)<", k)[0]
                    authorWithOrgs.append(authorWithOrg)
                
                authors.append(authorWithOrgs)

            with open(f"{dir}/{i}_authors.txt", 'w') as authorsFile:
                authorsFile.write(str(authors))

    print("Authors") 
