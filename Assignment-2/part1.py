import re
import string 
from nltk import word_tokenize
from nltk.corpus import stopwords


bigramDict = {}          # Dict to store bigram tokens
posDict = {}             # Dict to store positional tokens
docID = {}               # Dict to store DocID of each file
setDict = {}             # Dict to store tokens set 
total_tokens = {}        # Dict to store total no of tokens in a doc
doc_stats = {}           # Dict to store the stats of a doc eg. freq of each token


def createSetDict():

    for i in range(1400):

        end = str(i + 1)
        file_name = 'Dataset/cranfield' + (4 - len(end))*"0" + end

        # opening the files
        with open(file_name, 'r') as file:
            data = file.read()

        single_tokens = data.split()
        # setDict[i+1] = set(single_tokens)
        total_tokens[i+1] = len(single_tokens)

        doc_stats[i+1] = {}

        for word in single_tokens:
            if word not in doc_stats[i+1].keys():
                doc_stats[i+1][word] = 1
            else:
                doc_stats[i+1][word] += 1



def Preprocessing( data ):

    # define stopwords set
    stop_word_set = set(stopwords.words('english') + list(string.punctuation))

    #lowering the string
    data = data.lower()
    
    # tokenization
    sent_tokens = word_tokenize(data)

    # Removing stopwords & punctuations 
    sent_tokens = [ i for i in sent_tokens if i not in stop_word_set]

    # joining the tokens
    final_str = ' '.join(sent_tokens)
    
    #removal of non-char and non-numeric char
    final_str = re.sub(r'[^\w\s]', ' ', final_str)
    return final_str.split()


# ******************************************************* QUERY PROCESSING *******************************************

import pickle

# createSetDict()
# pickle.dump( total_tokens, open('totalToken', 'wb'))
# pickle.dump( doc_stats, open('docStats', 'wb'))

def save_data():
    pickle.dump( bigramDict, open('bigramIndex', 'wb'))
    pickle.dump( posDict, open('positionIndex', 'wb'))
    pickle.dump( docID, open('DocumentID', 'wb'))
    pickle.dump( setDict, open('setDict', 'wb'))
    


def load_data():
    return pickle.load( open( 'bigramIndex', 'rb')), pickle.load( open('positionIndex', 'rb')), pickle.load( open( 'DocumentID', 'rb')), pickle.load( open('setDict', 'rb')), pickle.load(open('totalToken', 'rb')), pickle.load(open('docStats','rb'))



#*************************************************************************************************************************
# createSetDict()
# pickle.dump( setDict, open('setDict', 'wb'))
# save_data()

bigramDict, posDict, docID, setDict, total_tokens, doc_stats = load_data()
# print(setDict[1])


import numpy as np
import math as mt
vocab_size = len(posDict)

def tf_idf_score(matrix, query):

    rel_score = np.dot( matrix, query)
    sorted_indices = np.argsort(-rel_score)

    for i in sorted_indices[:5]:
        print(docID[i+1])
    print()



def binary():
    tf_idf = np.zeros((1400, vocab_size))

    for i in range(1400):
        for j, word in enumerate(posDict.keys()):

            tf = 0
            if i in posDict[word]:
                tf = 1
            
            idf = mt.log(1400/ ( len(posDict[word]) +1 ))

            tf_idf[i][j] = tf * idf

    print("\nTop 5 documents using binary Weighting scheme:-\n")
    query_vector = np.ones(vocab_size)
    tf_idf_score(tf_idf, query_vector)

    return tf_idf


def raw_count():
    tf_idf = np.zeros((1400, vocab_size))

    for i in range(1400):
        for j, word in enumerate(posDict.keys()):

            tf = 0
            if i in posDict[word]:
                tf = len(posDict[word])
            
            idf = mt.log(1400/ ( len(posDict[word]) +1 ))

            tf_idf[i][j] = tf * idf

    print("\nTop 5 documents using raw count Weighting scheme:-\n")
    query_vector = np.ones(vocab_size)
    tf_idf_score(tf_idf, query_vector)

    return tf_idf


def log_normal():
    tf_idf = np.zeros((1400, vocab_size))

    for i in range(1400):
        for j, word in enumerate(posDict.keys()):

            tf = 0
            if i in posDict[word]:
                tf = len(posDict[word])
            
            tf = mt.log(1 + tf)

            idf = mt.log(1400/ ( len(posDict[word]) +1 ))

            tf_idf[i][j] = tf * idf

    print("\nTop 5 documents using log normalization count Weighting scheme:-\n")
    query_vector = np.ones(vocab_size)
    tf_idf_score(tf_idf, query_vector)

    return tf_idf


def term_freqency():
    tf_idf = np.zeros((1400, vocab_size))

    for i in range(1400):
        for j, word in enumerate(posDict.keys()):

            tf = 0
            if i in posDict[word]:
                tf = len(posDict[word])
                
            tf /= total_tokens[i+1]

            idf = mt.log(1400/ ( len(posDict[word]) +1 ))

            tf_idf[i][j] = tf * idf

    print("\nTop 5 documents using double normalization Weighting scheme:-\n")
    query_vector = np.ones(vocab_size)
    tf_idf_score(tf_idf, query_vector)

    return tf_idf

def double_normalization():
    tf_idf = np.zeros( ( 1400, vocab_size))
    
    for i in range(1400):
        for j, word in enumerate(posDict.keys()):

            tf = 0.5 + 0.5*( doc_stats[i+1][word]/max(doc_stats[i+1].values()))
            
            idf = mt.log(1400/ ( len(posDict[word]) +1))

            tf_idf[i][j] = tf * idf

    print("\nTop 5 documents using term frequency count Weighting scheme:-\n")
    query_vector = np.ones(vocab_size)
    tf_idf_score(tf_idf, query_vector)

    return tf_idf



# binary()
# raw_count()
# term_freqency()
# log_normal()
# double_normalization()


query = input("Enter the query for jaccard coefficient:- ")
query_set = set(Preprocessing(query))
jaccard_score = []

for i in range(1, 1401):

    sc = len( setDict[i] & query_set) / len( setDict[i] | query_set)
    jaccard_score.append(sc)

jaccard_score = np.array( jaccard_score )
sorted_indices = np.argsort(-jaccard_score)

print("\nTop 10 document with max jaccrad score :- ")
for i in sorted_indices[:10 ]:
    print( docID[i + 1] )


