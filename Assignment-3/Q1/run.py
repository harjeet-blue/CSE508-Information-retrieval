import lib as lb

print("For the data set \'", lb.file_path[11:], "\' , we have the following findings:")
NodeSet, EdgeList = lb.get_nodes_and_edges()
NumNodes = len(NodeSet)
print("Number of nodes :", NumNodes)

NumEdges = len(EdgeList) 
print("Number of edges :", NumEdges)

AdjMat, UnAdjMat = lb.get_adjacency_matrix(EdgeList, NumNodes)
InEdges, InDeg = lb.get_incoming_edges_and_degrees(AdjMat)
OutEdge, OutDeg = lb.get_outgoing_edges_and_degrees(AdjMat)
AvgInDeg = lb.np.average(InEdges) 
print("Average In-Degree :", AvgInDeg)

AvgOutDeg = lb.np.average(OutEdge) 
print("Average In-Degree :", AvgOutDeg)

MaxInDegreeIndex = InDeg.index(max(InDeg))
MaxInDegree = InDeg[MaxInDegreeIndex] 
print("Max In-Degree Node ID:", MaxInDegreeIndex, "with Degree:", MaxInDegree)

MaxOutDegreeIndex = OutDeg.index(max(OutDeg))
MaxOutDegree = OutDeg[MaxOutDegreeIndex] 
print("Max Out-Degree Node ID:", MaxOutDegreeIndex, "with Degree:", MaxOutDegree)

max_edges = (NumNodes * (NumNodes - 1)) 
NetworkDensity = NumEdges / max_edges
print("Network Density:", NetworkDensity)

local_clustering_coeff = lb.clustering_coeff(UnAdjMat)
in_degrees_list = [InDeg, "In-Degree", "Frequency", "In-Degree Graph"]
out_degrees_list = [OutDeg, "Out-Degree", "Frequency", "Out-Degree Graph"]
local_clustering_list = [local_clustering_coeff, "Clustering-Coeffecient", "Frequency", "Local Clustering Coefficient Graph"]

plot_list = [in_degrees_list, out_degrees_list, local_clustering_list]

for plot in plot_list:
    lb.get_plot(plot)
