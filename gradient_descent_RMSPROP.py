import numpy
import logging

import matplotlib.pyplot as plt
import random

verifyGDvalue = []
random.seed(71456)


def extract(vec, index):
    temp = numpy.array(vec)
    return temp[index]


# Update the best solution
def updateGdbest(currentBest, newValue):
    if currentBest is None:
        return newValue
    elif currentBest > newValue:
        return newValue
    else:
        return currentBest


def Batch_RMSprop(func, setting, candidate):
    batch_size = 5
    fitness = []
    for j in range(batch_size):
        fitness.append(RMSprop(func, setting, candidate))
    return sum(fitness)*1.0/batch_size


# Gradient descent using RMSprop
def RMSprop(func, setting, candidate):
    learningRate = 0.002
    iterationNum = 70
    moving_avg = []
    moving_win = 10

    # initializing the parameters and make sure it sums to 1
    nonzeroIndex = numpy.nonzero(candidate)[0]
    a = extract(setting.capacity, nonzeroIndex)
    D = extract(setting.latency, nonzeroIndex)
    beta = extract(setting.decayFactor, nonzeroIndex)
    paraLen = len(nonzeroIndex)  # the number of selected controllers
    if paraLen == 1:  # only one controller is selected
        para = []
        cost = func(setting, para, candidate, a, D, beta, False)
        logging.warning("individual %s" % candidate)
        # print "Complete iteration cost: %s, probability: 1" % cost
        return cost

    # temp = numpy.random.random(paraLen)
    temp = list(a)  # initialize the probability based on the capacity
    para = [float(element)/sum(temp) for element in temp]
    para = para[:-1]


    # para = numpy.random.random(paraLen - 1)  # initialize P
    # while True:
    #     print "evaluate the probability paramete
    #     sump = numpy.sum(para)
    #     if sump < 1:
    #         break
    #     else:
    #         para = numpy.random.random(paraLen - 1)

    print "start gradient evaluation"
    cost = func(setting, para, candidate, a, D, beta, False)
    verifyGDvalue.append(cost)

    g = func(setting, para, candidate, a, D, beta, True)
    eg2 = numpy.zeros(len(g[0]))  # initializing the moving average of g
    e = 1e-8
    paraOld = para

    for i in range(iterationNum):
        g = numpy.array(g)
        eg2 = 0.9 * eg2 + 0.1 * g * g  # update eg2
        para = paraOld - learningRate * g / numpy.sqrt(eg2 + e)  # update solution
        para = numpy.ndarray.tolist(para)[0]

        cost = func(setting, para, candidate, a, D, beta, False)
        verifyGDvalue.append(cost)

        # gdbest = updateGdbest(gdbest, cost)
        g = func(setting, para, candidate, a, D, beta, True)
        paraOld = para

        if i > (iterationNum - moving_win - 1):
            temp = func(setting, para, candidate, a, D, beta, False)
            moving_avg.append(temp[0])

    # print "Complete iteration, probability: %s" % para
    return [sum(moving_avg)*1.0/len(moving_avg)]


from theano_exp import theano_expression
from setting import Setting

setting = Setting()

individual = [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
print sum(individual)

fitness = RMSprop(theano_expression, setting, individual)
print fitness
plt.figure(1)
plt.plot(verifyGDvalue)
plt.title((0.002, fitness),fontsize=10)
plt.show()
