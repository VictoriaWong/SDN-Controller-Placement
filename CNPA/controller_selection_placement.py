# input:
# a list including all network nodes in the subgraph
# arr_rate: arrival_rates of all nodes
# proc_rate: processing_rates of all nodes
# D_e2e: propogation latency matrix
# T_th: the threshold used to obtain the controller number

# output:
# (npArray) centroids selected for controller placement

import numpy as np
from math import factorial as fact
from network_partition import network_partition


def extract(vec, index):
    temp = np.array(vec)
    size = temp.shape
    if len(size) == 1:  # vec is a vector
        return temp[index]
    else:  # vec is a matrix
        temp = temp[:, index]
        return temp[index, :]


def calculate_Queuing_Delay(arr_rate, proc_rate):
    rho = sum(arr_rate) * 1.0 / sum(proc_rate)
    m = len(list(proc_rate))
    p0 = 0.0
    if sum(arr_rate) > sum(proc_rate) or sum(arr_rate) == sum(proc_rate):
        return 1000000
    elif m == 1:
        return 1.0/(sum(proc_rate)-sum(arr_rate))
    else:
        for k in range(m):
            p0 += ((m * rho) ** k) / fact(k) + ((m * rho) ** m) / (fact(m) * (1 - rho))
        p0 = 1.0 / p0
        D_que = ((m * rho) ** m) * rho * p0 / (sum(arr_rate) * fact(m) * (1 - rho) ** 2)
        print("queuing delay: %s" % D_que)
        return D_que


def calculate_ctlNum(arr_rate, proc_rate, maxD_e2e, T_th):
    ctlNum = 0
    for m in range(len(proc_rate)):
        ctlNum = m+1
        selected_proc_rate = proc_rate[:ctlNum]
        D_que = calculate_Queuing_Delay(arr_rate, selected_proc_rate)
        max_D_tot = maxD_e2e + D_que
        print("max total response time: %s, total controller capacity: %s" % (max_D_tot, sum(selected_proc_rate)))
        if max_D_tot < T_th:
            break
        else:
            continue
    return ctlNum


def multiCtl_Select_Place(nodes, arr_rate, proc_rate, D_e2e, T_th):
    proc_rate = extract(proc_rate, nodes)
    D_e2e = extract(D_e2e, nodes)
    maxD_e2e = np.max(D_e2e)
    print("max propogation delay: %s" % maxD_e2e)
    ctlNum = calculate_ctlNum(arr_rate, proc_rate, maxD_e2e, T_th)

    centroid, _ = network_partition(D_e2e, ctlNum)
    nodes = np.array(nodes)
    result = nodes[centroid]
    return list(result)


# =========== How to call the function ===================
# D = [[0., 1.41421356, 7.07106781, 12.72792206],
#      [1.41421356, 0., 5.65685425, 11.3137085],
#      [7.07106781, 5.65685425, 0., 5.65685425],
#      [12.72792206, 11.3137085, 5.65685425, 0.]]
# arr = [10, 14, 12, 11]
# proc = [100, 200, 110, 150]
# nodes = [1, 2]
# placement = multiCtl_Select_Place(nodes, arr, proc, D, 2.8)
# print(placement)

# ============ Calculate the scheduler location ==========
from setting2 import Setting
setting = Setting()

# calculate the scheduler location
sumLaten = []
for i in range(setting.ctlNum):
    sumLaten.append(sum(setting.latency[i]))

# the node with smallest sum end-to-end latency to other nodes is selected as the centroid
c1 = sumLaten.index(min(sumLaten))
print("scheduler at node: %s" % c1)

nodes = range(0, setting.ctlNum)
placement = multiCtl_Select_Place(nodes, setting.arrivalRate, setting.capacity, setting.latency, np.max(setting.latency)+0.0005)
print(placement)
print(len(placement))