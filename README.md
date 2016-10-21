## Introduction
Program created by Vincent Yeh 10/04/2016
A program to read a number of doc#.txt files and compute the tf*idf score of each word within the file and export the result into its respective doc#.csv file.

## Files
Input: folder with input doc#.txt files
Output: folder with output doc#.csv files
tfidf.py: python script

## Assumptions
Assuming all words are in ASCII
Assuming punctuations: , . ' " ] } \ etc are not necessary for tf*idf calculation
Assuming numbers in any form: 5 5.3 1/2 etc are not necessary for tf*idf calculation
Assuming each word is split by space: back end would be considered as 2 words, while back-end is considered 1 word
Assuming word with punctuations or numbers are considered words: tf-idf is considered, 2000s is considered
Assuming capitalization of only the first letter equates to the same word: Hello == hello, LaTeX != latex
Assuming word with apostrophe are different: earth's != earth
Assuming all documents follow a format of: doc#.txt
Assuming TF and IDF are defined by equation stated on http://www.tfidf.com/

## Run Script
Environment: Python 2.7
Change directory to tf-idf
Input doc files in ../Input
**python tfidf.py**

## Workflow
1) Open each file in Input folder with doc#.txt format and store word and frequency in hash table
2) Compute tf value for each word in hash table
3) Create a respective doc#.csv file with {word, tf} in Output folder
4) After iterating through all doc files, open the doc#.csv files in Output folder for writing
5) Calculate tf*idf for each word and overwrite doc#.csv with {word, tf*idf}
6) Sort the doc#.csv file by largest tf*idf to smallest

## Efficiency Analysis
Given average of a doc#.txt files
Given each doc#.txt file has average of b words
Given each doc#.txt file has average of c UNIQUE words

(each doc)*(each word + calculate tf for each unique word)
(each csv)*(calculate tf*idf for each unique word + sort csv by decrementing order of tf*idf)

O(a*(b+c)+(a*(c+clog(c))