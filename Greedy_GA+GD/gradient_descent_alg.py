import numpy
import logging


# Revised the algorithm so that it can be applied when P is a matrix
# verifyGDvalue = []


def extract(vec, index):
    if type(vec).__module__ == numpy.__name__:
        temp = vec
    else:
        temp = numpy.array(vec)
    size = temp.shape
    if len(size) == 1:  # vec is a vector
        return temp[index]
    else:  # vec is a matrix
        return temp[:, index]


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
def RMSprop(func, setting, candidate, learningRate):
    learningRateMin = learningRate[0] #0.0000001  # 0.000001
    learningRateMax = learningRate[1] #0.0000007  #0.00001
    iterationNum = 10  #30
    gdbest = None

    # initializing the parameters and make sure it sums to 1
    nonzeroIndex = numpy.nonzero(candidate)[0]
    a = extract(setting.capacity, nonzeroIndex)
    D = extract(setting.latency, nonzeroIndex)
    beta = extract(setting.decayFactor, nonzeroIndex)
    paraLen = len(nonzeroIndex)  # the number of selected controllers
    # print("extracted capacity: %s\nextracted latency: %s\nextracted decay_factor: %s \n" % (a, D, beta))
    # print("selected capacity: %s, arrival_rate: %s" % (sum(a), sum(setting.arrivalRate)))
    if paraLen == 1:  # only one controller is selected
        para = [[]]
        cost = func(setting, para, a, D, beta, False)
        logging.warning("individual %s" % candidate)
        # print "Complete iteration cost: %s, probability: 1" % cost
        return cost

    # temp = numpy.random.random(paraLen)
    temp = list(a)  # initialize the probability based on the capacity
    para_row = [float(element) / sum(temp) for element in temp]
    sw_num, _ = D.shape

    para = [0]*sw_num
    for i in range(sw_num):
        para[i] = list(para_row) # para = [para_row]* sw_num # this is a shallow copy, change one element will change all elements with the same index
    para = numpy.array(para)
    para = para[:, :-1]
    # print("initialized probability %s" % para[:2])

    # print "start gradient evaluation"
    cost = func(setting, para, a, D, beta, False)
    gdbest = updateGdbest(gdbest, cost)
    # verifyGDvalue.append(cost)

    g = func(setting, para, a, D, beta, True)
    paraOld = para

    for i in range(iterationNum):
        g = numpy.array(g)
        learningRate = learningRateMax - (i - 1) * (learningRateMax - learningRateMin) / iterationNum
        para = paraOld - learningRate * g  # update solution

        for rownum in range(sw_num):
            para[0][rownum] = para[0][rownum].clip(0)
            while sum(para[0][rownum]) > 1:
                diff = sum(para[0][rownum])-1
                weight = para[0][rownum]
                weightedDiff = [diff * element / sum(weight) for element in weight]
                para[0][rownum] -= weightedDiff

        para = numpy.ndarray.tolist(para)[0]

        cost = func(setting, para, a, D, beta, False)

        # verifyGDvalue.append(cost)
        # print i, cost

        gdbest = updateGdbest(gdbest, cost)
        g = func(setting, para, a, D, beta, True)
        paraOld = para

    # print "Complete iteration, probability: %s" % para[:2]
    # prob = []
    # para = numpy.array(para)
    # for row in range(sw_num):
    #     temp = para[row, :]
    #     temp = numpy.append(temp, 1-sum(temp))
    #     prob.extend([temp])
    #
    # print "prob%s"%prob[:2]
    # print gdbest

    return gdbest


# from theano_exp import theano_expression
# import matplotlib.pyplot as plt
# # from setting import Setting
# class Setting:
#
#     def __init__(self):
#         self.latency = [[0., 1.41421356, 7.07106781, 12.72792206],
#                         [1.41421356, 0., 5.65685425, 11.3137085],
#                         [7.07106781, 5.65685425, 0., 5.65685425],
#                         [12.72792206, 11.3137085, 5.65685425, 0.]]
#         self.arrivalRate = [20, 25, 30, 24]  # total arrivalRate
#         self.capacity = [45, 450, 30, 300]
#         self.ctlNum = 4
#
#         # self.arrivalRate = 800
#         # self.capacity = [45000, 45000]
#         # self.latency = [0.001, 0.011]
#         # self.ctlNum = 2
#
#         # self.latency = [0.0002, 0.0001, 0.0001, 0.0002]
#         # self.capacity = [45000, 45000, 30000, 30000]
#         # self.ctlNum = 4
#         # self.arrivalRate = 105000
#
#         self.decayFactor = [
#                                0.9] * self.ctlNum  # forces some capacity (1-decayFactor) to be left aside to handle burst traffic
#         self.dlt = 1.0  # self.dlt * avg_resp_time / util
#         self.mu = [100.0] * 5
#         self.beta = 1.0
#
#
# from setting2 import Setting
# setting = Setting()
# individual = [1] *6
# individual.extend([0]*26)
# fitness = RMSprop(theano_expression, setting, individual)
# print(fitness)
#
# plt.figure()
# plt.plot(verifyGDvalue)
# plt.title(fitness, fontsize=10)
# plt.show()
