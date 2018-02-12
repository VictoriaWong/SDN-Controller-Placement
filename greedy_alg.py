from setting import Setting

setting = Setting()
ratio = []
candidate_ind = []

ctlNum = setting.ctlNum
capacity = setting.capacity
latency = setting.latency
arrivalRate = setting.arrivalRate
#
# ctlNum = 5
# capacity = [3, 4, 1, 6, 7]
# latency = [5, 3, 2, 1, 2]
# arrivalRate = 15

for i in range(ctlNum):
    temp = capacity[i]*1.0/latency[i]
    ratio.append(temp)

sortIndex = sorted(range(len(ratio)), key = lambda k: ratio[k])
remain = arrivalRate

for i in range(ctlNum):
    index = sortIndex[ctlNum-i-1]
    remain = remain - capacity[index]
    candidate_ind.append(index)
    if remain < 0:
        break

print "selected controller index: %s" % candidate_ind
