"""Genetic Algorithm."""
import random

import numpy

from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt

from contextlib import contextmanager
from datetime import datetime

from math import ceil


@contextmanager
def timeit(file_write=None):
    """Context Manager to check runtime."""
    start_time = datetime.now()
    print(f'Tempo de Inicio (hh:mm:ss.ms) {start_time}', file=file_write)
    yield
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print(f'Tempo de Termino (hh:mm:ss.ms) {end_time}', file=file_write)
    print(f'Tempo Total (hh:mm:ss.ms) {time_elapsed}', file=file_write)


def dist2pt(x1, y1, x2, y2):
    """."""
    return ((x1 - x2)**2 + (y1 - y2)**2)**(1 / 2)


def midPoint(x1, y1, x2, y2):
    """."""
    return (x1 + x2) / 2, (y1 + y2) / 2


def plotar(individuo, f):
    """."""
    individuo = decode(individuo)
    fig1, f1_axes = plt.subplots(ncols=2, nrows=1, constrained_layout=True)
    # fig1.figure(figsize=(15, 15))
    fig1.set_size_inches((20, 15))
    x1, y1, x, y = [], [], [], []
    colors = ['red', 'yellow']
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
        f1_axes[1].plot(x1, y1, '-', color=colors[1])
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
    f1_axes[0].plot(x, y, '-', color=colors[0])
    f1_axes[0].annotate(str(cutA), midPoint(*a1[0], *a1[1]))
    cutA += 1
    for i in range(len(individuo[0]) - 1):
        i1 = individuo[0][i]
        i2 = individuo[0][i + 1 if i + 1 < len(individuo[0]) else 0]
        a1 = edges[i1] if individuo[1][i] == 0 else edges[i1][::-1]
        a2 = edges[i2] if individuo[1][i + 1 if i + 1 <
                                       len(individuo[0]) else 0] == 0 else edges[i2][::-1]
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
            f1_axes[1].plot(x1, y1, '-', color=colors[1])
            f1_axes[1].annotate(str(cutA), midPoint(*a1[1], *a2[0]))
            cutA += 1
        x.append(a2[0][0])
        y.append(a2[0][1])
        x.append(a2[1][0])
        y.append(a2[1][1])
        # plt.annotate(str(cutA), midPoint(
        #     *a2[0], *a2[1]))
        # plt.plot(x, y, '-*', color=colors[0])
        f1_axes[0].annotate(str(cutA), midPoint(
            *a2[0], *a2[1]))
        f1_axes[0].plot(x, y, '-', color=colors[0])
        cutA += 1
    f1_axes[1].set_xlim(*f1_axes[0].get_xlim())
    f1_axes[1].set_ylim(*f1_axes[0].get_ylim())
    # plt.show()
    fig1.savefig(f'../resultados/brkga/plot/{f}.png')
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


def genIndividuoRK(edges):
    """
    Generate Individuo.

    args:
        edges -> edges to cut of grapth

    individuo[0]: order of edges
    individuo[1]: order of cut

    """
    return [random.random() for i in range(len(edges))], [
        random.random() for i in range(len(edges))]


def decode(ind):
    """."""
    return [ind[0].index(i) for i in sorted(ind[0])], [0 if i < 0.5 else 1 for i in ind[1]]


def evalCut(individuo, pi=1, mi=5):
    """
    Eval Edges Cut.

    args:
        pi -> cutting speed
        mi -> travel speed

    if individuo[1][i] == 0 the cut is in edge order
    else the cut is in reverse edge order

    """
    ind = decode(individuo)
    dist = 0
    i1 = ind[0][0]
    a1 = edges[i1] if ind[1][0] == 0 else edges[i1][::-1]
    if a1 != (0.0, 0.0):
        dist += dist2pt(0.0, 0.0, *a1[0])
    dist += (dist2pt(*a1[0], *a1[1])) / pi
    for i in range(len(ind[0]) - 1):
        i1 = ind[0][i]
        i2 = ind[0][i + 1 if i + 1 < len(ind[0]) else 0]
        a1 = edges[i1] if ind[1][i] == 0 else edges[i1][::-1]
        a2 = edges[i2] if ind[1][i + 1 if i + 1 <
                                 len(ind[0]) else 0] == 0 else edges[i2][::-1]
        if a1[1] == a2[0]:
            dist += (dist2pt(*a2[0], *a2[1])) / pi
        else:
            dist += (dist2pt(*a1[1], *a2[0])) / mi + (
                dist2pt(*a2[0], *a2[1])) / pi
    individuo.fitness.values = (dist, )
    return dist,


