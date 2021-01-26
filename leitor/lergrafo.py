"""Lê o svg e retorna o grafo."""
from bs4 import BeautifulSoup as bs


def dist(x1, x2):
    """."""
    return ((x1 - x2)**2)**(1 / 2)


def dist2pt(x1, y1, x2, y2):
    """."""
    return ((x1 - x2)**2 + (y1 - y2)**2)**(1 / 2)


def ler_grafo(ent, mostra=True):
    """."""
    parse = bs(ent, 'lxml')
    pontos = {}
    print('Poligonos:', len(parse.find_all('polygon')))
    for i in parse.find_all('polygon'):
        points = list(
            map(
                lambda x: tuple(map(float, x)),
                map(
                    lambda x: x.split(','),
                    i.get('points').split()
                )
            )
        )
        for k in range(len(points)):
            if not (points[k] in pontos.keys()):
                pontos[points[k]] = {}
            j = 0 if k + 1 >= len(points) else k + 1
            pontos[points[k]][points[j]] = dist2pt(*points[k], *points[j])
    out = ''
    if mostra:
        print(len(pontos.keys()), sum([len(i) for i in pontos.values()]))
    out += str(len(pontos.keys())) + ' ' + str(sum([len(i) for i in pontos.values()]))
    for i, j in pontos.items():
        for k, l in j.items():
            if mostra:
                print(*i, *k, ("%.2lf" % l))
            out += f"\n{i[0]} {i[1]} {k[0]} {k[1]} " + ("%.2lf" % l)
    return out


if __name__ == "__main__":
    ent = ''
    while True:
        try:
            ent = ent + input()
        except EOFError:
            break
    ler_grafo(ent)
