FILE_IN = "input3.txt"
FILE_OUT = "out3.txt"


OFFSET = 1  # поправка на +1 для счета с 1, для вывода в файл
DEBUG_SHOW_FLOW = False
DEBUG_SHOW_PATH = False


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


def fillData(k, l, edges):
    """ Создание и заполнение графа
        в соответствии с полученными данными
    """
    # создаем "поток"
    g = FF(k)

    # добавляем дополнительные вершины
    g.addVertex('s')
    g.addVertex('t')

    # добавляем k вершин x
    for i in range(k):
        g.addVertex('x' + str(i))

    # добавляем l вершин y
    for i in range(l):
        g.addVertex('y' + str(i))

    # добавляем грани соединяющие вершину s с вершинами x
    for i in range(k):
        g.addEdge('s', 'x' + str(i), 1)

    # добавляем грани соединяющие вершину t с вершинами y
    for i in range(l):
        g.addEdge('y' + str(i), 't', 1)

    # добавляем грани между x и y, определенные во входном файле
    for counter_i, i in enumerate(edges):  # для каждого перечня граней от вершины i(x)
        for counter_j, value in enumerate(i):   # к вершинам j(y)
            if value != 0:  # если значение 0, значит от вершины нет граней
                x = 'x' + str(counter_i)
                y = 'y' + str(value - 1)
                g.addEdge(x, y, 1)

    return g


class Edge():
    def __init__(self, u, v, w):
        self.source = u
        self.target = v
        self.capacity = w

    def __repr__(self) -> str:
        """ переопределение для вывода """
        return "({} -> {}) cap: {}".format(self.source, self.target, self.capacity)


class FF():
    def __init__(self, size):
        self.size = size
        self.adj = {}
        self.flow = {}
        self.initialGraph = {}

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

    def printFlow(self):
        if DEBUG_SHOW_FLOW:
            for key in self.flow:
                print('key:{} flow:{}'.format(key, self.flow[key]))

    def printPath(self, text, path):
        if DEBUG_SHOW_PATH:
            print('{} {}'.format(text, path))


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

            self.printPath('initial path : ', path)
            self.printFlow()

            while path != None:
                flow = min(res for edge, res in path)
                # print("counted flow: {}".format(flow))

                for edge, res in path:
                    self.flow[edge] += flow
                    self.flow[edge.redge] -= flow

                self.printFlow()

                path = self.findPath(source, target, [])
                self.printPath('path inside of while loop:', path)

            edges = self.getEdges(source)
            result = sum(self.flow[edge] for edge in edges)

            return result

    def getPairs(self):
        """ Перебираем сформированный поток,
            удаляем добавленные вершины s и t,
            берем только те грани, по которым пошел поток ( flow == 1) """
        for fl in self.flow:
            if (fl.source not in ('s', 't')):
                if (fl.target not in ('s', 't')):
                    if self.flow[fl] == 1:
                        self.initialGraph[fl] = self.flow[fl]

    def prepareResultList(self):
        self.getPairs()
        result = [0] * self.size

        for edge in self.initialGraph:
            sourceId = int(edge.source[1:])  # обрезаем x и переводим в число
            targetId = int(edge.target[1:])  # обрезаем y и переводим в число
            result[sourceId] = targetId + OFFSET

        return result


if __name__ == "__main__":
    k, l, data_size, edges = readInput()
    # edges // считанные из файла грани
    # 0:[1, 2, 3, 4]
    # 1:[1, 2, 3]
    # 2:[1, 2]
    # 3:[1]

    g = fillData(k, l, edges)

    maxFlow = g.maxFlow('s', 't')  # считаем максимальный поток для заданной системы
    print("Max flow: {}".format(maxFlow))

    pp = g.prepareResultList()

    writeOutput(pp)