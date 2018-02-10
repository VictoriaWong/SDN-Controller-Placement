import numpy
import logging
# import matplotlib.pyplot as plt

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

# verifyGDvalue = []
# verifyGDerror = []

# Gradient descent using RMSprop
def RMSprop(func, setting, candidate):
    learningRate = 0.002
    iterationNum = 300

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
    para = numpy.random.random(paraLen - 1)  # initialize P
    while True:
        sump = numpy.sum(para)
        if sump < 1:
            break
        else:
            para = numpy.random.random(paraLen - 1)

    g = func(setting, para, candidate, a, D, beta, True)
    # print "--------------------------------------"
    cost = func(setting, para, candidate, a, D, beta, False)
    # verifyGDvalue.append(cost)
    gdbest = updateGdbest(None, cost)
    # print "individual %s" % candidate
    # print "cost before optimization: %s, probability: %s" % (cost, para)
    # if isinstance(g, int):
    #     return -100  # when no controller is selected
    eg2 = numpy.zeros(len(g[0]))  # initializing the moving average of g
    e = 1e-8

    paraOld = para

    for i in range(iterationNum):
        g = numpy.array(g)
        eg2 = 0.9 * eg2 + 0.1 * g * g  # update eg2
        para = paraOld - learningRate * g / numpy.sqrt(eg2 + e)  # update solution
        # diff = numpy.sum(numpy.abs(paraOld - para))
        para = numpy.ndarray.tolist(para)[0]
        cost = func(setting, para, candidate, a, D, beta, False)
        # verifyGDerror.append(verifyGDvalue[-1]-cost[0])
        # verifyGDvalue.append(cost)
        gdbest = updateGdbest(gdbest, cost)
        g = func(setting, para, candidate, a, D, beta, True)
        paraOld = para
    # print "Complete iteration cost: %s, probability: %s" % (gdbest, para)
    return gdbest




# plt.figure(1)
# plt.subplot(211)
# plt.plot(verifyGDvalue)
# plt.subplot(212)
# plt.plot(verifyGDerror)
# plt.show()