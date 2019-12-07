# each scheduler has different latencies with each controller

import theano.tensor as T
from theano import function
import sys

# Calculate the value and gradient of the objective function using theano
def theano_expression(setting, Pv_vec, capacity, latency, decayFactor, isGradient=True):
    if len(setting.mu) < 3:
        print "invalid parameter for theano expression"
        sys.exit(1)

    P_red = T.dmatrix('P_red')  # (M * (N-1))
    lamda = T.dvector('lamda')  # (M) arrival rate
    capa = T.dvector('capa')  # (N) controller capacity
    D = T.dmatrix('D')  # (N) delay among controllers and schedulers
    dF = T.dvector('dF')  # N
    beta = T.dscalar('beta')  # weight for the synchronization
    # x = T.dvector('x')  # (N) controller selection decision
    delta = T.dscalar('delta')  # Lagrange multiplier for the setup cost
    mu1 = T.dscalar('mu1')
    mu2 = T.dscalar('mu2')
    mu3 = T.dscalar('mu3')
    mu4 = T.dscalar('mu4')
    T_kcenter = T.dscalar('T_kcenter')

    P = T.zeros((lamda.shape[-1], capa.shape[-1]))  # (M*N)
    P = T.set_subtensor(P[:,:-1], P_red)
    one_vec = T.ones(lamda.shape)  # (M)
    sum_mat = T.sum(P, axis=1)  # (M) sum over column
    last_col = T.sub(one_vec, sum_mat)
    P = T.set_subtensor(P[:,-1], last_col)  # assign value to the last column of P

    theta_n = T.dot(lamda, P)  # (1*N) the workload of n controllers

    temp = T.ones(capa.shape)
    # temp = beta*T.sum(temp)*temp  # (N) synchronization cost n
    temp = beta*T.sum(temp)*T.sum(temp) * temp  # (N) synchronization cost n^2
    # temp = beta * T.log(T.sum(temp)) * temp  # (N) synchronization cost log(n)
    a = T.sub(capa, temp)  # subtract the synchronization cost
    diff = T.largest(0.00001, T.sub(a, theta_n))  # set the difference of a and theta_n to
    v_n = T.inv(diff)  # (N) average sojourn time of the nth controller
    l_n = T.dot(lamda, T.mul(P, D))  # (1*N)
    l_n = T.mul(l_n, T.inv(theta_n))  # (1*N) normalize
    T_n = l_n + v_n  # (N) average response time of the nth controller
    avg_T = T.dot(theta_n, T_n) * T.inv(T.sum(theta_n))  # average response time of all controller
    obj1 = avg_T

    # U_n = T.inv(a) * theta_n  # (N) the utilisation of the nth controller
    # U = T.sum(U_n) * T.inv(T.sum(x))  # average utilisation
    U = T.sum(lamda) * T.inv(T.sum(capa))
    obj2 = - U

    remainCpc_n = T.mul(dF, a) - theta_n  # (N) remaining capacity of the nth controller
    const1 = mu1 * T.sum(T.smallest(0, remainCpc_n))

    const2 = mu2 * T.sum(T.smallest(0, last_col))  # probability sum constraint

    const3 = mu3 * T.sum(T.smallest(0, P))  # probability larger than 0 constraint

    const4 = mu4 * T.smallest(0, T_kcenter - avg_T)

    obj = delta * obj2 - const1 - const2 - const3 - const4  # Minimising (-util) while respTime is a constraint
    # obj = delta * obj1 / (-obj2) - const1 - const2 - const3  # Minimising the respTime/util
    # obj = delta * obj1 * T.dot(x, a) - const1 - const2 - const3  # Minimising the results

    if isGradient:
        g = T.grad(obj, P_red)
        gradient = function(inputs=[P_red, lamda, capa, D, dF, delta, beta, mu1, mu2, mu3, mu4, T_kcenter], outputs=[g], on_unused_input='warn')
        return gradient(Pv_vec, setting.arrivalRate, capacity, latency, decayFactor, setting.dlt, setting.beta, setting.mu[0], setting.mu[1], setting.mu[2], setting.mu[3], setting.t_thresh)
    else:
        cost = function(inputs=[P_red, lamda, capa, D, dF, delta, beta, mu1, mu2, mu3, mu4, T_kcenter], outputs=[obj], on_unused_input='warn')
        # time = function(inputs=[P_red, lamda, capa, D, dF, delta, beta], outputs=[obj1], on_unused_input='warn')
        return cost(Pv_vec, setting.arrivalRate, capacity, latency, decayFactor, setting.dlt, setting.beta, setting.mu[0], setting.mu[1], setting.mu[2], setting.mu[3], setting.t_thresh)\
            # , time(Pv_vec, setting.arrivalRate, capacity, latency, decayFactor, setting.dlt, setting.beta)




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
# dF = extract(decayFactor, nonzeroIndex)
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
