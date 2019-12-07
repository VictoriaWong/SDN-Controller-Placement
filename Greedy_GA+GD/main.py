from globalsetting import GlobalSetting
from localsetting import LocalSetting
import numpy as np
from copy import deepcopy
from theano_exp import theano_expression
from gradient_descent_alg import RMSprop
# from test import RMSprop


# Given two clusters C1 and C2, compute the smallest distance between a controller in C1
# and all the nodes in C2
# return the smallest distance and the closest controller
def computeDist(sett, C1, C2):
    indC1 = sett.cluster[len(sett.candidate[C1])]
    indC2 = sett.cluster[len(sett.candidate[C2])]
    indC1ctl = np.multiply(indC1, sett.candidate[C1])
    indC1ctl = filter(lambda a: a != 0, indC1ctl)  # selected ctl index
    nearestctl = 0
    smallestlaten = float("inf")
    for i in range(len(indC1ctl)):
        latenvec = sett.latency[indC1ctl[i],:]
        latenvec = latenvec[indC2]
        latentot = sum(latenvec)/len(indC2)
        if indC1ctl[i] in [17, 22, 10, 63, 56, 28, 21, 1]:
            latentot = float("inf")
        if latentot < smallestlaten:
            smallestlaten = latentot
            nearestctl = indC1ctl[i]
    return smallestlaten, nearestctl


def run(sett):
    temp = 0
    copyfitness = deepcopy(sett.fitness)
    while temp != sett.clusterNum:
        # print("+++++++++++++++%s+++++++++++++++++++++"%copyfitness)
        worstC = copyfitness.index(max(copyfitness))
        dist = []
        tempctl = []
        for i in range(sett.clusterNum):
            if i == worstC:
                dist.append(float("inf"))
                tempctl.append(None)
            else:
                laten, ctl = computeDist(sett, i, worstC)
                dist.append(laten)
                tempctl.append(ctl)
        # print(dist)
        nearCind = dist.index(min(dist))
        nearCtl = tempctl[nearCind]  # the index of the nearest controller
        nearCtl = [22, 63, 28, 21, 1]
        clusterSett = LocalSetting(sett, worstC, nearCind, nearCtl)

        for i in range(len(clusterSett.latency)):
            print('[' + ','.join(str(x) for x in clusterSett.latency[i]) + '],')

        ctlCandidate = deepcopy(sett.candidate[worstC])
        ctlCandidate.append(1)
        learningRate = sett.learningRate[worstC]
        newfitness = RMSprop(theano_expression, clusterSett, ctlCandidate, learningRate)
        print(sett.city[worstC], sett.city[nearCind])
        print(sett.fitness[worstC], newfitness)
        if newfitness < sett.fitness[worstC]:
            print("a better distribution is found")
            temp = 0
        else:
            temp += 1
            copyfitness[worstC] = 0
            print("No improvement")
            print("=============================================")





sett = GlobalSetting()
run(sett)
