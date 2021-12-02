
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


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[0 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight

    def shortWay(self, source):
        target = 0
        processed = []
        costs = {}
        parents = {}

        costs[source] = 0
        parents[source] = 1

        for node, val in enumerate(self.edges[source]):
            if val > 0:
                costs[node] = self.edges[source][node]
                parents[node] = source

        # for n in graph.keys():
        for n in range(self.v):
            if n not in costs and n != source:
                costs[n] = float('inf')
                parents[n] = None

        node = self.find_lowest_cost(costs, processed)

        while node:
            cost = costs[node]
            neigbors = self.edges[node] # [0, 2, 0, 0]
            # for n in neigbors.keys():
            for n, val in enumerate(neigbors):
                # добавить отфильтрацию с ценой 0 (когда нет грани)
                if val > 0:
                    new_cost = cost + neigbors[n]
                    if new_cost < costs[n]:
                        costs[n] = new_cost
                        parents[n] = node
            processed.append(node)
            node = self.find_lowest_cost(costs, processed)

        # пройти по parents и собрать путь от финиша к старту
        final_cost = costs[target]
        result = []

        while parents[target] != source:
            result.append(parents[target])
            target = parents[target]
            if target is None:
                break

        result.append(source)
        result.reverse()
        
        return final_cost, result
    
    def find_lowest_cost(self, costs, processed):
        lowest_cost = float('inf')
        lowest_cost_node = None
        for node in costs:
            cost = costs[node]
            # ?? добавить фильтр на 0 стоимость
            if cost < lowest_cost and node not in processed:
                lowest_cost = cost
                lowest_cost_node = node
        return lowest_cost_node


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


        prices_raw = f.readlines()
        prices = []
        for price_line in prices_raw:
            raw_price_line = [int(i) for i in price_line.split()]
            for i in raw_price_line:
                prices.append(i)

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

exitPrice, path = g.shortWay(startRoom)


writeOutput((exitPrice <= cash), exitPrice, path)

