class Setting:

    def __init__(self):

        # self.latency = [0.001, 0.006, 0.004, 0.003, 0.008, 0.003, 0.009000000000000001, 0.009000000000000001, 0.01, 0.001]
        # self.latency = numpy.random.randint(50, size=50)
        # self.latency = [30, 10, 4, 39, 24, 42, 2, 24, 26, 45,
        #            9, 38, 23, 34, 42, 3, 11, 10, 12, 10,
        #            39, 10, 16, 20, 17, 44, 48, 17, 17, 8,
        #            21, 40, 31, 18, 39, 12, 32, 22, 45, 40,
        #            33, 5, 35, 47, 12, 40, 30, 28, 0, 48]
        # self.arrivalRate = 20000  # total arrivalRate
        # self.capacity = [7000, 7000, 6000, 7000, 4000, 8000, 6000, 9000, 4000, 9000]
        # self.dlt = 50  # self.dlt * avg_resp_time + (-util)

        # Setting Three: Large data center in the cloud, latency 1ms-50ms
        self.ctlNum = 50
        self.latency = [0.001, 0.011, 0.027, 0.025, 0.022, 0.049, 0.019, 0.038, 0.028, 0.040,
                         0.019, 0.003, 0.013, 0.045, 0.046, 0.035, 0.017, 0.047, 0.013, 0.020,
                         0.049, 0.009, 0.004, 0.032, 0.005, 0.020, 0.014, 0.007, 0.019, 0.020,
                         0.049, 0.043, 0.023, 0.034, 0.012, 0.032, 0.044, 0.009, 0.002, 0.018,
                         0.002, 0.006, 0.015, 0.030, 0.013, 0.009, 0.026, 0.041, 0.046, 0.021]
        self.arrivalRate = 720000
        self.capacity = [45000, 45000, 45000, 45000, 45000, 45000, 45000, 45000, 45000, 45000,
                         30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000,
                         60000, 60000, 60000, 60000, 60000, 60000, 60000, 60000, 60000, 60000,
                         90000, 90000, 90000, 90000, 90000, 90000, 90000, 90000, 90000, 90000,
                         15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000]

        # Setting Two: Small data center in local placement, latency < 1ms
        # self.ctlNum = 10
        # self.latency = [0.0002, 0.0003, 0.0009, 0.0001, 0.0003, 0.0003, 0.0005, 0.0005, 0.0002, 0.0002]
        # self.capacity = [45000, 45000, 45000, 45000, 45000, 30000, 30000, 30000, 30000, 30000]
        # self.arrivalRate = 120000

        self.decayFactor = [
                               0.83] * self.ctlNum  # forces some capacity (1-decayFactor) to be left aside to handle burst traffic
        self.dlt = 1.0  # self.dlt * avg_resp_time / util
        self.mu = [10.0] * 5

    def printSetting(self):
        print "arrival rate: %s" % self.arrivalRate
        print "latency: %s" % self.latency
        print "capacity: %s" % self.capacity

