"""Genetic Algorithm."""
import random

import numpy

from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt

from contextlib import contextmanager
from datetime import datetime


@contextmanager
def timeit(file_write=None):
    """Context Manager to check runtime."""
    start_time = datetime.now()
    print(f"Tempo de Inicio (hh:mm:ss.ms) {start_time}", file=file_write)
    yield
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print(f"Tempo de Termino (hh:mm:ss.ms) {end_time}", file=file_write)
    print(f"Tempo Total (hh:mm:ss.ms) {time_elapsed}", file=file_write)


def dist2pt(x1, y1, x2, y2):
    """."""
    return max(fabs(x2 - x1), fabs(y2 - y1))  # Distancia de Chebyschev
    # return ((x1 - x2)**2 + (y1 - y2)**2)**(1 / 2) # Distancia Euclidiana


def midPoint(x1, y1, x2, y2):
    """."""
    return (x1 + x2) / 2, (y1 + y2) / 2


def plotar(individuo, f):
    """."""
    plt.close()
    fig1, f1_axes = plt.subplots(ncols=2, nrows=1, constrained_layout=True)
    # fig1.figure(figsize=(15, 15))
    fig1.set_size_inches((20, 15))
    x1, y1, x, y = [], [], [], []
    colors = ["red", "yellow"]
    cutA = 1
    i1 = individuo[0][0]
    a1 = edges[i1] if individuo[1][0] == 0 else edges[i1][::-1]
    if a1[0] != (0.0, 0.0):
        x1.append(0.0)
        y1.append(0.0)
        x1.append(a1[0][0])
        y1.append(a1[0][1])
        # plt.annotate("Des-"+str(deslocamento), midPoint(
        #     0, 0, *edges[individuo[0]][0]))
        # deslocamento += 1
        f1_axes[1].plot(x1, y1, "-", color=colors[1])
        f1_axes[1].annotate(str(cutA), midPoint(0, 0, a1[0][0], a1[0][1]))
        cutA += 1
        # plt.plot(x1, y1, '-*', color=colors[1])
    x.append(a1[0][0])
    y.append(a1[0][1])
    x.append(a1[1][0])
    y.append(a1[1][1])
    # plt.plot(x, y, '-*', color=colors[0])
    # plt.annotate(str(cutA), midPoint(
    #     *a1[0], *a1[1]))
    f1_axes[0].plot(x, y, "-", color=colors[0])
    f1_axes[0].annotate(str(cutA), midPoint(*a1[0], *a1[1]))
    cutA += 1
    for i in range(len(individuo[0]) - 1):
        i1 = individuo[0][i]
        i2 = individuo[0][i + 1 if i + 1 < len(individuo[0]) else 0]
        a1 = edges[i1] if individuo[1][i] == 0 else edges[i1][::-1]
        a2 = (
            edges[i2]
            if individuo[1][i + 1 if i + 1 < len(individuo[0]) else 0] == 0
            else edges[i2][::-1]
        )
        x1, y1, x, y = [], [], [], []
        if a1[1] != a2[0]:
            x1.append(a1[1][0])
            y1.append(a1[1][1])
            x1.append(a2[0][0])
            y1.append(a2[0][1])
            # print(edges[i1][1], edges[i2][0], i1, i2)
            # plt.annotate("Des-"+str(deslocamento), midPoint(
            #     *edges[i1][1], *edges[i2][0]))
            # deslocamento += 1
            # plt.plot(x1, y1, '-*', color=colors[1])
            f1_axes[1].plot(x1, y1, "-", color=colors[1])
            f1_axes[1].annotate(str(cutA), midPoint(*a1[1], *a2[0]))
            cutA += 1
        x.append(a2[0][0])
        y.append(a2[0][1])
        x.append(a2[1][0])
        y.append(a2[1][1])
        # plt.annotate(str(cutA), midPoint(
        #     *a2[0], *a2[1]))
        # plt.plot(x, y, '-*', color=colors[0])
        f1_axes[0].annotate(str(cutA), midPoint(*a2[0], *a2[1]))
        f1_axes[0].plot(x, y, "-", color=colors[0])
        cutA += 1
    f1_axes[1].set_xlim(*f1_axes[0].get_xlim())
    f1_axes[1].set_ylim(*f1_axes[0].get_ylim())
    # plt.show()
    fig1.savefig(f"../resultados/ga/plot/{f}.png")
    # plt.close()


def genIndividuo(edges):
    """
    Generate Individuo.

    args:
        edges -> edges to cut of grapth

    individuo[0]: order of edges
    individuo[1]: order of cut

    """
    v = [random.randint(0, 1) for i in range(len(edges))]
    random.shuffle(v)
    return random.sample(range(len(edges)), len(edges)), v


def evalCut(individuo, pi=1, mi=5):
    """
    Eval Edges Cut.

    args:
        pi -> cutting speed
        mi -> travel speed

    if individuo[1][i] == 0 the cut is in edge order
    else the cut is in reverse edge order

    """
    dist = 0
    i1 = individuo[0][0]
    a1 = edges[i1] if individuo[1][0] == 0 else edges[i1][::-1]
    if a1 != (0.0, 0.0):
        dist += dist2pt(0.0, 0.0, *a1[0])
    dist += (dist2pt(*a1[0], *a1[1])) / pi
    for i in range(len(individuo[0]) - 1):
        i1 = individuo[0][i]
        i2 = individuo[0][i + 1 if i + 1 < len(individuo[0]) else 0]
        a1 = edges[i1] if individuo[1][i] == 0 else edges[i1][::-1]
        a2 = (
            edges[i2]
            if individuo[1][i + 1 if i + 1 < len(individuo[0]) else 0] == 0
            else edges[i2][::-1]
        )
        if a1[1] == a2[0]:
            dist += (dist2pt(*a2[0], *a2[1])) / pi
        else:
            dist += (dist2pt(*a1[1], *a2[0])) / mi + (dist2pt(*a2[0], *a2[1])) / pi
    individuo.fitness.values = (dist,)
    return (dist,)


