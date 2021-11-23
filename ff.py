# https://www.programiz.com/dsa/ford-fulkerson-algorithm
from collections import defaultdict


FILE_IN = "input.txt"
FILE_OUT = "out.txt"


def read_input():
    with open(FILE_IN, 'r', encoding='utf-8') as f:
        k, l = f.readline().split()
        data_size = int(f.readline())  # считываем количество элементов массива, можно применить например для проверки
        data = f.read()
        adjucency_arr = [int(i) for i in data.split()]  # генератор и сплит - простой способ

        edges = []

        for i in range(adjucency_arr[0] - 1):  # ограничение о обработке массива
            start = adjucency_arr[i] - 1  # индекс начала перечня граней
            stop = adjucency_arr[i + 1]

            if adjucency_arr[start] == 32767:
                break

            verticals = adjucency_arr[start : stop - 1]
            edges.append(verticals)

        return int(k), int(l), data_size, edges


class Graph:

    def __init__(self, graph):
        self.graph = graph
        self.graphSize = len(graph)


    def bfs(self, source, target, parent):
        """ поиск в ширину """
        queue = []
        visited = [False] * (self.graphSize)

        queue.append(source)
        visited[source] = True

        while queue:
            currentVertex = queue.pop(0)

            edges = self.graph[currentVertex]

            # gVertex - номер вершины графа
            # hasEdge == 1 или 0, в зависимости если или нет грань между вершинами
            for gVertex, hasEdge in enumerate(edges):
                # если вершину еще не проверяли и есть грань с целевой вершиной (смежны)
                if visited[gVertex] == False and hasEdge > 0:
                    queue.append(gVertex)
                    visited[gVertex] = True
                    parent[gVertex] = currentVertex

        return True if visited[target] else False

    def ford_fulkerson(self, source, target):
        parent = [-1] * (self.graphSize)
        max_flow = 0  # начальный поток == 0

        # пока мы можем найти "дополняющий путь", по которому можно пустить еще немного "вещества"
        while self.bfs(source, target, parent):
            path_flow = float("Inf")
            s = target

            while(s != source):
                qq = self.graph[parent[s]][s]
                path_flow = min(path_flow, qq)  # получаем величину пути
                s = parent[s]

            max_flow += path_flow  # увеличиваем поток на величину пути


            # обновляем остаточные пропускную способность граней/"труб"
            # update residual capacities of the edges
            # and reverse edges along the path
            v = target

            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        for i in self.graph:
            print(i)
        print()

        return max_flow


if __name__ == "__main__":
    k, l, data_size, edges = read_input()

    # edges // считанные грани
    # 0:[1, 2, 3, 4]
    # 1:[1, 2, 3]
    # 2:[1, 2]
    # 3:[1]

    # создаем список списков c нулями
    size = k + l + 2
    graph = [[0 for _ in range(size)] for __ in range(size)]

    # S
    for i in range(k):
        graph[0][i + 1] = 1
        graph[i + 1][0] = 1

    # T
    for i in range(l):
        graph[-1][i + k + 1] = 1
        graph[i + k + 1][-1] = 1

    # заполняем
    for counter, i in enumerate(edges):
        for j in i:
            graph[counter + 1][j + k] = 1
            graph[j + k][counter + 1] = 1

    # graph // матрица "смежности"?
    # 0:[0, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    # 1:[1, 0, 0, 0, 0, 1, 1, 1, 1, 0]
    # 2:[1, 0, 0, 0, 0, 1, 1, 1, 0, 0]
    # 3:[1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
    # 4:[1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    # 5:[0, 1, 1, 1, 1, 0, 0, 0, 0, 1]
    # 6:[0, 1, 1, 1, 0, 0, 0, 0, 0, 1]
    # 7:[0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
    # 8:[0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    # 9:[0, 0, 0, 0, 0, 1, 1, 1, 1, 0]

    g = Graph(graph)

    source = 0
    sink = k + l + 1 # = 9

    print("Max Flow: %d " % g.ford_fulkerson(source, sink))


    # print(graph)
    # print(edges)
