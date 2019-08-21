"""."""
# from Geometry import Point, Line, Segment
# from Geometry.exceptions import CollinearLines
from sympy import Point, Segment
from sympy.geometry import intersection
from pprint import pprint
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


def partir(ent, mostra=True):
    """."""
    n = int(ent[0][0])
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
            if l1.contains(l2) or l2.contains(l1):
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
    out = str(len(arestas_final))
    if mostra:
        print(len(arestas_final))
    for i in arestas_final:
        out += f'\n{i.p1.x} {i.p1.y} {i.p2.x} {i.p2.y}'
        if mostra:
            print(i.p1.x, i.p1.y, i.p2.x, i.p2.y)
    plt.xlim(-1, 40)
    plt.ylim(-1, 40)
    j = 1
    for i in arestas_final:
        plt.plot([i.p1.x, i.p2.x], [i.p1.y, i.p2.y])
        plt.savefig(f'img/{j}.png')
        j += 1
    return out


if __name__ == "__main__":
    ent = [[int(i)] for i in input().split()]
    while True:
        try:
            ent.append([float(i) for i in input().split()])
        except EOFError:
            break
    partir(ent)

    # print(sorted([Point(1, 1), Point(6, 1), Point(4, 1), Point(8, 5)], key=lambda a: (a.x, a.y)))
    # print(Line(Point(1, 1), Point(6, 1)).isCollinear(Line(Point(6, 1), Point(6, 5))))
    # try:
    #     print(Line(Point(1, 1), Point(6, 1)).intersection(Line(Point(6, 1), Point(6, 5))))
    # except:
    #     ..
    # print(Segment(Point(4, 2), Point(8, 2)).contains(Segment(Point(5, 2), Point(5, 7))))
    # print(Segment(Point(4, 2), Point(8, 2)).p1.x)
    # print(Segment(Point(4, 2), Point(8, 2)).p1.y)
    # print(intersection(Segment(Point(4, 2), Point(8, 2)), Segment(Point(5, 2), Point(8, 2))))
