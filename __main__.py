from func.func import *
import os

def main():
    prepareFolder(inPath="pdfs")
    extractInfo()

    extractAbstract(outPath="out")
    getCitations(outPath="out")
    getAuthors(outPath="out")

    print('main')

    os.system("ya2ro -i /home/root/Research_Object.yaml -o ./out")

if __name__=="__main__":
    main()