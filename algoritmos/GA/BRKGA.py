"""Genetic Algorithm."""
import random

import numpy

from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt

from contextlib import contextmanager
from datetime import datetime

from math import ceil, fabs


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
    return max(fabs(x2 - x1), fabs(y2 - y1))  # Distancia de Chebyschev
    # return ((x1 - x2)**2 + (y1 - y2)**2)**(1 / 2) # Distancia Euclidiana


def midPoint(x1, y1, x2, y2):
    """."""
    return (x1 + x2) / 2, (y1 + y2) / 2


def plotar(individuo, f):
    """."""
    individuo = decode(individuo)
    fig1, f1_axes = plt.subplots(ncols=2, nrows=1, constrained_layout=True)
    # fig1.figure(figsize=(15, 15))
    fig1.set_size_inches((10, 10))
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
    fig1.savefig(f'plots/{f}.png')
    # fig1.savefig(f'../resultados/brkga/plot/{f}.png')
    plt.close()


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


def main(P=10000, Pe=0.2, Pm=0.3, pe=0.7, NumGenWithoutConverge=150, file=None):
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
    gens, inds = [], []
    gens.append(gen)
    inds.append(melhor)
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
        men = False
        try:
            if minf < melhor:
                men = True
                melhor = minf
                genMelhor = gen
        except Exception:
            print(minf)

        p = stats.compile(pop)
        logbook.record(gen=gen, **p)
        if gen - genMelhor <= NumGenWithoutConverge and not men:
            print(logbook.stream)
        else:
            print(logbook.stream, file=file)
        hof.update(pop)
        gens.append(gen)
        inds.append(minf)
    # fig1, f1_axes = plt.subplots(ncols=1, nrows=1, constrained_layout=True)
    # fig1.set_size_inches((20, 15))
    # f1_axes.set_xlim(-1, gens[-1] + 1)
    # f1_axes.set_ylim(inds[-1] - 10, inds[0] + 10)
    # f1_axes.plot(gens, inds, color='blue')
    # # fig1.show()
    # plt.show()
    # plt.close()
    return pop, stats, hof, gens, inds


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

    # 'rinstance_01_2pol',
    # 'rinstance_01_3pol',
    # 'rinstance_01_4pol',
    # 'rinstance_01_5pol',
    # 'rinstance_01_6pol',
    # 'rinstance_01_7pol',
    # 'rinstance_01_8pol',
    # 'rinstance_01_9pol',
    # 'rinstance_01_10pol',
    'sinstance_01_2pol_sep',
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

opcoes = {'pop': [10000, 5000, 1000], 'elite': [.3, .2, .1], 'mut': [.1, .15, .2]}
op = []
for i in opcoes['pop']:
    for j in opcoes['elite']:
        for k in opcoes['mut']:
            op.append((i, j, k))
# toolbox of GA
toolbox = base.Toolbox()
# Class Fitness
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Representation Individual
creator.create("Individual", list, fitness=creator.FitnessMin)
# if __name__ == "__main__":
if True:
    for f in files:
        file = open(f"../../datasets/particao_arestas/{f}.txt").read().strip().split('\n')
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
        for k in op:
            qtd = 1
            if True:
                file_write = None
            # with open(f"../resultados/brkga/{f}_[{k[0]},{k[1]},{k[2]}].txt", mode='w+') as \
                    # file_write:
                print("BRKGA:", file=file_write)
                print(file=file_write)
                for i in range(qtd):
                    print(f"Execução {i+1}:", file=file_write)
                    print(
                        f"Parametros: P={k[0]}, Pe={k[1]}, Pm={k[2]}, pe=0.7, Parada=150",
                        file=file_write
                    )
                    iteracao = None
                    with timeit(file_write=file_write):
                        iteracao = main(
                            P=k[0],
                            Pe=k[1],
                            Pm=k[2],
                            file=file_write
                        )
                    print("Individuo:", decode(iteracao[2][0]), file=file_write)
                    print("Fitness: ", iteracao[2][0].fitness.values[0], file=file_write)
                    print("Gens: ", iteracao[3], file=file_write)
                    print("Inds: ", iteracao[4], file=file_write)
                    print(file=file_write)
                    plotar(iteracao[2][0], f"{f}_[{k[0]}, {k[1]}, {k[2]}]" + str(i + 1))
                    fig1, f1_axes = plt.subplots(ncols=1, nrows=1, constrained_layout=True)
                    fig1.set_size_inches((10, 10))
                    gens, inds = iteracao[3], iteracao[4]
                    # f1_axes.set_ylabel("Valor do Melhor Individuo")
                    # f1_axes.set_xlabel("Gerações")
                    f1_axes.grid(True)
                    f1_axes.set_xlim(-1, gens[-1] + 1)
                    f1_axes.set_ylim(inds[-1] - 10, inds[0] + 10)
                    f1_axes.plot(gens, inds, color='blue')
                    # fig1.show()
                    # fig1.savefig(
                    #     'plots/' + f"{f}_[{k[0]}, {k[1]}, {k[2]}]" +
                    #     str(i + 1) + '.png'
                    # )
                    # fig1.savefig(
                    #     '../resultados/brkga/melhora/' + f"{f}_[{k[0]}, {k[1]}, {k[2]}]" +
                    #     str(i + 1) + '.png'
                    # )
                    # plt.show()
                    plt.close()
                    exit(0)

