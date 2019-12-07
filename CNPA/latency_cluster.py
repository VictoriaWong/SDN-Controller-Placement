import pickle
import numpy as np

f = open("sprint_cluster.pkl", "rb")
cluster = pickle.load(f)

file = open("/home/victoria/MEGA/Controller placement/topology/sprint_latency.txt", "rb")
D = np.load(file)
temp = 0

dist_cluster = [[] for _ in range(len(cluster))]   # distance matrix for each cluster

for key in cluster:
    print(key)
    subcluster = cluster[key]
    cluster_size = len(subcluster)
    matrix = np.zeros([cluster_size, cluster_size])
    for i in range(cluster_size):
        for j in range(i, cluster_size):
            matrix[i][j] = D[subcluster[i]][subcluster[j]]
    matrix += np.transpose(matrix)
    dist_cluster[temp] = matrix
    temp += 1

for i in range(len(dist_cluster)):
    print("cluster %s" % i)
    print(len(dist_cluster[i]))
    print("\n")

mylist = dist_cluster[0]
for i in range(len(mylist)):
    temp = ','.join(map(str, mylist[i]))
    print("[%s],"% temp)

print(mylist)


