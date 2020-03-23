"""."""
from math import ceil, floor
from solution import Solution
from pprint import pprint
from collections import OrderedDict
from random import sample, choice
import matplotlib.pyplot as plt


def plotar(individuo: Solution, f):
    """."""
    plt.close()
    fig1, f1_axes = plt.subplots(ncols=2, nrows=1, constrained_layout=True)
    plt.title(f"{f} - Fit: {individuo.fitness}")
    # fig1.figure(figsize=(15, 15))
    fig1.set_size_inches((15, 15))
    x1, y1, x, y = [], [], [], []
    colors = ["red", "yellow"]
    cutA = 1
    i1 = individuo.lista[0][0]
    a1 = edges[i1] if individuo.lista[1][0] == 0 else edges[i1][::-1]
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
    for i in range(len(individuo.lista[0]) - 1):
        i1 = individuo.lista[0][i]
        i2 = individuo.lista[0][i + 1 if i + 1 < len(individuo.lista[0]) else 0]
        a1 = edges[i1] if individuo.lista[1][i] == 0 else edges[i1][::-1]
        a2 = (
            edges[i2]
            if individuo.lista[1][i + 1 if i + 1 < len(individuo.lista[0]) else 0] == 0
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
    fig1.savefig(f"plots/{f}.png")
    # plt.close()


def buscaLocal(solucao: Solution, delta=0.2, sigma=0.05) -> Solution:
    """."""
    if delta > 0:
        elementos = int(ceil(delta * len(solucao.lista[0])))
        escolhidos = sample(solucao.lista[0], elementos)
        escolhidos = list(zip(escolhidos, escolhidos[::-1]))[
            : floor(len(escolhidos) / 2)
        ]
        for i in escolhidos:
            solucao.lista[0][i[0]], solucao.lista[0][i[1]] = (
                solucao.lista[0][i[1]],
                solucao.lista[0][i[0]],
            )
    if sigma > 0:
        elementos = int(ceil(delta * len(solucao.lista[0])))
        escolhidos = sample(solucao.lista[0], elementos)
        for i in escolhidos:
            solucao.lista[1][i] = 0 if solucao.lista[1][i] == 1 else 1
    return solucao


def atualizaSolucao(solucao: Solution, melhorSolucao: Solution) -> True:
    """."""
    evalCut(solucao)
    if solucao.fitness < melhorSolucao.fitness:
        melhorSolucao.lista = solucao.lista
        melhorSolucao.fitness = solucao.fitness
        return True
    return False


def evalCut(individuo: Solution, pi: float = 1, mi: float = 5) -> float:
    """
    Eval Edges Cut.

    args:
        pi -> cutting speed
        mi -> travel speed

    if individuo[1][i] == 0 the cut is in edge order
    else the cut is in reverse edge order

    """
    dist = 0
    i1 = individuo.lista[0][0]
    a1 = edges[i1] if individuo.lista[1][0] == 0 else edges[i1][::-1]
    if a1 != (0.0, 0.0):
        dist += dist2pt(0.0, 0.0, *a1[0])
    dist += (dist2pt(*a1[0], *a1[1])) / pi
    for i in range(len(individuo.lista[0]) - 1):
        i1 = individuo.lista[0][i]
        i2 = individuo.lista[0][i + 1 if i + 1 < len(individuo.lista[0]) else 0]
        a1 = edges[i1] if individuo.lista[1][i] == 0 else edges[i1][::-1]
        a2 = (
            edges[i2]
            if individuo.lista[1][i + 1 if i + 1 < len(individuo.lista[0]) else 0] == 0
            else edges[i2][::-1]
        )
        if a1[1] == a2[0]:
            dist += (dist2pt(*a2[0], *a2[1])) / pi
        else:
            dist += (dist2pt(*a1[1], *a2[0])) / mi + (dist2pt(*a2[0], *a2[1])) / pi
    individuo.fitness = dist
    return dist


def dist2pt(x1: float, y1: float, x2: float, y2: float) -> float:
    """."""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


def midPoint(x1, y1, x2, y2):
    """."""
    return (x1 + x2) / 2, (y1 + y2) / 2


def construcaoRandomicaGulosa() -> Solution:
    """."""
    grafo = {}
    for key in graph.keys():
        grafo[key] = list(graph[key])
    inicio = choice([*graph.keys()])
    arestas = []
    direcao = []
    arestaAtual = inicio
    while len(arestas) != len(ordEdges):
        distancias = []
        for i in grafo[arestaAtual]:
            distancias.append(
                (i, dist2pt(*unCriptGraph[arestaAtual], *unCriptGraph[i]))
            )
        if distancias == []:
            edge = []
            list(map(lambda x: edge.extend(x[1]), grafo.items()))
            edge = list(set(edge))
            distancias = [
                (i, dist2pt(*unCriptGraph[arestaAtual], *unCriptGraph[i])) for i in edge
            ]
            menor = min(distancias, key=lambda x: x[1])
            arestaAtual = menor[0]
            continue
        menor = None
        menor = min(distancias, key=lambda x: x[1])
        arestas.append((arestaAtual, menor[0]))
        direcao.append(0 if arestas[-1] in ordEdges else 1)
        grafo[arestaAtual].remove(arestas[-1][-1])
        arestaAtual = arestas[-1][-1]
        grafo[arestaAtual].remove(arestas[-1][0])
    return Solution(
        [
            [
                ordEdges.index(j if direcao[i] == 0 else j[::-1])
                for i, j in enumerate(arestas)
            ],
            direcao,
        ]
    )


def GRASP(maximoIteracoes: int, seed=None) -> Solution:
    """."""
    it, itMelhor = 0, 0
    melhorSolucao = Solution()
    while it - itMelhor <= maximoIteracoes:
        if it % 100 == 0:
            print(f"IT: {it} "
                  f"ITMELHOR: {itMelhor} "
                  f"IT-ITMELHOR: {it-itMelhor} "
                  f"MAXIMOIT: {maximoIteracoes} "
                  f"FIT: {melhorSolucao.fitness}")
        solucao = construcaoRandomicaGulosa()
        if atualizaSolucao(solucao, melhorSolucao):
            itMelhor = it
        solucao = buscaLocal(solucao)
        if atualizaSolucao(solucao, melhorSolucao):
            itMelhor = it
        it += 1
    return melhorSolucao


files = [
    # 'instance_01_2pol',
    # 'instance_01_4pol',
    # 'instance_01_6pol',
    # 'instance_01_8pol',
    # 'instance_01_8polc',
    # "rinstance_01_2pol",
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

    # novas instancias

    # "albano",
    # "blaz1",
    # "blaz2",
    # "blaz3",
    # "dighe1",
    # "dighe2",
    # "fu",
    # "instance_01_2pol",
    # "instance_01_3pol",
    # "instance_01_4pol",
    # "instance_01_5pol",
    # "instance_01_6pol",
    # "instance_01_7pol",
    # "instance_01_8pol",
    # "instance_01_9pol",
    # "instance_01_10pol",
    # "instance_01_16pol",
    # "instance_artificial_01_26pol_hole",
    # "rco1",
    # "rco2",
    "rco3",
    # "shapes2",
    # "shapes4",
    # "spfc_instance",
    # "trousers",
    # "albano_sep",
    # "blaz1_sep",
    # "blaz2_sep",
    # "blaz3_sep",
    # "dighe1_sep",
    # "dighe2_sep",
    # "fu_sep",
    # "instance_01_2pol_sep",
    # "instance_01_3pol_sep",
    # "instance_01_4pol_sep",
    # "instance_01_5pol_sep",
    # "instance_01_6pol_sep",
    # "instance_01_7pol_sep",
    # "instance_01_8pol_sep",
    # "instance_01_9pol_sep",
    # "instance_01_10pol_sep",
    # "instance_01_16pol_sep",
    "instance_artificial_01_26pol_hole_sep",
    # "rco1_sep",
    # "rco2_sep",
    # "rco3_sep",
    # "shapes2_sep",
    # "shapes4_sep",
    # "spfc_instance_sep",
    # "trousers_sep",
]
if __name__ == "__main__":
    for f in files:
        file = (
            open(f"../../datasets/particao_arestas/ejor/{f}.txt").read().strip().split("\n")
        )
        edges = []
        if file:
            n = int(file.pop(0))
            for i in range(len(file)):
                a = [float(j) for j in file[i].split()]
                edges.append([(a[0], a[1]), (a[2], a[3])])
        criptGraph = OrderedDict()
        unCriptGraph = OrderedDict()
        indice = 0
        ordEdges = []
        for i in edges:
            for j in i:
                if not (j in criptGraph.keys()):
                    criptGraph[j] = indice
                    unCriptGraph[indice] = j
                    indice = indice + 1
            ordEdges.append((criptGraph[i[0]], criptGraph[i[1]]))
        graph = {}
        for i in edges:
            if criptGraph[i[0]] in graph.keys():
                graph[criptGraph[i[0]]].append(criptGraph[i[1]])
            else:
                graph[criptGraph[i[0]]] = [criptGraph[i[1]]]
            if criptGraph[i[1]] in graph.keys():
                graph[criptGraph[i[1]]].append(criptGraph[i[0]])
            else:
                graph[criptGraph[i[1]]] = [criptGraph[i[0]]]
        melhorSolucao = GRASP(1000)
        plotar(melhorSolucao, f)
        pprint(melhorSolucao)
        pprint(melhorSolucao.fitness)
