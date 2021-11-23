FILE_IN = "input5.txt"
FILE_OUT = "out5.txt"


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

class Edge():
    def __init__(self, u, v, w):
        self.source = u
        self.target = v
        self.capacity = w

    def __repr__(self) -> str:
        """ переопределение для вывода """
        return "({} -> {}) cap: {}".format(self.source, self.target, self.capacity)


class FF():
    def __init__(self):
        self.adj = {}
        self.flow = {}
    
    def addVertex(self, vertex):
        self.adj[vertex] = []

    def getEdges(self, vertex):
        return self.adj[vertex]

    def addEdge(self, u, v, w = 0):
        if u == v:
            raise ValueError("u == v")

        edge = Edge(u, v, w)  # "прямой" путь
        redge = Edge(v, u, 0)  # "обратный" путь
        edge.redge = redge
        redge.redge = edge

        self.adj[u].append(edge)
        self.adj[v].append(redge)

        self.flow[edge] = 0
        self.flow[redge] = 0

    def findPath(self, source, target, path):
        """ Формируем путь """
        if source == target:
            return path

        edges = self.getEdges(source)
        for edge in edges:
            # считаем разность между емкостью трубы и текущим потоком
            residual = edge.capacity - self.flow[edge]

            if residual > 0 and not (edge, residual) in path:
                result = self.findPath(edge.target, target, path + [(edge, residual)])

                if result != None:
                    return result
        
    def maxFlow(self, source, target):
            """ Считаем максимальный поток """
            path = self.findPath(source, target, [])
            print('path after enter MaxFlow: {}'.format(path))

            for key in self.flow:
                print('key:{} flow:{}'.format(key, self.flow[key]))

            print('-' * 20)

            while path != None:
                flow = min(res for edge, res in path)
                print("counted flow: {}".format(flow))

                for edge, res in path:
                    self.flow[edge] += flow
                    self.flow[edge.redge] -= flow

                for key in self.flow:
                    print('{}:{}'.format(key, self.flow[key]))

                path = self.findPath(source, target, [])
                print('path inside of while loop: %s' % path)

            print("ending")
            for key in self.flow:
                print('key:{} flow:{}'.format(key, self.flow[key]))

            print("debug")
            edges = self.getEdges(source)
            for edge in edges:
                print("edge: {}, flow: {}".format(edge, self.flow[edge]))

            result = sum(self.flow[edge] for edge in edges)

            return result




if __name__ == "__main__":
    k, l, data_size, edges = readInput()
    # edges // считанные из файла грани
    # 0:[1, 2, 3, 4]
    # 1:[1, 2, 3]
    # 2:[1, 2]
    # 3:[1]

    # задаём "поток"
    g = FF()

    # заводим вершины
    g.addVertex('s')
    g.addVertex('t')

    for i in range(k):
        g.addVertex('x' + str(i))

    for i in range(l):
        g.addVertex('y' + str(i))


    # заводим грани/трубы
    for i in range(k):
        g.addEdge('s', 'x' + str(i), 1)

    for i in range(l):
        g.addEdge('y' + str(i), 't', 1)


    for counter_i, i in enumerate(edges):  # для каждого перечня граней от вершины i(x)
        for counter_j, j in enumerate(i):   # к вершинам j(y)
            x = 'x' + str(counter_i)
            y = 'y' + str(counter_j)
            g.addEdge(x, y, 1)



    print (g.maxFlow('s', 't'))