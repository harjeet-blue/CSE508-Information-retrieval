import math
import csv
import numpy as np
import matplotlib.pyplot as plt
def get_count(dic):
    return math.factorial(dic[3])*math.factorial(dic[2])*math.factorial(dic[1])*math.factorial(dic[0])

def getDCG(data):
    dcg = [0]*len(data)
    dcg[0] = (int)(data[0][col("rel")])
    for line in range(1, len(data)):
        dcg[line] = dcg[line-1] + (int)(data[line][col("rel")]) / math.log(line + 1, 2)
    return dcg

# f1 to get feature-1, q to get query_id and rel to get relevance score
def col(str): 
    if(str == "rel"):
        return 0
    elif(str == "q"):
        return 1
    else:
        return (int)(str[1:]) + 1

def get_rel(item):
    return (int)(item[col("rel")])

def get_f75(item):
    return (float)(item[col("f75")][3:])


file = open("IR-assignment-2-data (2).txt","r")
nLines = file.readlines()
dataset = []
for l in nLines:
    line = l.strip().split()
    if( line[col("q")] == 'qid:4'):
        dataset.append(l.strip().split())

dcg = getDCG(dataset)
dataset = sorted(dataset, key=get_rel, reverse=True)

with open("filter.csv", "w+") as fil:
    writer = csv.writer(fil, delimiter=',')
    writer.writerows(dataset)

#Using the filtered Data
count_dict = { 3:0 , 2:0, 1:0, 0:0 }
filer_data = []
with open("filter.csv", "r") as fil:
    reader = csv.reader(fil)
    for line in reader:
        count_dict[get_rel(line)]+=1
        filer_data.append(line)

print("Total files Possible :", get_count(count_dict))
ndcg = getDCG(filer_data)
print("nDCG of 50th element:", dcg[49]/ndcg[49])
print("nDCG of given dataset:", dcg[len(dcg)-1]/ndcg[len(ndcg)-1])

ranking = sorted(filer_data, key=get_f75, reverse=True)
with open("ranking.csv", "w+") as fil:
    writer = csv.writer(fil, delimiter=',')
    writer.writerows(ranking)

#reading ranked data
ranking_data = []
with open("ranking.csv", "r") as fil:
    reader = csv.reader(fil)
    for line in reader:
        ranking_data.append(line)
dcg_ranked = getDCG(ranking_data)
print("nDCG of ranked dataset:", dcg_ranked[len(dcg_ranked)-1]/ndcg[len(ndcg)-1])

#plotting precision-recall curve
relevance = []
for row in ranking_data:
    if((int)(row[col("rel")]) > 0):
        relevance.append(1)
    else:
        relevance.append(0)

relevance = np.array(relevance)
# Calculate precision and recall for each document
precision = np.cumsum(relevance) / np.arange(1, len(relevance)+1)
recall = np.cumsum(relevance) / np.sum(relevance)

# Plot the precision-recall curve
plt.plot(recall, precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()
file.close()