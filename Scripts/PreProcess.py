# Script description:
# This script takes as input the 'enwiki-20170820-pages-articles-multistream.xml.bz2' file.
# It contains all content from the english wikipedia.
# Thanks to the iterparse function, the xml file is read tag by tag.
# The text tags corresponding to an article (ns !=0) and the one than are not
# #REDIRECT are cleaned and saved.

# The articles are saved into dictionnaries of a given length (corresponding to a fix number of articles)
# The keys of the dictionnaries correspond to the id of the articles.
# The values correspond to the text of each article.
# A referencesDictionnary is also created. 
# Its keys correspond to the title of the articles.
# Its values are lists containing the id of the articles and the number of the dictionary in which they are stored.

########################################################################################################################

from lxml import etree as et
from bz2file import BZ2File
import string
from contextlib import closing
import shelve
import json
import sys
import time

# Little function that put all the letter of a text in lower case and convert 
# all breaks line into spaces

def text_cleaning(text):
    text = text.lower()
    cleanText = text.replace('\n', ' ')
    return(cleanText)

articleInFileNumberLimit = 50000  # Number of articles saved in each file

path = "/Users/antoine/Documents/Python/Computanional tools for big data/Challenge 1/enwiki-20170820-pages-articles-multistream.xml.bz2"

# Indices initialization
articleIndice = 0
titleIndice = 0
totalIndice = 0
fileIndice = 0
idIndice = 0
articleInFileNumber = 0

articlesDictionnary = {}
referenceDictionnary = {}

start_time = time.time()
with BZ2File(path) as xml_file:
    parser = et.iterparse(xml_file, events=('end',))
    for events, elem in parser:

        # If the number of article in one file reach the num articleInFileNumberLimit,
        # The current file is saved and a new file is created
        if articleInFileNumber == articleInFileNumberLimit:

            fileName = 'articlesDictionnary_' + str(fileIndice) +'.json'
            with open('CleanArticles2/' + fileName, 'w') as fp:
                json.dump(articlesDictionnary,fp)

            del text
            del cleanText
            del articlesDictionnary

            articlesDictionnary = {}
            articleInFileNumber = 0
            fileIndice += 1 

        if elem.tag =='{http://www.mediawiki.org/xml/export-0.10/}title':
            title = elem.text
            titleIndice += 1
            idIndice = 0 

        if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}ns':
            ns = elem.text   
            
        if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}id':
            if idIndice == 0:   # Only the ID tag after the text tag is saved
                idArticle = elem.text
                idIndice += 1
                
        if elem.tag =='{http://www.mediawiki.org/xml/export-0.10/}text':
            # If loop to make sure that there is a text tag correponding to the title tag
    
            if titleIndice > 1:
                print('Error: no text tag in the article')
                break

            text = elem.text

            if text is not None:
                # If the text is a #REDIRECT or not a ns = 0 type (which correspond to articles)
                # It is not taking into account
                if text[0:9].upper() != '#REDIRECT' and ns == str(0):
                    cleanText = text_cleaning(text)

                    articlesDictionnary[idArticle] = cleanText
                    referenceDictionnary[title] = [idArticle, fileIndice]

                    if articleIndice % 10000 == 0:
                        print("File folder: %(key1)s ; Article: %(key2)s ; Last ID: %(key3)s" % {'key1':fileIndice, 'key2':articleIndice, 'key3':idArticle})
                        print("--- %s seconds ---" % (time.time() - start_time))
                    articleInFileNumber += 1
                    articleIndice += 1

            titleIndice = 0
            totalIndice += 1

        # After each tag assesment, the element is deleted in order to save the memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

fileName = 'articlesDictionnary_' + str(fileIndice) + '.json'
with open('CleanArticles2/' + fileName, 'w') as fp:
    json.dump(articlesDictionnary,fp)
        
# The reference dictionnary is created saved at the end of the script
fileName = 'referenceDictionnary' + '.json'
with open('CleanArticles2/' + fileName, 'w') as fp:
    json.dump(referenceDictionnary,fp)
