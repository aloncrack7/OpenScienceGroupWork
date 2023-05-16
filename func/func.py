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
time=str(datetime.time(datetime.now())).replace(":", "")
folderPath=f'out_{date}_{time}'

def prepareFolder(dir=folderPath, inPath="papers"):
    oldDircetory=os.popen(f"ls | grep \"out_\" | tail -n 1").read().replace("\n", "")
    os.system(f"mkdir {dir}")
    # loadedPapers=[]

    # if oldDircetory!='' and oldDircetory!='out_container':
    #     with open(f"{oldDircetory}/loadedPapers.txt") as file:
    #         loadedPapers = [line.rstrip() for line in file]

    for requestPaper in os.listdir(inPath):
        fileName=re.sub(r"\.[^$]*", "", requestPaper)
        # TODO USE symbolic links
        # if fileName in loadedPapers:
        #     print(f"ln -s ./{oldDircetory}/{fileName}.tei.xml ./{folderPath}/{fileName}.tei.xml")
        #     os.system(f"ln -s ./{oldDircetory}/{fileName}.tei.xml ./{folderPath}/{fileName}.tei.xml")
        # else: 

        filePath=re.sub(r" ", "\\ ", f"{inPath}/{requestPaper}", 0)
        os.system(f"cp {filePath} {dir}")

        # os.system(f"echo {fileName} >> {dir}/loadedPapers.txt")

    print('Prepare folder')

# Ask the server to process the .pdf  
def extractInfo(dir=folderPath):
    client.process("processFulltextDocument", dir, n=10)
    os.system(f"rm {dir}/*.pdf")
    print('extract info')

# Get the abstract of every paper
def extractAbstract(dir=folderPath, outPath=None):
    teis=os.listdir(dir)

    for i in teis:
        if not i.endswith(".txt"):
            filePath = f'{dir}/{i}'
            outPath = f'{dir}/{i}' if outPath==None else f"{outPath}/{i}"
            with open(filePath, 'r') as xmlFile:
                doc=gtx.parse_document_xml(xmlFile.read())

                with open(f"{filePath}_abstract.txt", 'w') as abstractFile:
                    abstract=str(doc.abstract)
                    if abstract!=None:
                        abstractFile.write(str(doc.abstract))

    print('Extract abstract')


def getCitations(dir=folderPath, outPath=None):
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

            filePath = f"{dir}/{i}_reference.txt" if outPath==None else f"{outPath}/{i}_reference.txt"
            with open(filePath, 'w') as referenceFile:
                referenceFile.write(str(links))

    print("Citations")

def getAuthors(dir=folderPath, outPath=None):
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
                forename=str(j.find("forename"))
                if forename=="None": forename='><'
                surname=str(j.find("surname"))
                if surname=="None": surname='><'
                author=re.findall(r">(.*?)<", forename)[0] +' '+re.findall(r">(.*?)<", surname)[0]
                
                authorWithOrgs=[]
                affiliation=j.find("affiliation")
                if affiliation!=None:
                    orgList=affiliation.find_all("orgName")
                    for k in orgList:
                        authorWithOrg=author+": "+re.findall(r">(.*?)<", str(k))[0]
                        authorWithOrgs.append(authorWithOrg)
                    
                    authors.append(authorWithOrgs)

            filePath = f"{dir}/{i}_authors.txt" if outPath==None else f"{outPath}/{i}_authors.txt"
            with open(filePath, 'w') as authorsFile:
                authorsFile.write(str(authors))

    print("Authors") 
