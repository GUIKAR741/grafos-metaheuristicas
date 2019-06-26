"""."""
import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt

# from multiprocessing import Pool

from contextlib import contextmanager
from datetime import datetime


@contextmanager
def timeit():
    """Gerenciador de Contexto para verificar o tempo de execução."""
    start_time = datetime.now()
    yield
    time_elapsed = datetime.now() - start_time
    print(f'Tempo total (hh:mm:ss.ms) {time_elapsed}')


def dist2pt(x1, y1, x2, y2):
    """."""
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)


def ptmed(x1, y1, x2, y2):
    """."""
    return (x1+x2)/2, (y1+y2)/2


def plotar(individuo):
    """."""
    x1, y1, x, y = [], [], [], []
    cores = ['red', 'yellow']
    corteA = 1
    deslocamento = 1
    if arestas[individuo[0]][0] != (0.0, 0.0):
        x1.append(0.0)
        y1.append(0.0)
        x1.append(arestas[individuo[0]][0][0])
        y1.append(arestas[individuo[0]][0][1])
        # plt.annotate("Des-"+str(deslocamento), ptmed(
        #     0, 0, *arestas[individuo[0]][0]))
        # deslocamento += 1
        plt.plot(x1, y1, '-*', color=cores[1])
    for i in range(len(individuo)):
        i1 = individuo[i]
        i2 = individuo[i+1 if i+1 < len(individuo) else 0]
        x1, y1, x, y = [], [], [], []
        if arestas[i1][1] != arestas[i2][0]:
            x1.append(arestas[i1][1][0])
            y1.append(arestas[i1][1][1])
            x1.append(arestas[i2][0][0])
            y1.append(arestas[i2][0][1])
            # print(arestas[i1][1], arestas[i2][0], i1, i2)
            # plt.annotate("Des-"+str(deslocamento), ptmed(
            #     *arestas[i1][1], *arestas[i2][0]))
            # deslocamento += 1
            plt.plot(x1, y1, '-*', color=cores[1])
        x.append(arestas[i2][0][0])
        y.append(arestas[i2][0][1])
        x.append(arestas[i2][1][0])
        y.append(arestas[i2][1][1])
        plt.annotate(str(corteA), ptmed(
            *arestas[individuo[i2]][0], *arestas[individuo[i2]][1]))
        corteA += 1
        plt.plot(x, y, '-*', color=cores[0])
    plt.show()


n = int(input())
arestas = []
for i in range(n):
    a = [float(j) for j in input().split()]
    arestas.append([(a[0], a[1]), (a[2], a[3])])

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i',
               fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("indices", random.sample, range(len(arestas)), len(arestas))

# Structure initializers
toolbox.register("individual", tools.initIterate,
                 creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalCorte(individuo, pi=1, mi=5):
    """."""
    dist = 0
    if arestas[individuo[0]][0] != (0.0, 0.0):
        dist += dist2pt(0.0, 0.0, *arestas[individuo[0]][0])
    for i in range(len(individuo)):
        i1 = individuo[i]
        i2 = individuo[i+1 if i+1 < len(individuo) else 0]
        if arestas[i1][1] == arestas[i2][0]:
            dist += (dist2pt(*arestas[i2][0], *arestas[i2][1]))/pi
        else:
            dist += (dist2pt(*arestas[i1][1], *arestas[i2][0]))/mi + (
                dist2pt(*arestas[i2][0], *arestas[i2][1]))/pi
    return dist,


toolbox.register("mate", tools.cxPartialyMatched)
# toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.2)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalCorte)

# pool = Pool(50)
toolbox.register("map", map)
# toolbox.register("map", pool.map)


def main(pop=500, CXPB=0.7, MUTPB=0.2, NGENSEMMELHORA=300):
    """."""
    pop = toolbox.population(n=1000)

    gen, genMelhor = 0, 0

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)

    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    melhor = min(fitnesses)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    logbook = tools.Logbook()
    p = stats.compile(pop)
    logbook.record(gen=0, **p)
    logbook.header = "gen", 'min', 'max', "avg", "std"
    print(logbook.stream)
    while gen - genMelhor <= NGENSEMMELHORA:
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(toolbox.map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(toolbox.map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        gen += 1
        try:
            if min(fitnesses) < melhor:
                melhor = min(fitnesses)
                genMelhor = gen
        except:
            print(fitnesses)

        p = stats.compile(pop)
        logbook.record(gen=gen, **p)
        print(logbook.stream)

        hof.update(pop)
    # print(hof[0])
    # print([arestas[i] for i in hof[0]])
    return pop, stats, hof


if __name__ == "__main__":
    hof = None
    ll = []
    for i in range(10):
        with timeit():
            ll.append(main(NGENSEMMELHORA=10))
    print([i[2][0].fitness.values for i in ll])
    # plotar(hof[0])