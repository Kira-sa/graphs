
from os import pardir, read


with open("test_1.txt", 'r') as f:
    data_in = f.readlines()
n = int(data_in[0])
assert n > 0
# g = [{} for i in range(n)]
graph = {}
for i in range(n):
    buf = [int(i) for i in data_in[i + 1].split()]
    buf.pop()
    buf_dictionary = {}
    for j in range(0, len(buf), 2):
        # destination = buf[j]
        # cost =  buf[j + 1]
        buf_dictionary[buf[j]] = buf[j + 1]
    graph[i + 1] = buf_dictionary

source = int(data_in[-2])
target = int(data_in[-1])

processed = []
costs = {}
parents = {}

costs[source] = 0
parents[source] = 1

for node in graph[source]:
    costs[node] = graph[source][node]
    parents[node] = source

for n in graph.keys():
    if n not in costs and n != source:
        costs[n] = float('inf')
        parents[n] = None

def find_lowest_cost(costs):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

node = find_lowest_cost(costs)

while node:
    cost = costs[node]
    neigbors = graph[node]
    for n in neigbors.keys():
        new_cost = cost + neigbors[n]
        if new_cost < costs[n]:
            costs[n] = new_cost
            parents[n] = node
    processed.append(node)
    node = find_lowest_cost(costs)

# пройти по parents и собрать путь от финиша к старту
final_cost = costs[target]
result = []
result.append(target)
while parents[target] != source:
    result.append(parents[target])
    target = parents[target]
    if target is None:
        break

with open("out_1.txt", 'w') as f:
    if target is None:
        f.write("N")
    else:
        result.append(source)
        result.reverse()
        f.write("Y\n")
        f.write(" ".join(str(i) for i in result))
        f.write(f"\n{final_cost}")
        a = 23
