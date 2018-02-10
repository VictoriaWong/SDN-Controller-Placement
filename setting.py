class Setting():

    def __init__(self):
        self.ctlNum = 10
        self.latency = [0.001, 0.006, 0.004, 0.003, 0.008, 0.003, 0.009000000000000001, 0.009000000000000001, 0.01, 0.001]
        self.arrivalRate = 20000  # total arrivalRate
        self.capacity = [7000, 7000, 6000, 7000, 4000, 8000, 6000, 9000, 4000, 9000]
        self.decayFactor = [1.0] * self.ctlNum  # forces some capacity (1-decayFactor) to be left aside to handle burst traffic
        self.dlt = 50
        self.mu = [10.0] * 5

    def printSetting(self):
        print "arrival rate: %s" % self.arrivalRate
        print "latency: %s" % self.latency
        print "capacity: %s" % self.capacity