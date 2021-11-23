# Python program to find
# maximal Bipartite matching.
# https://www.geeksforgeeks.org/maximum-bipartite-matching/


from ff import Graph


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
    def __init__(self, graph, k, l):
        self.graph = graph  # residual graph
        self.k = k
        self.l = l

    def bpm(self, u, matchR, visited):
        """ модифицированный рекурсивный поиск в ширину,
            возвращает True, если есть соответствие вершине """

        # для всех вершин в 'l'
        for vertex in range(self.l):
            # смежные вершины (есть грань)
            isAdjacent = bool(self.graph[u][vertex])
            # вершина не проверялась
            isNotVisited = visited[vertex] == False

            if isAdjacent and isNotVisited:
                # отмечаем вершину проверенной
                visited[vertex] = True

                '''If job 'vertex' is not assigned to an applicant
                OR
                previously assigned applicant for job v (which is matchR[v]) has an alternate job available.

                Since v is marked as visited in the above line, matchR[v] in the following
                recursive call will not get job 'v' again'''
                if matchR[vertex] == -1 or self.bpm(matchR[vertex], matchR, visited):
                    matchR[vertex] = u
                    return True
        return False


    def findMaxPairs(self):
        """ поиск паросочетаний и подсчет их количества """
        # список с перечнем совпадений пар (xi; yi),
        # где i - номер элемента x, matches[i] - номер элемента y,
        # если у x нет пары ->  matches[i] == -1
        matches = [-1] * self.l
        # Счетчик найденных пар
        matchCount = 0

        # для каждой вершины k
        for i in range(self.k):
            # отметим все вершины не посещенными
            visited = [False] * self.l
            # и пойдем проверять, удастся ли найти пару из вершин l
            if self.bpm(i, matches, visited):
                matchCount += 1
        return matches, matchCount


if __name__ == "__main__":
    k, l, data_size, edges = read_input()

    # edges // считанные из файла грани
    # 0:[1, 2, 3, 4]
    # 1:[1, 2, 3]
    # 2:[1, 2]
    # 3:[1]

    # создаем список списков c нулями
    graph = [[0 for _ in range(k)] for __ in range(l)]

    for counter, i in enumerate(edges):
        for j in i:
            graph[counter][j - 1] = 1

    g = Graph(graph, k, l)
    print ("Maximum number of applicants that can get job is %d " % g.findMaxPairs())

