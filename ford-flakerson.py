# Цель:
#   Найти наибольшее паpосочетание в двудольном гpафе

# Метод решения:
#   сведение к задаче о максимальном потоке и использование
# алгоpитма Фоpда-Фалкеpсона.


# Файл входных данных:
#   Двудольный гpаф G=(X,Y,E), k=|X|, l=|Y|, заданный Х-массивом смежностей.

#   X-массив смежностей:
#   * также как и массив смежностей, только перечисляются смежные с вершинами x из X.
#   * Для изолиpованной веpшины индекс в массиве pавен 0.
#   * В пеpвой стpоке файла числа k l.
#   * Во втоpой pазмеp массива.
#   * Далее pасположен массив смежности ( не более 10 чисел в одной стpоке).
#   * Последний элемент массива pавен 32767.


# Файл выходных данных:
#   Массив XПАРА длины k (XПАРА[xi]=yj,
#       если {xi,yj} входит в паросочетание,
#       иначе XПАРА[xi]=0).


FILE_IN = "input.txt"
FILE_OUT = "out.txt"


class Edge():
    def __init__(self, u, v, w):
        self.source = u
        self.target = v
        self.capacity = w

    def __repr__(self) -> str:
        """ переопределение для вывода """
        return "({} -> {}) cap: {}".format(self.source, self.target, self.capacity)


class FlowNetwork():
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



# Считываем входные данные
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


if __name__ == "__main__":
    k, l, data_size, edges = read_input()
    print(edges)


    # создаем "поток"
    g = FlowNetwork()


    # заводим вершины
    g.addVertex('s')
    g.addVertex('t')

    for i in range(k):
        g.addVertex('k' + str(i))

    for i in range(l):
        g.addVertex('l' + str(i))


    # заводим грани/трубы
    for i in range(k):
        g.addEdge('s', 'k' + str(i), 1)

    for i in range(l):
        g.addEdge('l' + str(i), 't', 1)


    for counter_i, i in enumerate(edges):  # для каждого перечня граней от вершины i(x)
        for counter_j, j in enumerate(i):   # к вершинам j(y)
            x = 'k' + str(counter_i)
            y = 'l' + str(counter_j)
            g.addEdge(x, y, 1)



    print (g.maxFlow('s', 't'))