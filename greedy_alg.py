import logging
import numpy as np
from setting import Setting
greedy = [0, 1, 11, 12, 18, 21, 22, 24, 26, 27, 34, 37, 38, 39, 40, 41, 44, 45]

_overprovision_factor = 1.2

def ratio_selection(setting):
    ratio = []
    candidate_ind = []
    for i in range(setting.ctlNum):
        temp = setting.capacity[i]*1.0/setting.latency[i]
        ratio.append(temp)
    sortIndex = sorted(range(len(ratio)), key=lambda k: ratio[k])
    remain = setting.arrivalRate*_overprovision_factor

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
        if temp > setting.arrivalRate*_overprovision_factor:
            return candidate_ind
    logging.warning("Controller pool is not large enough")
    return candidate_ind


def latency_selection(setting):
    candidate_ind = []
    sortIndex = sorted(range(len(setting.latency)), key=lambda k: setting.latency[k])
    remain = setting.arrivalRate*_overprovision_factor
    for i in range(setting.ctlNum):
        index = sortIndex[i]
        remain = remain - setting.capacity[index]
        candidate_ind.append(index)
        if remain < 0:
            return candidate_ind


def capacity_selection(setting):
    candidate_ind = []
    sortIndex = sorted(range(len(setting.capacity)), key=lambda k: setting.capacity[k])
    remain = setting.arrivalRate*_overprovision_factor
    for i in range(setting.ctlNum):
        index = sortIndex[setting.ctlNum-i-1]
        remain = remain - setting.capacity[index]
        candidate_ind.append(index)
        if remain < 0:
            return candidate_ind


setting = Setting()
candidate_ind = capacity_selection(setting)
print "selected controller index: %s" % sorted(candidate_ind)
print len(candidate_ind)
