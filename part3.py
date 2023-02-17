import re
import string 
from nltk import word_tokenize
from nltk.corpus import stopwords


bigramDict = {}          # Dict to store bigram tokens
posDict = {}             # Dict to store positional tokens
docID = {}               # Dict to store DocID of each file


def createInvertedIndex():

    for i in range(1400):

        end = str(i + 1)
        file_name = 'Dataset/cranfield' + (4 - len(end))*"0" + end
        docID[i+1] = "cranfield" + (4 - len(end))*"0" + end


        # opening the files
        with open(file_name, 'r') as file:
            data = file.read().replace('\n', '')

        single_tokens = data.split()


        # ************************* CODE TO CREATE BIGRAM INVERTED LISTS ***********************************
        tokens = []

        for j in range(0, len(single_tokens)-1):
            tokens.append(single_tokens[j] + " " + single_tokens[j+1])

        
        for word in tokens:
            if word not in bigramDict:                 # add only if that index is not present in the bigramDict
                bigramDict[word] = [i+1]

            else:
                if i+1 not in bigramDict[word]:        # if that docID is already there in list then don't add
                    bigramDict[word].append(i+1)


        # ************************ CODE TO CREATE POSITIONAL INVERTED LISTS *********************************

        for itr in range(0, len(single_tokens)):
            word = single_tokens[itr]

            if word not in posDict:                 # add only if that index is not present in the posDict
                
                posDict[word] = {}
                posDict[word][i+1] = [itr]

            else:
                if i + 1 in posDict[word]:
                    posDict[word][i+1].append(itr)
                else:
                    posDict[word][i+1] = [itr]


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


def OR(l1, l2):

    i = 0
    j = 0
    
    ans = []

    while i < len(l1) and j < len(l2):

        if l1[i] == l2[j]:
            ans.append(l1[i])
            i = i + 1
            j = j + 1

        elif l1[i] < l2[j]:
            ans.append(l1[i])
            i = i+1
        else:
            ans.append(l2[j])
            j = j+1


    while i < len(l1):
        ans.append(l1[i])
        i = i + 1
    
    while j < len(l2):
        ans.append(l2[j])
        j = j + 1

    return ans
    


def AND( l1, l2):
    i = 0
    j = 0
    
    ans = []

    while i < len(l1) and j < len(l2):

        if l1[i] == l2[j]:
            ans.append(l1[i])
            i = i+1
            j = j+1

        elif l1[i] < l2[j]:
            i = i+1
        else:
            j = j+1

    return ans


def NOT(l):   
    ans = []
    
    for i in range(1, 1401):
        if i not in l:
            ans.append(i)

    return ans


def ANDNOT(l1 , l2):            # l1 and not l2
    i = 0
    j = 0

    ans = []

    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            i = i + 1
            j = j + 1

        elif l1[i] < l2[j]:
            ans.append(l1[i])
            i = i + 1
        else:
            j = j + 1


    while i < len(l1):
        ans.append(l1[i])
        i = i + 1

    return ans

def ORNOT(l1, l2):

    l3 = ANDNOT(l2, l1)
    return NOT(l3)


def helper( l1, l2):
    i = 0
    j = 0
    
    ans = []

    while i < len(l1) and j < len(l2):

        if l1[i]+1 == l2[j]:
            ans.append(l1[i]+1)
            i = i+1
            j = j+1

        elif l1[i] < l2[j]:
            i = i+1
        else:
            j = j+1

    return ans




# ******************************************************* QUERY PROCESSING *******************************************

import pickle
def save_data():
    pickle.dump( bigramDict, open('bigramIndex', 'wb'))
    pickle.dump( posDict, open('positionIndex', 'wb'))
    pickle.dump( docID, open('DocumentID', 'wb'))

def load_data():
    return pickle.load( open( 'bigramIndex', 'rb')), pickle.load( open('positionIndex', 'rb')), pickle.load( open( 'DocumentID', 'rb'))


#*************************************************************************************************************************

# createInvertedIndex()
# save_data()
bigramDict, posDict, docID = load_data()
# print(posDict)

#*********************************************** QUERY PROCESSING *******************************************************


def bigram_query(query, qn):

    if len(query) < 2:
        print("\nfor BIGRAM query you need to enter atleast 2 tokens. \n ")
        return
    
    d_query=[]

    for itr in range(0, len(query)-1):
        d_query.append(query[itr] + " " + query[itr+1])

    ans = bigramDict[d_query[0]]

    for i in range(1, len(d_query)):
        ans = AND(ans, bigramDict[d_query[i]])
        

    print("\nQuery ", qn+1, "Using BIGRAM INVERTED INDEX : ")
    print("No of documents retrived: ", len(ans))
    # print("Name of the documents retrived: ", [ docID[i] for i in ans ], '\n' )



def positional_query(query, qn):

    potential = list(posDict[query[0]].keys())

    for i in range(1, len(query)):
        potential = AND(potential, list( posDict[query[i]].keys()) )

    ans = []
    
    for file in potential:
        temp = posDict[query[0]][file]
        for word in range(1, len(query)):
            temp = helper(temp, posDict[query[word]][file] )
        if( len(temp) != 0 ):
            ans.append(file)
    

    print("\nQuery ", qn+1, "Using POSITIONAL INVERTED INDEX: ")
    print("No of documents retrived: ", len(ans))
    print("Name of the documents retrived: ", [ docID[i] for i in ans ], '\n' )



N = int(input("Enter no of phrase queries: "))

for i in range(N):

    query = input("Enter the INPUT phrase query: ")

    query = Preprocessing(query)

    try: 
        bigram_query(query, i)
        positional_query(query, i)

    except KeyError:
        print("\n No such token exists in any files :\n ")
        continue




