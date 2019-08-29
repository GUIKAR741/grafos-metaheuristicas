"""."""
from pprint import pprint
v, a = [int(i) for i in input().split()]
vertices = []
for i in range(v):
    vertices.append([float(i) for i in input().split(',')])
arestas_ = []
for i in range(a):
    arestas_.append([int(i) for i in input().split()[0].split('-')])
arestas = []
for i in arestas_:
    # print(i, (vertices[i[0] - 1], vertices[i[1] - 1]))
    arestas.append((vertices[i[0] - 1], vertices[i[1] - 1]))
print(len(arestas))
for i in arestas:
    print(*i[0], *i[1])
