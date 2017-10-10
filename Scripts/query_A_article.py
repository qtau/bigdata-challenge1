from lxml import etree as et
from bz2file import BZ2File
import string
from contextlib import closing
import json
import re
import time

# Recurrent function that returns all the positions of the last character for all the substrings that match the query
# starting at position.

def check_query_recurrence(query, text, position):
    # Condition to stop: if the query (it's a list) has only 1 element left (this last element should be a string)
    if len(query)==1:
        try:
            if query[0] == text[position:(position+len(query[0]))]:
                return set([position+len(query[0])])
            else:
                return -1
        except:
            return -1
    else:
        result = set()
        # if the first element of the query is a list ([2,4] for example), then we call the function as many times as there
        # are gaps (3 times in the example). And we return all the final positions.
        if isinstance(query[0], list):
            for i in range(query[0][0], query[0][1]+1):
                temp = check_query_recurrence(query[1:], text, position+i)
                if temp != -1:
                    result = result.union(temp)
            return result
        # Otherwise, if the first element of the query is a string, then we check if the sub-strings match and we continue
        # going through the query if yes.
        else:
            try:
                if query[0] == text[position:(position+len(query[0]))]:
                    temp = check_query_recurrence(query[1:], text, position+len(query[0]))
                    if temp != -1:
                        result = result.union(temp)
                    return result
                else:
                    return -1
            except:
                return -1

# Function that returns all the sub-strings that match the query in the string 'text'

def query_search(query, text):
    # Find all the positions of the first character, in the text.
    list_init_position = set([m.start() for m in re.finditer(query[0][0], text)])
    
    # Create a new query without the first character.
    new_query = []
    new_query.append(query[0][1:])
    new_query = new_query + query[1:]
    result = []

    # Loop on all the positions of the characters and return the positions of the corresponding final characters
    for position in list_init_position:
        position_temp = check_query_recurrence(new_query, text, position+1)
        if position_temp != -1:
            for pos_final in position_temp:
                result.append(text[position:pos_final])
    
    return result



timeQuery = 0
max_fichiers = 110 # To be changed with the number of files you have
nb_match = 0
nb_results = 0

query =   ['apache', [0, 100], 'software']

# The query can be written in the file
name_file = str(query) + '_articlesA.txt'

with open('CleanArticles2/articles_by_file.json') as f:
    articles_by_file = json.load(f)

with open('CleanArticles2/set_files.json') as f:
    set_files = json.load(f)

start_time = time.time()

# To go through all the files that begin with an "a/A"
nb_articles_tot = 0
for i_fichier in set_files:
    with open('CleanArticles2/articlesDictionnary_' + str(i_fichier) + '.json')  as f:
        print('Dictionnary open: Number ' + str(i_fichier) +' Matches: ' + str(nb_match))
        print("--- %s seconds ---" % (time.time() - start_time))
        dic = json.load(f)
        # Loop all the articles in the selected file
        startTimeTemp = time.time()
        
        for i_article in articles_by_file[str(i_fichier)]:
            # Find all the substrings that match in that article
            result = query_search(query, dic[i_article])
            
            # If the result is not null then we print/store it
            if bool(result):
                to_be_written = ''
                for match in result:
                    nb_match +=1
                    to_be_written += "%(key1)6s %(key2)9s %(key3)s \n" % {'key1':str(nb_match), 'key2':str(i_article), 'key3':match}

                #print(to_be_written)
                nb_results += 1
                # To write it in a textfile instead of just printing it:
                with open(name_file, 'a') as file_result:
                    file_result.write(to_be_written)
                    
        timeQuery += time.time() - startTimeTemp
        
with open(name_file, 'r+') as file_result:
    old = file_result.read()
    file_result.seek(0)
    to_be_written_final = "Got %d results and %d matches\n" % (nb_results, nb_match) 
    file_result.write(to_be_written_final + old)
        

                    
print('======== Execution terminated ========')
print("--- %s seconds including opening files ---" % (time.time() - start_time))
print("--- %s seconds NOT including opening files ---" % (timeQuery))
