from collections import defaultdict
from math import ulp
from os import supports_bytes_environ
import numpy


FILE_IN = "ford_flakerson\input.txt"
FILE_OUT = "out.txt"

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

k, l, data_size, edges = read_input()

print(edges)


px = []  # массив вершин y∈R, инцидентные xi∈L в текущем паросочетании
py = []  # массив вершин x∈L, инцидентные yi∈R в текущем паросочетании
visited = []  # массив, где помечаются посещенные вершины

# Максимальное паросочетание — такие ребра (x,y), что x∈L,y∈R,px[x]=y.


# поиск в глубину
def dfs(x):
    if visited[x]:
        return False
    visited[x] = True
    for i in x: # for (x,y)∈E
        if py[y]
