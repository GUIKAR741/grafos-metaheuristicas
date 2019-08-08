"""Lê o svg e retorna o grafo."""
from bs4 import BeautifulSoup as bs


def dist(x1, x2):
    """."""
    return ((x1-x2)**2)**(1/2)


def dist2pt(x1, y1, x2, y2):
    """."""
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

ent = ''
while True:
    try:
        ent = ent + input()
    except EOFError:
        break
parse = bs(ent, 'lxml')
pontos = {}
l = []
for i in parse.find_all('polygon'):
    if not ('str0' in i.get('class')):
        lvez = []
        for k in list(map(lambda x: x.split(','), i.get('points').split())):
            x1, y1 = list(map(float, k))
            if not ((x1, y1) in pontos.keys()):
                pontos[(x1, y1)] = {}
            lvez.append((x1, y1))
        for j in range(len(lvez)):
            if lvez[(j-1)] != lvez[j]:
                pontos[lvez[j]][lvez[j-1]] = dist2pt(*lvez[j], *lvez[j-1])
            if lvez[0 if j+1 >= len(lvez) else j+1] != lvez[j]:
                pontos[lvez[j]][lvez[0 if j+1 >= len(lvez) else j+1]] = dist2pt(
                    *lvez[j], *lvez[0 if j+1 >= len(lvez) else j+1])
print(len(pontos.keys()), sum([len(i) for i in pontos.values()]))
arr = set()
for i, j in pontos.items():
    for k, l in j.items():
        print(*i, *k, ("%.2lf" % l))
