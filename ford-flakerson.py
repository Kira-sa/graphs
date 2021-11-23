# Цель:
#   Найти наибольшее паpосочетание в двудольном гpафе

# Метод решения: сведение к задаче о максимальном потоке и использование 
# алгоpитма Фоpда-Фалкеpсона.
 

# Файл входных данных:
#   Двудольный гpаф G=(X,Y,E), k=|X|, l=|Y|, заданный Х-массивом смежностей.

#   X-массив смежностей:  
#   * также как и массив смежностей,  только перечисляются смежные с вершинами x из X.  
#   * Для изолиpованной веpшины индекс в массиве pавен 0.
#   * В пеpвой стpоке файла числа k l.  
#   * Во втоpой pазмеp массива. 
#   * Далее pасположен массив смежности (  не  более  10  чисел  в  одной  стpоке).
#   * Последний элемент массива pавен 32767.
 

# Файл выходных данных:
#   Массив XПАРА длины k (XПАРА[xi]=yj,  
#       если {xi,yj} входит в паросочетание, 
#       иначе XПАРА[xi]=0).


from collections import defaultdict
from math import ulp
from os import supports_bytes_environ
import numpy


FILE_IN = "ford_flakerson\input.txt"
FILE_OUT = "out.txt"


# class Graph:
#     def __init__(self, k, l):
#         self.k= k  # количество вершин x
#         self.l = l  # количество вершин y
#         self.graph = defaultdict(list)  # словарь для хранения графа

#     def addEdge(self, v, w):
#         """ Функция добавления грани графа (двустороннее) """
#         self.graph[v].append(w)  #Add w to v_s list
#         self.graph[w].append(v)  #Add v to w_s list
        
class Edge():
    def __init__(self, u, v, w):
        self.source = u
        self.target = v
        self.capacity = w
        # self.redge = none

    def __repr__(self) -> str:
        return "%s -> %s : %s" % (self.source, self.target, self.capacity)


class FlowNetwork():
    def __init__(self):
        self.adj = {}
        self.flow = {}

    def addVertex(self, vertex):
        self.adj[vertex] = []
    
    def getEdges(self, v):
        return self.adj[v]
    
    def addEdge(self, u, v, w = 0):
        if u == v:
            raise ValueError("u == v")

        edge = Edge(u, v, w)
        redge = Edge(v, u, 0)
        edge.redge = redge
        redge.redge = edge

        self.adj[u].append(edge)
        self.adj[v].append(redge)

        self.flow[edge] = 0
        self.flow[redge] = 0
    
    def findPath(self, source, target, path):
        if source == target:
            return path
        
        for edge in self.getEdges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge, residual) in path:
                result = self.findPath(edge.target, target, path + [(edge, residual)])
                if result != None:
                    return result
    
    def maxFlow(self, source, target):
        path = self.findPath(source, target, [])
        print('path after enter MaxFlow: %s' % path)
        for key in self.flow:
            print ('%s:%s' % (key,self.flow[key]))
        print('-' * 20)

        while path != None:
            flow = min(res for edge, res in path)
            for edge, res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            for key in self.flow:
                print('%s:%s' % (key,self.flow[key]))
            path = self.FindPath(source, target, [])
            print('path inside of while loop: %s' % path)
        for key in self.flow:
            print('%s:%s' % (key,self.flow[key]))
        return sum(self.flow[edge] for edge in self.getEdges(source))



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

# qwe = read_input()

# print(qwe)
# Что-то делаем
def doSomething():
    pass

# Выводим результат в файл
def out_processing(graph, weight):
    """ Подготовка данных к записи и вывод в файл """
    pass


if __name__ == "__main__":
#   g = FlowNetwork()
#   map(g.AddVertex, ['s', 'o', 'p', 'q', 'r', 't'])
#   g.AddEdge('s', 'o', 5)
#   g.AddEdge('s', 'p', 3)
#   g.AddEdge('o', 'p', 2)
#   g.AddEdge('o', 'q', 3)
#   g.AddEdge('p', 'r', 4)
#   g.AddEdge('r', 't', 3)
#   g.AddEdge('q', 'r', 4)
#   g.AddEdge('q', 't', 2)
#   print (g.MaxFlow('s', 't'))
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
        g.addEdge('s', 'k' + str(i), 0)
    
    for i in range(l):
        g.addEdge('l' + str(i), 't', 0)


    for counter_i, i in enumerate(edges):  # для каждого перечня граней от вершины i(x)
        for counter_j, j in enumerate(i):   # к вершинам j(y)
            x = 'k' + str(counter_i)
            y = 'l' + str(counter_j)
            g.addEdge(x, y, 0)



    print (g.maxFlow('s', 't'))