from func.func import *

def main():
    prepareFolder(inPath="pdfs")
    extractInfo()

    extractAbstract()
    getCitations()
    getAuthors()

    print('main')

if __name__=="__main__":
    main()