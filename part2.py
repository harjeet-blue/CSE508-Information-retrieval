import re
import string 
from nltk import word_tokenize
from nltk.corpus import stopwords

dict = {}
docID = {}

def createInvertedIndex():

    for i in range(1400):

        end = str(i + 1);
        file_name = 'Dataset/cranfield' + (4 - len(end))*"0" + end;

        # opening the files
        with open(file_name, 'r') as file:
            data = file.read().replace('\n', ' ')

        tokens = data.split()

        docID[i+1] = "cranfield" + (4 - len(end))*"0" + end;

        for word in tokens:
            if word not in dict:                 # add only if that index is not present in the dict
                dict[word] = [i+1]

            else:
                if i+1 not in dict[word]:        # if that docID is already there in list then don't add
                    dict[word].append(i+1)


def Preprocessing( data ):

    # define stopwords set
    stop_word_set = set(stopwords.words('english') + list(string.punctuation))

    #lowering the string
    data = data.lower();
    
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
    cnt = 0
    ans = []

    while i < len(l1) and j < len(l2):
        cnt += 1
        if l1[i] == l2[j]:
            ans.append(l1[i])
            i = i + 1
            j = j + 1

        elif l1[i] < l2[j]:
            ans.append(l1[i]);
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

    return ans, cnt
    


def AND( l1, l2):
    i = 0
    j = 0
    cnt = 0
    ans = []

    while i < len(l1) and j < len(l2):
        cnt += 1
        if l1[i] == l2[j]:
            ans.append(l1[i])
            i = i+1
            j = j+1

        elif l1[i] < l2[j]:
            i = i+1
        else:
            j = j+1

    return ans, cnt


def NOT(l):   
    ans = []
    
    for i in range(1, 1401):
        if i not in l:
            ans.append(i)

    return ans


def ANDNOT(l1 , l2): # l1 and not l2
    i = 0
    j = 0
    cnt = 0
    ans = []

    while i < len(l1) and j < len(l2):
        cnt += 1
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

    return ans, cnt

def ORNOT(l1, l2):

    l3, cnt = ANDNOT(l2, l1);
    return NOT(l3), cnt

# ******************************************************* QUERY PROCESSING *******************************************

import pickle
def save_data():
    pickle.dump(dict, open('unigramIndex', 'wb'))
    pickle.dump(docID, open('DocumentID', 'wb'))

def load_data():
    return pickle.load( open( 'unigramIndex', 'rb')), pickle.load( open( 'DocumentID', 'rb'))


# ******************************************************* QUERY PROCESSING *******************************************
# createInvertedIndex()
# save_data()

dict,docID = load_data()
# print(dict)



N = int(input("Enter no of queries: "))

for i in range(N):

    query = input("Enter the INPUT Sequence: ")
    query = Preprocessing(query)

    opert = input("Enter the OPERATIONS separted by comma: ")
    operations = opert.split(',')

    operations = [ j.strip() for j in operations ]
    # print(operations)

    try: 

        comparisons = 0
        ans = dict[query[0]]

        if( len(operations) == 0):
            print("Query ", i+1)
            print("No of documents retrived: ", len(ans))
            # print("Name of the documents retrived: ", [ docID[i] for i in ans ] )
            print("No of comparisions: ", comparisons)
            continue


        for i in range(0, len(operations)):

            if operations[i] == 'OR':
                ans, cnt = OR(ans, dict[query[i + 1 ]])
                comparisons += cnt

            elif operations[i] == 'AND':
                ans, cnt = AND(ans, dict[query[i + 1]])
                comparisons += cnt

            elif operations[i] == 'AND NOT':
                ans, cnt = ANDNOT(ans, dict[query[i + 1]])
                comparisons += cnt

            elif operations[i] == 'OR NOT':
                ans, cnt = ORNOT(ans, dict[query[i + 1]])
                comparisons += cnt

            elif operations[i] == 'NOT':
                ans = NOT(ans)

    except KeyError:
        print("\n No such token exists in any file :\n ")
        continue


    print("Query ", i+1)
    print("No of documents retrived: ", len(ans))
    # print("Name of the documents retrived: ", [ docID[i] for i in ans ] )
    print("No of comparisions: ", comparisons)


