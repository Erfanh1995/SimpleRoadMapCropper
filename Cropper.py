# Crop OSM maps based on a bounding box (Not a true crop = partial edges will not be considered)
# Put this code next to your data folder (This code is compatible with Graph Sampling Toolkit)
# Author: Erfan Hosseini Sereshgi (shosseinisereshgi@tulane.edu)
# Company: Tulane University
# Modified: 4/18/2023

XLow = 9999999
XHigh = 0
YLow = 9999999
YHigh = 0

data = "" # name of the dataset e.g. berlin_large

# If you want to use another map's bounding box to crop the current map uncomment this section:
""" 
algorithm = "" # name of the algorithm that generated that map e.g. james
with open("data/"+data+"/algorithm/"+algorithm+"/"+data+"_"+algorithm+"_vertices.txt",'r') as f1:
	vertices = f1.readlines()
	print("Done reading!")

for i in vertices:
	a = i.strip('\n').split(',')
	if float(a[1]) > XHigh:
		XHigh = float(a[1])
	if float(a[1]) < XLow:
		XLow = float(a[1])
	if float(a[2]) > YHigh:
		YHigh = float(a[2])
	if float(a[2]) < YLow:
		YLow = float(a[2])
print("Updated the bounding box")
"""

rcm_vertices = {}
with open("data/"+data+"/groundtruth/"+data+"_vertices_osm.txt",'r') as f2:
	for line in f2:
		temp = line.strip('\n').split(',')
		rcm_vertices[temp[0]] = (float(temp[1]), float(temp[2]))

rcm_edges = []
with open("data/"+data+"/groundtruth/"+data+"_edges_osm.txt", 'r') as f3:
	for line in f3:
		temp = line.strip('\n').split(',')
		rcm_edges.append([temp[1], temp[2]])

final_v = {}
final_e = []

print("filtering...")

with open("data/"+data+"/groundtruth/"+data+"_vertices_osm_crp.txt", 'w') as f4:
	for edge in rcm_edges:
		flag1 = False
		flag2 = False
		if rcm_vertices[edge[0]][0] < XHigh and rcm_vertices[edge[0]][0] > XLow and rcm_vertices[edge[0]][1] < YHigh and rcm_vertices[edge[0]][1] > YLow:
			if edge[0] not in final_v.keys():
				final_v[edge[0]] = rcm_vertices[edge[0]]
				f4.write(str(edge[0]) + "," + str(rcm_vertices[edge[0]][0]) + "," + str(rcm_vertices[edge[0]][1]) + "\n")
			else:
				print(edge[0])
			flag1 = True
		if rcm_vertices[edge[1]][0] < XHigh and rcm_vertices[edge[1]][0] > XLow and rcm_vertices[edge[1]][1] < YHigh and rcm_vertices[edge[1]][1] > YLow:
			if edge[1] not in final_v.keys():
				final_v[edge[1]] = rcm_vertices[edge[1]]
				f4.write(str(edge[1]) + "," + str(rcm_vertices[edge[1]][0]) + "," + str(rcm_vertices[edge[1]][1]) + "\n")
			else:
				print(edge[1])
			flag2 = True
		if flag1 and flag2:
			if edge not in final_e:
				final_e.append(edge)

print("Done with vertices!")

counter = 1
with open("data/"+data+"/groundtruth/"+data+"_edges_osm_crp.txt",'w') as f5:
	for edge in final_e:
		f5.write(str(counter) + "," + str(edge[0]) + "," + str(edge[1]) + "\n")
		counter += 1

print("Done with edges!")



