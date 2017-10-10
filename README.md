# bigdata-challenge1
Repository for the challenge 1 of the course Big data 02807

The Python scripts consist in 4 different scripts:

  - PreProcess.py : Open the bz2-compressed XML file little by little and compute some preprocessing on the text. Store the titles and the texts of the articles in 110 json files of 50 000 articles each
  - query.py : Main script that runs the query-search on all the articles of the English Wikipedia and store the results in a txt file, containing the number of matches and results.
  - query_A_articles : Run the query search on only articles which title begins with an "a" or an "A"
  - selection_A_articles : Select all the ids of the articles (and the file there are in) which title begins with an "a" or an "A"
  
 
The query results can be found in the folder and contains the 15 validation queries: 5 on only one article cat, 5 on all the "A-articles" and 5 on all the English wikipedia.
