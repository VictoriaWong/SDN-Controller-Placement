import logging
import numpy as np


def ratio_selection(setting):
    ratio = []
    candidate_ind = []
    for i in range(setting.ctlNum):
        temp = setting.capacity[i]*1.0/setting.latency[i]
        ratio.append(temp)
    sortIndex = sorted(range(len(ratio)), key=lambda k: ratio[k])
    remain = setting.arrivalRate

    for i in range(setting.ctlNum):
        index = sortIndex[setting.ctlNum-i-1]
        remain = remain - setting.capacity[index]
        candidate_ind.append(index)
        if remain < 0:
            return candidate_ind


def random_selection(setting):
    candidate_ind = []
    temp = 0
    ctlList = np.random.permutation(setting.ctlNum)
    for i in range(setting.ctlNum):
        candidate_ind.append(ctlList[i])
        temp += setting.capacity[ctlList[i]]
        if temp > setting.arrivalRate:
            return candidate_ind
    logging.warning("Controller pool is not large enough")
    return candidate_ind


def latency_selection(setting):
    candidate_ind = []
    sortIndex = sorted(range(len(setting.latency)), key=lambda k: setting.latency[k])
    remain = setting.arrivalRate
    for i in range(setting.ctlNum):
        index = sortIndex[i]
        remain = remain - setting.capacity[index]
        candidate_ind.append(index)
        if remain < 0:
            return candidate_ind


def capacity_selection(setting):
    candidate_ind = []
    sortIndex = sorted(range(len(setting.capacity)), key=lambda k: setting.capacity[k])
    remain = setting.arrivalRate
    for i in range(setting.ctlNum):
        index = sortIndex[setting.ctlNum-i-1]
        remain = remain - setting.capacity[index]
        candidate_ind.append(index)
        if remain < 0:
            return candidate_ind


class Setting:
    def __init__(self):
        self.ctlNum = 50
        # self.latency = [0.001, 0.006, 0.004, 0.003, 0.008, 0.003, 0.009000000000000001, 0.009000000000000001, 0.01, 0.001]
        # latency = numpy.random.randint(50, size=50)
        # self.latency = [0] * 50
        self.latency = [30, 10, 4, 39, 24, 42, 2, 24, 26, 45,
                   9, 38, 23, 34, 42, 3, 11, 10, 12, 10,
                   39, 10, 16, 20, 17, 44, 48, 17, 17, 8,
                   21, 40, 31, 18, 39, 12, 32, 22, 45, 40,
                   33, 5, 35, 47, 12, 40, 30, 28, 0, 48]
        # self.arrivalRate = 20000  # total arrivalRate
        self.arrivalRate = 10000000
        # self.capacity = [7000, 7000, 6000, 7000, 4000, 8000, 6000, 9000, 4000, 9000]
        self.capacity = [700000, 700000, 700000, 700000, 700000, 700000, 700000, 700000, 700000, 700000,
                         300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000, 300000,
                         500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000,
                         350000, 350000, 350000, 350000, 350000, 350000, 350000, 350000, 350000, 350000,
                         800000, 800000, 800000, 800000, 800000, 800000, 800000, 800000, 800000, 800000]
        self.decayFactor = [1.0] * self.ctlNum  # forces some capacity (1-decayFactor) to be left aside to handle burst traffic
        # self.dlt = 50  # self.dlt * avg_resp_time + (-util)
        self.dlt = 1.0  # self.dlt * avg_resp_time / util
        self.mu = [10.0] * 5

setting = Setting()
candidate_ind = capacity_selection(setting)
print "selected controller index: %s" % sorted(candidate_ind)