def main(P=10000, Pe=0.2, Pm=0.3, pe=0.7, NumGenWithoutConverge=300, file=None):
    """
    Execute Genetic Algorithm.

    args:
        P -> size of population
        Pe -> size of elite population
        Pm -> size of mutant population
        Pe -> elite allele inheritance probability
        NumGenWithoutConverge -> Number of generations without converge
        file -> if write results in file

    """
    pop = toolbox.population(n=P)

    toolbox.register("mate", crossBRKGA, indpb=pe)

    tamElite = ceil(P * Pe)
    tamMutant = ceil(P * Pm)
    tamCrossover = P - tamElite - tamMutant

    gen, genMelhor = 0, 0

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Evaluate the entire population
    list(toolbox.map(toolbox.evaluate, pop))
    # for i in pop:
    #     toolbox.evaluate(i)
    melhor = numpy.min([i.fitness.values for i in pop])
    logbook = tools.Logbook()
    p = stats.compile(pop)
    logbook.record(gen=0, **p)
    logbook.header = "gen", 'min', 'max', "avg", "std"
    print(logbook.stream, file=file)
    while gen - genMelhor <= NumGenWithoutConverge:
        # Select the next generation individuals
        offspring = sorted(
            list(toolbox.map(toolbox.clone, pop)),
            key=lambda x: x.fitness,
            reverse=True
        )
        elite = offspring[:tamElite]
        cross = offspring[tamElite:tamCrossover]
        c = []
        # Apply crossover and mutation on the offspring
        for i in range(tamCrossover):
            e1 = random.choice(elite)
            c1 = random.choice(cross)
            ni = creator.Individual([[], []])
            ni[0] = toolbox.mate(e1[0], c1[0])
            ni[1] = toolbox.mate(e1[1], c1[1])
            c.append(ni)

        p = toolbox.population(n=tamMutant)
        c = elite + c + p
        offspring = c

        # Evaluate the individuals with an invalid fitness

        # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        # list(toolbox.map(toolbox.evaluate, invalid_ind))

        list(toolbox.map(toolbox.evaluate, offspring[tamElite:]))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        gen += 1
        minf = numpy.min([i.fitness.values for i in pop])
        try:
            if minf < melhor:
                melhor = minf
                genMelhor = gen
        except:
            print(minf)

        p = stats.compile(pop)
        logbook.record(gen=gen, **p)
        if gen - genMelhor <= NumGenWithoutConverge and gen != 1:
            print(logbook.stream)
        else:
            print(logbook.stream, file=file)
        hof.update(pop)

    return pop, stats, hof


def crossBRKGA(ind1, ind2, indpb):
    """."""
    return [ind1[i] if random.random() < indpb else ind2[i]
            for i in range(min(len(ind1), len(ind2)))]


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

    'rinstance_01_2pol',
    'rinstance_01_3pol',
    'rinstance_01_4pol',
    'rinstance_01_5pol',
    'rinstance_01_6pol',
    'rinstance_01_7pol',
    'rinstance_01_8pol',
    'rinstance_01_9pol',
    'rinstance_01_10pol',
    'sinstance_01_2pol_sep',
    'sinstance_01_3pol_sep',
    'sinstance_01_4pol_sep',
    'sinstance_01_5pol_sep',
    'sinstance_01_6pol_sep',
    'sinstance_01_7pol_sep',
    'sinstance_01_8pol_sep',
    'sinstance_01_9pol_sep',
    'sinstance_01_10pol_sep',

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
        file = open(f"../datasets/particao_arestas/{f}.txt").read().strip().split('\n')
        edges = []
        if file:
            n = int(file.pop(0))
            for i in range(len(file)):
                a = [float(j) for j in file[i].split()]
                edges.append([(a[0], a[1]), (a[2], a[3])])
        # Generate Individual
        toolbox.register("indices", genIndividuoRK, edges)
        # initializ individual
        toolbox.register("individual", tools.initIterate,
                         creator.Individual, toolbox.indices)
        # Generate Population
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        # Objective Function
        toolbox.register("evaluate", evalCut)
        # function to execute map
        toolbox.register("map", map)

        hof = None
        qtd = 10
        # if True:
        #     file_write = None
        with open(f"../resultados/brkga/{f}.txt", mode='w+') as file_write:
            print("BRKGA:", file=file_write)
            print(file=file_write)
            for i in range(qtd):
                print(f"Execução {i+1}:", file=file_write)
                print(file=file_write)
                iteracao = None
                with timeit(file_write=file_write):
                    iteracao = main(file=file_write)
                print("Individuo:", decode(iteracao[2][0]), file=file_write)
                print("Fitness: ", iteracao[2][0].fitness.values[0], file=file_write)
                print(file=file_write)
                plotar(iteracao[2][0], f + '-b-' + str(i + 1))
