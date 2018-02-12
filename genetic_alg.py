import random
from deap import creator, base, tools
import multiprocessing
import logging
import matplotlib.pyplot as plt
from theano_exp import theano_expression
from setting import Setting
from gradient_descent_alg import RMSprop

# logging.basicConfig(level=logging.INFO)

# ========================================================================================
# Knapsack problem setting
# ========================================================================================
# POP_SIZE = 10000
# CXPB, MUTPB = 1, 0.1
#
# # Dataset 1: Optimal 13549094
# IND_SIZE = 24
# VALUE = [ 825594,1677009,1676628,1523970, 943972,  97426,  69666,1296457,1679693,1902996,1844992,1049289,1252836,1319836, 953277,2067538, 675367, 853655,1826027,  65731, 901489, 577243, 466257, 369261]
# WEIGHT = [382745,799601,909247,729069,467902, 44328, 34610,698150,823460,903959,853665,551830,610856,670702,488960,951111,323046,446298,931161, 31385,496951,264724,224916,169684]
# CAPACITY = 6404180
#
# # Dataset 2: Optimal 1458
# # IND_SIZE = 15
# # VALUE = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240]
# # WEIGHT = [70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120]
# # CAPACITY = 750
#
# # Dataset 3: http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/
# # VALUE = []
# # WEIGHT = []
# # data = []
# # with open("knapPI_1_100_1000_1", "r") as testFile:
# #     for line in testFile:
# #         data = line.split()
# #         VALUE.append(int(data[0]))
# #         WEIGHT.append(int(data[1]))
# # IND_SIZE = VALUE.pop(0)
# # CAPACITY = WEIGHT.pop(0)
# #
# # Fitness function design for knapsack problem
# def evalMax(individual):
#     value = [a * b for a, b in zip(VALUE, individual)]
#     weight = [a * b for a, b in zip(WEIGHT, individual)]
#     if sum(weight) > CAPACITY:
#         return sum(value)+30*(CAPACITY-sum(weight)),
#     else:
#         return sum(value),


setting = Setting()
IND_SIZE = setting.ctlNum
POP_SIZE = 200
# CXPB  is the probability with which two individuals are crossed
# MUTPB is the probability for mutating an individual
CXPB, MUTPB = 1, 0.1


def evalMin(individual):
    logging.info("Evaulating %s " % individual)
    if max(individual) == 0:
        return 10000,
    fitness = RMSprop(theano_expression, setting, individual)
    return fitness[0],

# ----------
# Operator registration
# ----------
# register the goal / fitness function


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of IND_SIZE 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, IND_SIZE)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalMin)

# register the crossover operator
toolbox.register("mate", tools.cxOnePoint)

# register a mutation operator with a probability to flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=1)

# operator for selecting individuals for breeding the next generation:
toolbox.register("selectParent", tools.selRandom)

toolbox.register("selectGeneration", tools.selBest)


def main():
    random.seed(64)

    pool = multiprocessing.Pool(8)

    toolbox.register("map", pool.map)
    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=POP_SIZE)

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    print("  Min %s" % min(fits))
    print("  Max %s" % max(fits))

    # Variable keeping track of the number of generations
    g = 0
    std = 100
    elitist_ind = []
    elitist_fit = []


    # Begin the evolution
    while g < 300 :
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next len(pop) generation individuals
        offspring = toolbox.selectParent(pop, POP_SIZE)
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                # fitness values of the children must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced
        pop[:] = toolbox.selectGeneration(pop + offspring, POP_SIZE)

        print "New gener has %s " % (len(pop))
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        best_ind = tools.selBest(pop, 1)[0]
        elitist_ind.append(best_ind)
        elitist_fit.append(best_ind.fitness.values)
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    plt.figure(1)
    plt.subplot(211)
    plt.plot(elitist_ind)
    plt.subplot(212)
    plt.plot(elitist_fit)
    plt.show()


if __name__ == "__main__":
    main()



