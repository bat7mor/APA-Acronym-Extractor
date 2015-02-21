import re
import pdfminer 
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfparser import PDFSyntaxError
import slate
import sys
import subprocess

def get_acronyms(file_name):
    try:
        fname = file_name.replace(".pdf", "_acronyms.txt")
        acronyms = open(fname, 'w')
        articleToParse = open(file_name)
        parsedArticle = slate.PDF(articleToParse)

        textArticle = " ".join(parsedArticle)
        
        pattern = "[(][A-Z]+[)]" 

        acronymIndices = [(m.start(0), m.end(0)) for m in re.finditer(pattern, textArticle)]

        for item in acronymIndices: 
            if (item[1] - item[0] > 3): 
                splitPiece = textArticle[item[0] - 100: item[1]].split(" ")
                numWords = item[1] - item[0] - 1
                segment = splitPiece[-numWords:]
                acronyms.write(segment[-1] + " = " + " ".join(segment[0:-1]) + "\n") 

        subprocess.call(['open', '-a', 'TextEdit', fname])

    except PDFSyntaxError as e:
        print "Error with file: " + file_name + ": " + str(e)


file_name = sys.argv[1]
get_acronyms(file_name)
