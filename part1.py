# importing re module
import re
import string 
from nltk import word_tokenize
from nltk.corpus import stopwords


def relevantTextExtraction():

    for i in range(1400):

        end = str(i + 1)
        file_name = 'Dataset/cranfield' + (4 - len(end))*"0" + end
        # opening the files
        with open(file_name, 'r') as file:
            data = file.read().replace('\n', ' ')

        # regex to extract required strings
        tag1 = "TITLE"
        reg_str = "<" + tag1 + ">(.*?)</" + tag1 + ">"
        res = re.findall(reg_str, data)
        title_str = " ".join(res)

        # regex to extract required strings
        tag2 = "TEXT"
        reg_str = "<" + tag2 + ">(.*?)</" + tag2 + ">"
        res2 = re.findall(reg_str, data)
        text_str = " ".join(res2)

        #concatenate both the strings
        final_str = title_str + " " + text_str

        #printing the result
        # print(title_str, text_str, sep='\n')

        # updating the contenst of the file
        file1 = open(file_name, 'w')
        file1.write(final_str)
        file1.close()


def Preprocessing():

    for i in range(1400):
        end = str(i + 1)
        file_name = 'Dataset/cranfield' + (4 - len(end))*"0" + end
        # opening the files
        with open(file_name, 'r') as file:
            data = file.read().replace('\n', ' ')

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

        # updating the contenst of the file
        file1 = open(file_name, 'w')
        file1.write(final_str)
        file1.close()


relevantTextExtraction()
Preprocessing()
