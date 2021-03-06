import numpy
import logging

import matplotlib.pyplot as plt

verifyGDvalue = []


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
    return sum(fitness) * 1.0 / batch_size


# Gradient descent using RMSprop
def RMSprop(func, setting, candidate):
    learningRateMin = 0.01
    learningRateMax = 0.04
    iterationNum = 30
    gdbest = None

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
    para = [float(element) / sum(temp) for element in temp]
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
    cost = func(setting, para, a, D, beta, False)
    verifyGDvalue.append(cost)

    g = func(setting, para, a, D, beta, True)
    paraOld = para

    for i in range(iterationNum):
        g = numpy.array(g)
        learningRate = learningRateMax - (i - 1) * (learningRateMax - learningRateMin) / iterationNum
        para = paraOld - learningRate * g  # update solution
        para = numpy.ndarray.tolist(para)[0]

        cost = func(setting, para, a, D, beta, False)

        verifyGDvalue.append(cost)
        print i, cost

        gdbest = updateGdbest(gdbest, cost)
        g = func(setting, para, a, D, beta, True)
        paraOld = para

    # print "Complete iteration, probability: %s" % para
    print para
    print 1 - sum(para)
    print gdbest
    return gdbest


from theano_exp import theano_expression




class Setting:

    def __init__(self):
        self.latency = [0.001, 0.011, 0.003, 0.013, 0.013, 0.009, 0.004, 0.005, 0.014, 0.007, 0.012, 0.009, 0.002, 0.018, 0.002, 0.009]
        self.arrivalRate = 500000  # total arrivalRate
        self.capacity = [45000, 45000, 30000, 30000, 30000, 60000, 60000, 60000, 60000, 60000, 90000, 90000, 90000, 90000, 15000, 15000]
        self.ctlNum = 16

        # self.arrivalRate = 800
        # self.capacity = [45000, 45000]
        # self.latency = [0.001, 0.011]
        # self.ctlNum = 2

        # self.latency = [0.0002, 0.0001, 0.0001, 0.0002]
        # self.capacity = [45000, 45000, 30000, 30000]
        # self.ctlNum = 4
        # self.arrivalRate = 105000

        self.decayFactor = [
                               1.0] * self.ctlNum  # forces some capacity (1-decayFactor) to be left aside to handle burst traffic
        self.dlt = 1.0  # self.dlt * avg_resp_time / util
        self.mu = [10.0] * 5


setting = Setting()

individual = [1] * setting.ctlNum
fitness = RMSprop(theano_expression, setting, individual)

plt.figure(1)
plt.plot(verifyGDvalue)
plt.title(fitness, fontsize=10)
plt.show()
