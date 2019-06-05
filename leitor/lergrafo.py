"""."""
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt


def dist(x1, x2):
    """."""
    return ((x1-x2)**2)**(1/2)

ent = ''
while True:
    try:
        ent = ent + input()
    except EOFError:
        break
parse = bs(ent, 'lxml')
pontos = []
vertices = set()
par = []
for i in parse.find_all('polygon'):
    if not ('str0' in i.get('class')):
        par.append([[], []])
        for k in list(map(lambda x: x.split(','), i.get('points').split())):
            par[-1][0].append(float(k[0]))
            par[-1][1].append(float(k[1]))
        for j in list(map(lambda x: x.split(','), i.get('points').split())):
            conv = []
            x1, y1 = list(map(float, j))
            for k in j:
                conv.append(float(k))
                vertices.add(float(k))
            pontos.append(conv)
print(len(vertices), len(pontos))
for i in pontos:
    print("%d %d %.2lf" % (*i, dist(*i)))
for i in par:
    i[0].append(i[0][0])
    i[1].append(i[1][0])
    plt.plot(i[0], i[1])
plt.grid(True)
plt.show()
