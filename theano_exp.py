import theano.tensor as T
from theano import function
import sys
import numpy

# Calculate the value and gradient of the objective function using theano
def theano_expression(setting, Pv_vec, candidate, capacity, latency, decayFactor, isGradient=True):
    if len(setting.mu) < 3:
        print "invalid parameter for theano expression"
        sys.exit(1)

    P_red = T.dvector('P_red')
    lamda = T.dscalar('lamda')
    a = T.dvector('a')  # (N) controller capacity
    D = T.dvector('D')  # (N) delay among controllers and schedulers
    beta = T.dvector('beta')  # N
    x = T.dvector('x')  # (N) controller selection decision
    delta = T.dscalar('delta')  # Lagrange multiplier for the setup cost
    mu1 = T.dscalar('mu1')
    mu2 = T.dscalar('mu2')
    mu3 = T.dscalar('mu3')

    P = T.zeros(a.shape)
    P = T.set_subtensor(P[:-1], P_red)
    P = T.set_subtensor(P[-1], 1 - T.sum(P_red))

    theta_n = P * lamda  # (N) the workload of the nth controller
    U_n = T.inv(a) * theta_n  # (N) the utilisation of the nth controller
    U = T.sum(U_n) * T.inv(T.sum(x))  # average utilisation
    obj2 = - U

    diff = T.largest(10, T.sub(a, theta_n))  # set the difference of a and theta_n to
    v_n = T.inv(diff)  # (N) average sojourn time of the nth controller
    l_n = D
    T_n = l_n + v_n  # (N) average response time of the nth controller
    avg_T = T.dot(theta_n, T_n) * T.inv(T.sum(theta_n))  # average response time of all controller
    obj1 = avg_T

    remainCpc_n = T.mul(beta, a) - theta_n - 10  # (N) remaining capacity of the nth controller
    const1 = mu1 * T.sum(T.smallest(0, remainCpc_n))

    mask = T.ones(a.shape)
    mask = T.set_subtensor(mask[-1], 0)
    const2 = 1 - T.dot(P, mask)
    # temp = T.set_subtensor(P[-1], T.largest(0,const4))  # set the last element of P to satisfy the sum to 1
    # P = temp
    const2 = mu2 * T.smallest(0, const2)

    const3 = mu3 * T.sum(T.smallest(0, P))

    obj = delta * obj1 + obj2 - const1 - const2 - const3  # Minimising the results

    if isGradient:
        g = T.grad(obj, P_red)
        gradient = function(inputs=[P_red, lamda, a, D, beta, x, delta, mu1, mu2, mu3], outputs=[g])
        return gradient(Pv_vec, setting.arrivalRate, capacity, latency, decayFactor, candidate, setting.dlt, setting.mu[0], setting.mu[1], setting.mu[2])
    else:
        cost = function(inputs=[P_red, lamda, a, D, beta, x, delta, mu1, mu2, mu3], outputs=[obj])
        return cost(Pv_vec, setting.arrivalRate, capacity, latency, decayFactor, candidate, setting.dlt, setting.mu[0], setting.mu[1], setting.mu[2])




# # Validate the correctness of theano expression
# # There may exist some error between theano_validation and theano_expression, due to different operations for remaining capacity (i.e., whether minus 10 or not)
# # same input as theano_expression: all vectors need to be squeezed\

# def extract(vec, index):
#     temp = numpy.array(vec)
#     return temp[index]

# nonzeroIndex = numpy.nonzero(candidate)[0]
# para = extract(Pv, nonzeroIndex)
# para = para[:-1]
# para = numpy.ndarray.tolist(para)
# a = extract(capacity, nonzeroIndex)
# D = extract(latency, nonzeroIndex)
# beta = extract(decayFactor, nonzeroIndex)
#
# def theano_validation(Pv, arrivalRate, capacity, latency, decayFactor, candidate, dlt, mu, isGradient=True):
#     length = len(capacity)
#     Pv_vec = Pv[:]
#     Pv_vec.append(1 - sum(Pv_vec))
#     theta_n = [arrivalRate * Pv_vec[i] for i in range(length)]
#     vn = [1.0 * candidate[i] / (capacity[i] - theta_n[i]) for i in range(length)]
#     ln = [latency[i] * candidate[i] for i in range(length)]
#     Tn = [vn[i] + ln[i] for i in range(length)]
#     theta_n_Tn = [theta_n[i] * Tn[i] for i in range(length)]
#     T = 1.0 * sum(theta_n_Tn) / sum(theta_n)
#     Un = [theta_n[i] * 1.0 / capacity[i] for i in range(length)]
#     U = sum(Un) * 1.0 / sum(candidate)
#
#     remainCpc = [decayFactor[i] * capacity[i] - theta_n[i] for i in range(length)]
#     for i in range(length):
#         if remainCpc[i] > 10 or remainCpc[i] == 10:
#             remainCpc[i] = 0
#         else:
#             remainCpc[i] -= 10
#     const1 = mu[0] * sum(remainCpc)
#
#     sumP = sum(Pv_vec[:-1])
#     if 1 - sumP > 0 or 1 - sumP == 0:
#         sumP = 0
#     const2 = mu[1] * sumP
#
#     for i in range(length):
#         if Pv_vec[i] > 0:
#             Pv_vec[i] = 0
#     const3 = mu[2] * sum(Pv_vec)
#
#     obj = T - dlt * U - const1 - const2 - const3
#     return obj
