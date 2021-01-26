"""."""
from lergrafo import ler_grafo
from particao_arestas import partir
import matplotlib.pyplot as plt


class Grafo:
    """."""

    def __init__(self, v, e):
        """."""
        self._g = {}
        self.v = v
        self.e = e

    def addAresta(self, v1: (int or float), v2: (int or float), p: (int or float) = 0):
        """."""
        if not (v1 in self._g.keys()):
            self._g[v1] = {}
        self._g[v1][v2] = p

    @property
    def g(self):
        """."""
        return self._g

    @property
    def clique(self):
        """."""
        gg = Grafo(self.v, self.e)
        for i in self._g.keys():
            for j in self._g[i].keys():
                gg.addAresta(i, j)
        for i in gg.g.keys():
            for j in gg.g.keys():
                if i != j:
                    gg.addAresta(i, j)
        return [([*i, *j]) for j in gg.g[i].keys() for i in gg.g.keys()]
        # return []

    def __repr__(self):
        """."""
        return str(self._g)


def plotar(grafo):
    """."""
    def midPoint(x1, y1, x2, y2):
        """."""
        return (x1 + x2) / 2, (y1 + y2) / 2

    plt.close()
    for j, i in enumerate(grafo[1:]):
        plt.plot([i[0], i[2]], [i[1], i[3]], "-", color="red")
        plt.annotate(str(j), midPoint(i[0], i[1], i[2], i[3]))
    plt.show()


def ler(ent):
    """."""
    return [[float(j) for j in i.split()] for i in ent.split('\n')]


if __name__ == "__main__":
    ent = ''
    while True:
        try:
            ent += input()
        except EOFError:
            break
    # print("LENDO")
    ent = ler_grafo(ent, mostra=False)
    ent = ler(ent)
    v = ent[0][0]
    print("VERTICES:", int(ent[0][0]), "ARESTAS:", int(ent[0][1]))

    # print("CORTANDO")
    # ent = cortar(ent, mostra=False)
    # ent = ler(ent)
    # print("ARESTAS:", int(*ent[0]))

    # g = Grafo(v, len(ent[1:]))
    # for i in ent[1:]:
    #     g.addAresta((i[0], i[1]), (i[2], i[3]))
    # print("CLIQUE:", len(g.clique))

    # print("PARTINDO")
    ent = partir(ent, mostra=False)
    ent = ler(ent)
    print("ARESTAS:", int(ent[0][0]))
    # g = Grafo(v, len(ent[1:]))
    # for i in ent[1:]:
    #     g.addAresta((i[0], i[1]), (i[2], i[3]))
    # print("CLIQUE:", len(g.clique))