def main(pop=10000, CXPB=0.75, MUTPB=0.1, NumGenWithoutConverge=100, file=None):
    """
    Execute Genetic Algorithm.

    args:
        pop -> population of GA
        CXPB -> Crossover Probability
        MUTPB -> MUTATION Probability
        NumGenWithoutConverge -> Number of generations without converge
        file -> if write results in file

    """
    pop = toolbox.population(n=pop)

    gen, genMelhor = 0, 0

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Evaluate the entire population
    list(toolbox.map(toolbox.evaluate, pop))
    melhor = min([i.fitness.values for i in pop])
    logbook = tools.Logbook()
    p = stats.compile(pop)
    logbook.record(gen=0, **p)
    logbook.header = "gen", "min", "max", "avg", "std"
    print(logbook.stream, file=file)
    while gen - genMelhor <= NumGenWithoutConverge:
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(toolbox.map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate0(child1[0], child2[0])
                toolbox.mate1(child1[1], child2[1])
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate0(mutant[0])
                toolbox.mutate1(mutant[1])
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        list(toolbox.map(toolbox.evaluate, invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        gen += 1
        minF = min([i.fitness.values for i in pop])
        if minF < melhor:
            melhor = minF
            genMelhor = gen

        p = stats.compile(pop)
        logbook.record(gen=gen, **p)
        if gen - genMelhor <= NumGenWithoutConverge and gen != 1:
            print(logbook.stream)
        else:
            print(logbook.stream, file=file)
        hof.update(pop)
    return pop, stats, hof


files = [
    # 'instance_01_2pol',
    # 'instance_01_3pol',
    # 'instance_01_4pol',
    # 'instance_01_5pol',
    # 'instance_01_6pol',
    # 'instance_01_7pol',
    # 'instance_01_8pol',
    # 'instance_01_9pol',
    # 'instance_01_10pol',
    "rinstance_01_2pol",
    # 'rinstance_01_3pol',
    # 'rinstance_01_4pol',
    # 'rinstance_01_5pol',
    # 'rinstance_01_6pol',
    # 'rinstance_01_7pol',
    # 'rinstance_01_8pol',
    # 'rinstance_01_9pol',
    # 'rinstance_01_10pol',
    # 'sinstance_01_2pol_sep',
    # 'sinstance_01_3pol_sep',
    # 'sinstance_01_4pol_sep',
    # 'sinstance_01_5pol_sep',
    # 'sinstance_01_6pol_sep',
    # 'sinstance_01_7pol_sep',
    # 'sinstance_01_8pol_sep',
    # 'sinstance_01_9pol_sep',
    # 'sinstance_01_10pol_sep',
    # 'g3',
    # 'geo1',
    # 'g2',
    # 'geo3',
    # 'geozika',
    # 'FU',
    # 'rco1',
    # 'TROUSERS',
    # 'DIGHE1',
    # 'DIGHE2',
    # 'teste1',
    # 'g1',
    # 'blaz1',
    # 'rco2',
    # 'blaz2',
    # 'rco3',
    # 'blaz3'
]
# toolbox of GA
toolbox = base.Toolbox()
# Class Fitness
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Representation Individual
creator.create("Individual", list, fitness=creator.FitnessMin)
# if __name__ == "__main__":
if True:
    for f in files:
        file = open(f"../../datasets/particao_arestas/{f}.txt").read().strip().split("\n")
        edges = []
        if file:
            n = int(file.pop(0))
            for i in range(len(file)):
                a = [float(j) for j in file[i].split()]
                edges.append([(a[0], a[1]), (a[2], a[3])])
        # Generate Individual
        toolbox.register("indices", genIndividuo, edges)
        # initializ individual
        toolbox.register(
            "individual", tools.initIterate, creator.Individual, toolbox.indices
        )
        # Generate Population
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        # Selection
        toolbox.register("select", tools.selTournament, tournsize=3)
        # Crossover
        toolbox.register("mate0", tools.cxPartialyMatched)
        toolbox.register("mate1", tools.cxTwoPoint)
        # Mutate
        toolbox.register("mutate0", tools.mutShuffleIndexes, indpb=0.05)
        toolbox.register("mutate1", tools.mutFlipBit, indpb=0.05)
        # toolbox.register("mutate0", tools.mutShuffleIndexes, indpb=0.05)
        # toolbox.register("mutate1", tools.mutFlipBit, indpb=0.05)
        # Objective Function
        toolbox.register("evaluate", evalCut)
        # function to execute map
        toolbox.register("map", map)
        #     n = int(input())
        #     edges = []
        #     for i in range(n):
        #         a = [float(j) for j in input().split()]
        #         edges.append([(a[0], a[1]), (a[2], a[3])])
        hof = None
        qtd = 10
        print(toolbox.individual())
        exit(0)
        # if True:
        #     file_write = None
        with open(f"../resultados/ga/{f}.txt", mode="w+") as file_write:
            print("GA:", file=file_write)
            print(file=file_write)
            for i in range(qtd):
                print(f"Execução {i+1}:", file=file_write)
                print(file=file_write)
                iteracao = None
                with timeit(file_write=file_write):
                    iteracao = main(file=file_write)
                print("Individuo:", iteracao[2][0], file=file_write)
                print("Fitness: ", iteracao[2][0].fitness.values[0], file=file_write)
                print(file=file_write)
                plotar(iteracao[2][0], f + "-" + str(i + 1))
