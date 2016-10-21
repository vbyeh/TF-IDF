import string
import os
import re
import math
import csv

"""
    Check if words are the same but only different in capitalizaiton of first letter
"""
def verify_word(curr_word):
    temp_word = curr_word[0].lower() + curr_word[1:]
    if temp_word == curr_word.lower():   #Capitalization of only first letter
        return temp_word
    else:   #Capitalization of letters in the middle of words
        return curr_word

#data structure with hash tables
#local_hash = {word : current frequency}
#doc_hash = {word: total frequency}

def local_word_hash(doc_path, files, doc_hash, path):
    csv_file_array = []
    for num in range(len(doc_path)):
        curr_csv_file = os.path.join(path, files[num].split('.')[0]+'.csv')
        csv_file_array.append(curr_csv_file)
        doc_len = 0 #number of words in current document
        local_hash = {} #hash to keep all words in current doc
        try:
            with open(doc_path[num],'r') as docfile:
                for line in docfile:
                    for word in line.split():
                        doc_len += 1
                        curr_word_array = re.findall(r"[\w'-]+", word.strip(string.punctuation))
                        for curr_word in curr_word_array:
                            if any(char.isalpha() for char in curr_word):
                                checked_word = verify_word(curr_word)
                                if checked_word not in local_hash:
                                    local_hash[checked_word] = 1
                                    if checked_word not in doc_hash:
                                        doc_hash[checked_word] = 1
                                    else:
                                        doc_hash[checked_word] += 1
                                else:
                                    local_hash[checked_word] += 1
            print 'Input: ' + doc_path[num]
            docfile.close()
            try:
                with open(curr_csv_file, 'wb') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',')
                    for obj in local_hash.items():
                        csvwriter.writerow([obj[0], computeTF(obj[1], doc_len)])
                csvfile.close()
            except:
                print 'Unable to open ' + curr_csv_file + ' for writing'
        except:
            print 'Error compiling data from ' + doc_path[num]
        #temporary write to designated csv file

    return csv_file_array

def complete_word_hash(csvfiles, doc_hash, num_doc):
    for csvf in csvfiles:
        read = csv.reader(open(csvf))
        lines = [line for line in read]
        for line in lines:
            line[1] = float(line[1])*computeIDF(num_doc, doc_hash[line[0]])
        writer = csv.writer(open(csvf, 'w'))
        writer.writerows(sorted(lines, key=lambda x: x[1], reverse=True))
        print 'Output: ' + csvf

"""
    Equation to compute tf
    curr_term = # of times the current term appeared in this doc
    total_doc_terms = # of terms in this doc
"""
def computeTF(curr_term, total_doc_terms):  #everytime we finish a document, we can compute this
    try:
        return curr_term/float(total_doc_terms)
    except ZeroDivisionError:
        return 0

"""
    Equation to compute idf
    num_doc = # of documents in sample
    appear_doc = total number of documents the word appeared in
"""
def computeIDF(num_doc, appear_doc):   #can only compute idf at the end of all documents
    try:
        return math.log10(num_doc/appear_doc)
    except ZeroDivisionError:
        return 0

def initialization():
    try:
        os.chdir("Input")
    except:
        print "ERROR: no input folder found"
        exit(1)
    doc_path = [os.path.join(os.getcwd(), file) for file in os.listdir('.') if re.match(r'doc[0-9].txt', file)]
    files = [file for file in os.listdir('.') if re.match(r'doc[0-9].txt', file)]
    if len(files) == 0:
        print "No files read"
        exit(0)
    os.chdir("..")
    try:
        os.chdir("Output")
    except:
        os.mkdir("Output")
        os.chdir("Output")
    csv_path = os.path.abspath(os.curdir)

    return doc_path, files, csv_path

doc_hash = {}   #hash to keep an aggregated table of all words from all doc
doc_path, files, csv_path = initialization()
csv_files = local_word_hash(doc_path, files, doc_hash, csv_path)
complete_word_hash(csv_files, doc_hash, len(csv_files))

