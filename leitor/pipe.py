"""."""
from lergrafo import ler_grafo
from corte_arestas import cortar
from particao_arestas import partir


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
    ent = ler_grafo(ent, mostra=False)
    ent = ler(ent)
    ent = cortar(ent, mostra=False)
    # print(ent)
    ent = ler(ent)
    partir(ent, mostra=True)