"""
BRKGA:

Execução 1:

Tempo de Inicio (hh:mm:ss.ms) 2019-10-01 20:48:06.211839
gen	min    	max    	avg    	std
0  	556.548	673.022	620.806	14.7455
1  	554.538	665.074	611.875	15.5769
2  	550.229	666.983	607.451	17.6894
3  	549.55 	672.015	603.517	19.357
4  	546.102	670.419	600.424	20.9821
5  	543.855	671.83 	597.589	22.321
6  	541.608	662.582	594.909	23.4414
7  	535.642	672.304	592.85 	24.4513
9  	529.579	664.499	590.181	25.6122
13 	528.363	667.677	586.344	27.6074
22 	526.038	670.423	581.377	30.1616
24 	524.055	669.279	580.585	30.8253
28 	519.034	670.359	578.569	31.6536
30 	518.52 	671.728	577.992	32.2748
35 	517.747	669.98 	575.68 	33.3946
38 	516.468	665.607	574.15 	34.4093
40 	510.408	668.454	573.123	34.7949
44 	506.869	677.278	570.22 	36.448
47 	506.719	663.572	567.407	37.9637
49 	503.388	665.795	565.032	39.3319
51 	501.162	667.079	561.815	40.7315
53 	496.931	669.893	558.499	43.009
54 	493.876	669.729	556.793	43.9632
56 	492.167	667.817	553.399	45.849
58 	490.699	665.852	550.095	47.8366
59 	490.281	668.584	548.633	48.6687
60 	483.668	663.316	547.01 	49.8228
63 	479.399	680.029	542.714	52.4493
64 	476.292	661.876	541.447	53.5456
68 	475.312	664.84 	536.227	56.3416
69 	471.014	669.508	535.069	57.0638
71 	470.592	662.862	532.903	58.6707
73 	469.449	661.37 	530.522	59.756
74 	466.584	663.32 	529.55 	60.659
76 	466.419	666.176	527.264	61.7212
77 	465.646	665.462	526.53 	62.9322
78 	463.949	675.07 	525.449	63.2201
79 	462.253	669.467	524.409	63.8393
80 	460.861	671.686	523.531	64.6594
81 	459.223	668.694	522.473	65.1638
82 	458.029	663.796	521.475	65.6754
83 	457.321	668.25 	520.753	66.5461
84 	456.843	666.998	519.783	66.8178
85 	455.763	672.6  	518.987	67.4119
86 	455.061	662.56 	518.262	68.0614
87 	453.904	672.383	517.388	68.5554
88 	450.264	666.482	516.598	69.1649
90 	449.039	670.77 	515.04 	70.1529
94 	446.038	670.781	511.749	71.9762
96 	445.577	662.139	510.083	73.2107
97 	440.673	676.771	509.225	73.7143
102	439.774	665.531	504.667	76.5169
105	439.416	662.452	502.535	78.1118
106	437    	663.483	501.866	78.6747
107	435.442	663.537	501.121	79.0047
112	435.418	666.932	498.275	80.7711
113	434.76 	664.324	497.83 	81.2252
116	434.186	666.088	496.237	82.1912
118	433.583	666.018	495.082	82.8042
120	432.227	662.291	494.144	83.7389
126	432.227	663.629	490.761	85.352
128	430.597	667.689	490.533	85.5167
137	429.472	668.038	489.516	86.2696
288	429.472	661.114	487.045	88.1951
Tempo de Termino (hh:mm:ss.ms) 2019-10-01 21:06:44.428997
Tempo Total (hh:mm:ss.ms) 0:18:38.217158
Individuo: ([46, 24, 9, 45, 18, 8, 40, 22, 13, 4, 6, 0, 47, 28, 3,
39, 14, 10, 32, 27, 15, 20, 42, 30, 12, 29, 43, 23, 38, 19, 44, 1,
36, 2, 37, 5, 7, 21, 41, 11, 17, 26, 16, 25, 35, 31, 34, 33], [0, 1,
1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1])
Fitness:  429.4720917914253
Gens:  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97,
98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126,
127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154,
155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182,
183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288]
Inds:  [556.5475205002921, 554.5377534703593, 550.2288351594676, 549.5500620793666, 546.10156512925, 543.8546595362784, 541.6076622648234, 535.6420482445498, 535.6420482445498, 529.5785125465768, 529.5785125465768, 529.5785125465768, 529.5785125465768, 528.363491730856, 528.363491730856, 528.363491730856, 528.363491730856, 528.363491730856, 528.363491730856, 528.363491730856, 528.363491730856, 528.363491730856, 526.0376119020696, 526.0376119020696, 524.0549959207762, 524.0549959207762, 524.0549959207762, 524.0549959207762, 519.0338183513446, 519.0338183513446, 518.5204666225251, 518.5204666225251, 518.5204666225251, 518.5204666225251, 518.5204666225251, 517.7472184114233, 517.7472184114233, 517.7472184114233, 516.4677897322063, 516.4677897322063, 510.4078111200727, 510.4078111200727, 510.4078111200727, 510.4078111200727, 506.869215441767, 506.869215441767, 506.869215441767, 506.7186271847863, 506.7186271847863, 503.38765150993504, 503.38765150993504, 501.16229072219426, 501.16229072219426, 496.9308472653943, 493.8763039608785, 493.8763039608785, 492.1668863041338, 492.1668863041338, 490.69943598023247, 490.2807434471736, 483.66759946416727, 483.66759946416727, 483.66759946416727, 479.3994910833241, 476.2921797782762, 476.2921797782762, 476.2921797782762, 476.2921797782762, 475.3116528055977, 471.0140231019098, 471.0140231019098, 470.5916511026767, 470.5916511026767, 469.44949545946673, 466.5836500747186, 466.5836500747186, 466.4193447772613, 465.6456069639994, 463.9488160435378, 462.25273848983716, 460.8612896262721, 459.2226740405565, 458.02934174229034, 457.3213375716078, 456.84335629895685, 455.76324488589495, 455.06080739199524, 453.90444279305063, 450.26375829107536, 450.26375829107536, 449.03948441244427, 449.03948441244427, 449.03948441244427, 449.03948441244427, 446.0376296205499, 446.0376296205499, 445.57689173016786, 440.67293896879147, 440.67293896879147, 440.67293896879147, 440.67293896879147, 440.67293896879147, 439.77448885856825, 439.77448885856825, 439.77448885856825, 439.41617898084115, 436.9997558633173, 435.4422996136808, 435.4422996136808, 435.4422996136808, 435.4422996136808, 435.4422996136808, 435.41799738458946, 434.759673371529, 434.759673371529, 434.759673371529, 434.18627763582475, 434.18627763582475, 433.5825995186131, 433.5825995186131, 432.2266636893054, 432.2266636893054, 432.2266636893054, 432.2266636893054, 432.2266636893054, 432.2266636893054, 432.2266636893053, 432.2266636893053, 430.59663629367105, 430.59663629367105, 430.59663629367105, 430.59663629367105, 430.59663629367105, 430.59663629367105, 430.59663629367105, 430.59663629367105, 430.59663629367105, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253, 429.4720917914253]
"""
