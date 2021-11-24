
FILE_IN = "input.txt"
FILE_OUT = "out.txt"


class Room():
    def __init__(self, number):
        self.number = number
        self.doors = []

    def __repr__(self):
        return "room: {}, doors: {}".format(self.number, self.doors)

class Door():
    def __init__(self, doorNumber, source, target, price):
        self.doorNumber = doorNumber
        self.source = source
        self.target = target
        self.price = price
    
    def __repr__(self):
        return "doorN: {}".format(self.doorNumber)

class House():
    def __init__(self):
        self.rooms = {}
        self.doors = {}
        self.start = None
        self.outs = []

    def addRoom(self, roomNumber):
        self.rooms[roomNumber] = Room(roomNumber)

    def addDoor(self, doorNumber, source,  price):
        if doorNumber not in self.doors:
            door = Door(doorNumber, source, 0, price)
            self.doors[doorNumber] = door
        else:
            self.doors[dn].target = r

        self.rooms[source].doors.append(self.doors[doorNumber])

    def getDoors(self, roomN):
        return self.rooms[roomN].doors


def readInput():
    with open(FILE_IN, 'r', encoding='utf-8') as f:
        # n - число комнат
        # m - число дверей
        # k - стартовая комната
        # t - количество монет
        n, m, k, t = [int(i) for i in f.readline().split()]
        doors = []

        for i in range(n):
            doors.append([int(i) for i in f.readline().split()])

        prices = [int(i) for i in f.readline().split()]

        # комнаты - узлы
        # двери - грани
        roomsList = {}

        for room, val in enumerate(doors):
            roomsList[room + 1] = val[1:]

        return n, m, k, t, prices, roomsList


def writeOutput(result: bool, totalPrice: int, path: list):
    if result:
        with open(FILE_OUT, 'w') as f:
            f.write('Y\n')
            f.write('{}\n'.format(totalPrice))
            f.write('{}'.format(" ".join([str(i) for i in path])))
    else:
        with open(FILE_OUT, 'w') as f:
            f.write('N\n')


def  findPossibleExits(house):
    """ ищем комнаты, в которых есть дверь, 
        ведущая НЕ в другую комнату"""
    result = [] 
    for r in house.rooms:
        for d in house.rooms[r].doors:
            if d.target == 0:
                result.append(d.doorNumber)
    return result


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight

    def dijkstra2(self, src):
        """ Рассчет стоимости по алг.Дейкстры """
        visited = []
        path = []
        distance = {src: 0}
        node = list(range(self.v))

        # отмечаем стартовый узел посщенным
        node.remove(src)
        visited.append(src)
        path.append(src)
        
        for i in node:
            distance[i] = self.edges[src][i]

        prefer = src
        while node:
            _distance = float('inf')
            for i in visited:
                for j in node:
                    if self.edges[i][j] > 0:
                        if _distance > distance[i] + self.edges[i][j]:
                            _distance = distance[j] = distance[i] + self.edges[i][j]
                            prefer = j
            visited.append(prefer)
            node.remove(prefer)
            path.append(prefer)
        return path, distance[0]

    def dijkstra3(self, src):
        nodes = list(range(self.v))

        visited = [src]
        path = {src:{src:[]}}
        nodes.remove(src)
        distance_graph = {src:0}
        pre = next = src

        while nodes:
            distance = float('inf')
            for v in visited:
                for d in nodes:
                    new_dist = self.edges[src][v] + self.edges[v][d]
                    if new_dist <= distance:
                        distance = new_dist
                        next = d
                        pre = v
                        self.edges[src][d] = new_dist


            path[src][next] = [i for i in path[src][pre]]
            path[src][next].append(next)

            distance_graph[next] = distance

            visited.append(next)
            nodes.remove(next)

        return distance_graph, path

    def dijkstra(self, source):
        target = 0
        processed = []
        costs = {}
        parents = {}

        costs[source] = 0
        parents[source] = 1

        for node in self.edges[source]:
            costs[node] = self.edges[source][node]
            parents[node] = source

        for n, val in enumerate(self.edges):
            if n not in costs and n != source:
                costs[n] = float('inf')
                parents[n] = None

        node = self.find_lowest_cost(costs, processed)

        while node:
            cost = costs[node]
            neigbors = self.edges[node]
            for n, val in enumerate(neigbors):
                new_cost = cost + neigbors[n]
                if new_cost < costs[n]:
                    costs[n] = new_cost
                    parents[n] = node
            processed.append(node)
            node = self.find_lowest_cost(costs, processed)

        final_cost = costs[target]
        result = []
        result.append(target)
        while parents[target] != source:
            result.append(parents[target])
            target = parents[target]
            if target is None:
                break
            
        return final_cost, result

    
    def find_lowest_cost(self, costs, processed):
        lowest_cost = float('inf')
        lowest_cost_node = None
        for node in costs:
            cost = costs[node]
            if cost < lowest_cost and node not in processed:
                lowest_cost = cost
                lowest_cost_node = node
        return lowest_cost_node

# получение входных данных и заполнение "дома"
n, m, startRoom, cash, prices, roomsList = readInput()

house = House()

house.addRoom(0)  # выход как еще одна комната

for roomN in roomsList:
    house.addRoom(roomN)

for r in roomsList:
    for dn in roomsList[r]:
        house.addDoor(dn, r, prices[dn - 1])

house.outs = findPossibleExits(house)

# добавим выходных дверей
for i in house.outs:
    house.doors[i].target = 0
    house.rooms[0].doors.append(house.doors[i])


# а теперь создадим граф, заполним матрицу смежности и найдем путь
g = Graph(n + 1)
for r in house.rooms:
    for d in house.rooms[r].doors:
        g.add_edge(d.source, d.target, d.price)

exitPrice, path = g.dijkstra(startRoom)


writeOutput((exitPrice[0] <= cash), exitPrice, path)

