import numpy as np
from copy import deepcopy

class LocalSetting():

    def __init__(self, globset, clusterind, neigclusterind, newCtlind):
        swind = deepcopy(np.array(globset.cluster[len(globset.candidate[clusterind])]))  # the new controller is not added into the switch pool yet
        swind = np.append(swind, newCtlind)
        # ctlind = np.multiply(swind, globset.candidate[clusterind])
        # ctlind = ctlind[ctlind != 0]
        # if (0 in swind) and (globset.candidate[clusterind][0] == 1):  # if the first controller (index = 0) is selected
        #     ctlind = ctlind + [0]
        # ctlind = np.append(ctlind, newCtlind)  # add the new controller
        neig_swind = globset.cluster[len(globset.candidate[neigclusterind])]
        neig_arrivalRate = self.extract(globset.arrivalRate, neig_swind)
        newCtlcapacity = globset.capacity[newCtlind]
        disproba = np.array(globset.disproba[neigclusterind])
        temp = [x*y for x,y in zip(globset.candidate[neigclusterind], neig_swind)]
        temp = filter(lambda a: a != 0, temp)
        if len(newCtlind) == 1:
            disproba = disproba[:, temp.index(newCtlind)]
            newCtlcapacity -= np.dot(disproba, neig_arrivalRate)
        else:
            for i in range(len(newCtlind)):
                disprobatemp = disproba[:, temp.index(newCtlind[i])]
                newCtlcapacity[i] -= np.dot(disprobatemp, neig_arrivalRate)

        self.ctlNum = len(swind)
        self.latency = self.extract(globset.latency, swind)
        self.capacity = self.extract(globset.capacity, swind, newCtlcapacity)
        self.arrivalRate = self.extract(globset.arrivalRate, swind, 0)
        self.decayFactor = [0.85]*self.ctlNum
        self.dlt = 1.0
        self.mu = [100.0]*5
        self.beta = 0.1

    def extract(self, glob, ind, val=None):
        if type(glob).__module__== np.__name__:
            temp = glob
        else:
            temp = np.array(glob)
        size = temp.shape

        if len(size) == 1:  # vec is a vector
            if val is None:
                return temp[ind]
            elif type(val).__module__== np.__name__:
                temp = temp[ind]
                for i in range(len(val)):
                    temp[i-len(val)] = val[i]
                return temp
            else:
                temp = temp[ind]
                temp[-1] = val
                return temp
        else:  # vec is a matrix
               # add the new controller as a switch, which has 0 arrival rate
            extratemp = temp[ind, :]
            return extratemp[:, ind]



