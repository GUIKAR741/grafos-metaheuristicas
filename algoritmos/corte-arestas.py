"""."""
from random import shuffle
from pprint import pprint
import matplotlib.pyplot as plt
print, pprint = pprint, print


def dist2pt(x1, y1, x2, y2):
    """."""
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)


def CriaGrafo() -> dict:
    """Recebe e cria o Grafo."""
    ve = [int(i) for i in input().split()]
    grafo = dict()
    ent = []
    while ve[1] > 0:
        ent.append([float(k) for k in input().split()])
        grafo[(ent[-1][0], ent[-1][1])] = {}
        ve[1] -= 1
    for k in ent:
        grafo[(k[0], k[1])][(k[2], k[3])] = k[4]
    return grafo


def corta(g: dict, pi: (int or float), mi: (int or float)):
    """Corta as arestas do grafo.

    args:
    g -> grafo
    pi -> velocidade do corte
    mi -> velocidade do deslocamento
    """
    somatorio = []
    arestas = [(i, j) for i in g.keys() for j in g[i]]
    cortadas = []
    shuffle(arestas)
    x, y = [], []
    for i in range(len(arestas)):
        if not(arestas[i] in cortadas or (arestas[i][1], arestas[i][0]) in cortadas):
            if i == 0:
                somatorio.append((g[arestas[i][0]][arestas[i][1]])/pi)
            else:
                if arestas[i-1][1] == g[arestas[i][0]]:
                    somatorio.append((g[arestas[i][0]][arestas[i][1]])/pi)
                else:
                    somatorio.append(
                        (dist2pt(*arestas[i-1][1], *arestas[i][0]))/mi +
                        (g[arestas[i][0]][arestas[i][1]])/pi)
            x.append(arestas[i][0][0])
            y.append(arestas[i][0][1])
            x.append(arestas[i][1][0])
            y.append(arestas[i][1][1])
            cortadas.append(arestas[i])
            plt.plot(x, y)
    plt.grid(True)
    plt.show()
    return sum(somatorio)


g = CriaGrafo()
print(corta(g, 1, 5))
