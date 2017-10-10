from lxml import etree as et
from bz2file import BZ2File
import string
from contextlib import closing
import json
import re
import time

# Select all the articles which title begins with an "a" or an "A"
articles_by_file = {}
set_files = []
letter_start = 'a'

with open('CleanArticles2/referenceDictionnary.json')  as f:
        refDic = json.load(f)
        
for dic_key in refDic.keys():
    if dic_key.lower()[0] == letter_start:
        articleIndice = refDic[dic_key][0]
        fileIndice = refDic[dic_key][1]
        print(fileIndice)
        set_files.append(fileIndice)
        if fileIndice in articles_by_file.keys():
            articles_by_file[fileIndice].append(articleIndice)
        else:
            articles_by_file[fileIndice] = list([articleIndice])

set_files = list(set(set_files))

with open('articles_by_file.json', 'w') as f:
    json.dump(articles_by_file, f)

with open('set_files.json', 'w') as f:
    json.dump(set_files, f)
    

