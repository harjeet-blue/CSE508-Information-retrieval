import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

file_path = '../Dataset/email-Eu-core.txt'

def clean_data():
    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(file_path, 'w') as f:
        for line in lines:
            if (line[0] != "#"):
                f.write(line)

def get_nodes_and_edges():
    clean_data()
    data_file = open(file_path, 'r')
    lines = data_file.readlines()
    NodeList = []
    EdgeList = [] 
    for line in lines:
        SplitList = line.split()
        if(SplitList[0].isdigit()):
            NodeList.append(int(SplitList[0]))
        if(SplitList[1].rstrip("\n").isdigit()):
            NodeList.append(int(SplitList[1].rstrip("\n")))
        if(SplitList[0].isdigit() and SplitList[1].rstrip("\n").isdigit()):
            EdgeList.append([int(SplitList[0]), int(SplitList[1].rstrip("\n"))])
    return set(NodeList), EdgeList

def get_adjacency_matrix(EdgeList, NumNodes):
    Adj_Mat = np.zeros((NumNodes, NumNodes)) 
    UnAdjMat = np.zeros((NumNodes, NumNodes)) 
    for Edge in EdgeList: 
        Adj_Mat[Edge[0]][Edge[1]] = 1 
        UnAdjMat[Edge[0]][Edge[1]] = 1
        UnAdjMat[Edge[1]][Edge[0]] = 1
    return Adj_Mat, UnAdjMat

def get_incoming_edges_and_degrees(Adj_Mat):
    in_edges = np.array([sum(row) for row in Adj_Mat.T])
    in_deg = [sum(row) for row in Adj_Mat.T]
    return in_edges, in_deg

def get_outgoing_edges_and_degrees(Adj_Mat):
    out_edges = np.array([sum(row) for row in Adj_Mat])
    out_deg = [sum(row) for  row in Adj_Mat]
    return out_edges, out_deg

def get_direct_neighbours(nodeID, UnAdjMat):
    direct_neighbours = []
    NumNodes = len(UnAdjMat)
    for node in range(NumNodes):
        if(node != nodeID and UnAdjMat[nodeID][node] == 1): 
            direct_neighbours.append(node)
    return direct_neighbours

def get_num_edges(neighbour_list, UnAdjMat):
    edges = 0
    for neighbour1 in neighbour_list:
        for neighbour2 in neighbour_list:
            if(UnAdjMat[neighbour1][neighbour2] == 1 and neighbour1 != neighbour2): 
                edges += 1
    edges = edges/2 
    return edges

def clustering_coeff(UnAdjMat):
    NumNodes = len(UnAdjMat)
    Cluster_List = [0]*NumNodes
    for node in range(NumNodes): 
        neighbours = get_direct_neighbours(node, UnAdjMat) 
        Num_Neigh = len(neighbours)
        Num_Neigh_Edges = get_num_edges(neighbours, UnAdjMat)
        if( Num_Neigh < 2 ):
            coeff = 0
        else:
            coeff = (2 * Num_Neigh_Edges) / ((Num_Neigh * (Num_Neigh - 1)))
        Cluster_List[node] = coeff
    return Cluster_List

def get_dict(list):
    return dict(sorted(dict(Counter(list)).items()))

def get_plot(input):
    values = get_dict(input[0])
    plt_x = values.keys()
    plt_y = values.values()
    plt.plot(plt_x, plt_y)
    plt.xlabel(input[1])
    plt.ylabel(input[2])
    plt.title(input[3])
    fig_name = input[3] + ".png"
    plt.savefig(fig_name)
    plt.show()