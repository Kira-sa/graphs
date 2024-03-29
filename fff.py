FILE_IN = "input4.txt"
FILE_OUT = "out4.txt"


def readInput():
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


def writeOutput(matches: list):
    result = "[" + ", ".join(str(i) for i in matches) + "]"

    with open(FILE_OUT, 'w') as f:
        f.write(result)


class Graph:
    def __init__(self, graph, k, l):
        self.graph = graph  # residual graph
        self.k = k
        self.l = l

    def bpm(self, u, match, visited):
        """ модифицированный рекурсивный поиск в ширину,
            возвращает True, если есть соответствие вершине """

        # для всех вершин в 'l'
        for vertex in range(self.l):
            if self.graph[u][vertex]:  # смежные вершины (есть грань)
                if not visited[vertex]:  # вершина не проверялась
                    # отмечаем вершину проверенной
                    visited[vertex] = True

                    """
                    если вершине l не подобрано паросочетание, то сочетаем ее
                    с вершиной vertex (из k) и возвращаем True.

                    если для подходящей вершины vertex уже подобрано паросочетание
                    - рекурсивно ищем альтернативу для этой вершины
                    """
                    if match[vertex] == -1 or self.bpm(match[vertex], match, visited):
                        match[vertex] = u
                        return True
        return False


    def findMaxPairs(self):
        """ поиск паросочетаний и подсчет их количества """
        matches = [-1] * self.l

        # Счетчик найденных пар
        matchCount = 0

        # для каждой вершины k
        for xi in range(self.k):

            # отметим все вершины не посещенными
            visited = [False] * self.l

            # и пойдем проверять, удастся ли найти пару из вершин l
            if self.bpm(xi, matches, visited):
                matchCount += 1

        return matches, matchCount
    
    def reverse(self, matches):
        res = [0] * len(matches)
        for pos, index in enumerate(matches):
            if index != 0:
                res[index - 1] = pos + 1
        return res



if __name__ == "__main__":
    k, l, data_size, edges = readInput()

    # edges // считанные из файла грани
    # 0:[1, 2, 3, 4]
    # 1:[1, 2, 3]
    # 2:[1, 2]
    # 3:[1]

    # создаем список списков c нулями
    graph = [[0 for _ in range(k)] for __ in range(l)]

    for counter, i in enumerate(edges):
        for j in i:
            if j != 0:
                graph[counter][j - 1] = 1

    g = Graph(graph, k, l)

    reversedMatches, matchCount = g.findMaxPairs()  # matches = [4, 3, 2, 1], matchCount = 4
    reversedMatches = [i + 1 for i in reversedMatches]
    matches = g.reverse(reversedMatches)

    writeOutput(matches)

