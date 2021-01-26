"""."""
from sympy import Point, Segment
from sympy.geometry import intersection
from matplotlib import pyplot as plt


def separaArestas(p1, p2, p3, p4=None):
    """."""
    arestas_separadas = []
    if p1 != p2:
        arestas_separadas.append(Segment(Point(p1.x, p1.y), Point(p2.x, p2.y)))
    if p2 != p3:
        arestas_separadas.append(Segment(Point(p2.x, p2.y), Point(p3.x, p3.y)))
    if p3 != p4 and not (p4 is None):
        arestas_separadas.append(Segment(Point(p3.x, p3.y), Point(p4.x, p4.y)))
    return arestas_separadas


def midPoint(x1, y1, x2, y2):
    """."""
    return (x1 + x2) / 2, (y1 + y2) / 2


def partir(ent, mostra=True, plotar=False):
    """."""
    n = int(ent[0][1])
    ent.pop(0)
    arestas = []
    for i in range(n):
        a = ent[i]
        arestas.append(Segment(Point(a[0], a[1]), Point(a[2], a[3])))
    arestas_teste = list(arestas)
    arestas_final = []
    i, j = 0, 0
    while i < len(arestas_teste):
        l1 = arestas_teste[i]
        j = 1
        add_final = True
        while j < len(arestas_teste):
            l2 = arestas_teste[j]
            if l1.contains(l2):
                ordenado = separaArestas(*sorted([l1.p1, l1.p2, l2.p1, l2.p2],
                                                 key=lambda a: (a.x, a.y)))
                [arestas_teste.append(k) for k in ordenado]
                arestas_teste.pop(j)
                add_final = False
                break
            elif len(intersection(l1, l2)) > 0:
                ponto_intersecao = intersection(l1, l2)[0]
                # Entra aqui se o ponto estiver no meio do segmento
                if not (ponto_intersecao in [l1.p1, l1.p2] and ponto_intersecao in [l2.p1, l2.p2]):
                    if ponto_intersecao in [l1.p1, l1.p2]:
                        add_final = False
                        ordenado = separaArestas(l2.p1, ponto_intersecao, l2.p2)
                        ordenado += [l1]
                        [arestas_teste.append(k) for k in ordenado]
                        arestas_teste.pop(j)
                        continue
                    elif ponto_intersecao in [l2.p1, l2.p2]:
                        add_final = False
                        ordenado = separaArestas(l1.p1, ponto_intersecao, l1.p2)
                        [arestas_teste.append(k) for k in ordenado]
                        break
            j += 1
        if add_final:
            arestas_final.append(l1)
        arestas_teste.pop(0)
        i = 0
    set_arestas_final = set()
    for i in arestas_final:
        if not((i.p1.x, i.p1.y, i.p2.x, i.p2.y) in set_arestas_final or (i.p2.x, i.p2.y,
                                                                         i.p1.x, i.p1.y)
               in set_arestas_final):
            set_arestas_final.add((float(i.p1.x), float(
                i.p1.y), float(i.p2.x), float(i.p2.y)))
    arestas_final = set_arestas_final
    out = str(len(arestas_final))
    if mostra:
        print(len(arestas_final))
    for i in arestas_final:
        out += f'\n{i[0]} {i[1]} {i[2]} {i[3]}'
        if mostra:
            print(*i)
            # print(float(i.p1.x), float(i.p1.y), float(i.p2.x), float(i.p2.y))
    if plotar:
        X = []
        Y = []
        for p1x, p1y, p2x, p2y in arestas_final:
            X.append(p1x)
            X.append(p2x)
            Y.append(p1y)
            Y.append(p2y)
        minimoX = min(X)
        maximoX = max(X)
        minimoY = min(Y)
        maximoY = max(Y)
        plt.xlim(minimoX - 1, maximoX + 1)
        plt.ylim(minimoY - 1, maximoY + 1)
        j = 1
        for p1x, p1y, p2x, p2y in arestas_final:
            plt.plot([p1x, p2x], [p1y, p2y], color="red")
            plt.annotate(str(j), midPoint(p1x, p1y, p2x, p2y))
            # plt.savefig(f'img/g{j}.png')
            j += 1
        plt.show()
    return out


if __name__ == "__main__":
    ent = [[int(i)] for i in input().split()]
    while True:
        try:
            ent.append([float(i) for i in input().split()])
        except EOFError:
            break
    partir(ent)
