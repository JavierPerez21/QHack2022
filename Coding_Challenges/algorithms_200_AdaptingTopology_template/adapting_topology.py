#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml

graph = {
    0: [1],
    1: [0, 2, 3, 4],
    2: [1],
    3: [1],
    4: [1, 5, 7, 8],
    5: [4, 6],
    6: [5, 7],
    7: [4, 6],
    8: [4],
}


def n_swaps(cnot):
    """Count the minimum number of swaps needed to create the equivalent CNOT.

    Args:
        - cnot (qml.Operation): A CNOT gate that needs to be implemented on the hardware
        You can find out the wires on which an operator works by asking for the 'wires' attribute: 'cnot.wires'

    Returns:
        - (int): minimum number of swaps
    """

    # QHACK #
    wires = [x for x in cnot.wires]
    def build_m(graph):
        m = np.zeros((len(graph), len(graph)), dtype=int)
        for i in range(len(graph)):
            for j in graph[i]:
                m[i, j] = 1
                m[j, i] = 1
        return m
    m = build_m(graph)
    def min_distance(edges, u, v):
        visited = [0] * len(edges)
        distance = [0] * len(edges)
        # Code without queue
        Q = [u]
        visited[u] = True
        while len(Q) > 0:

            x = Q.pop(0)
            for i in range(len(edges[x])):
                if visited[int(edges[x][i])]:
                    continue
                distance[int(edges[x][i])] = distance[x] + 1
                Q.append(int(edges[x][i]))
                visited[int(edges[x][i])] = True
        return distance[v]
    return (min_distance(graph, wires[0], wires[1]) -1)*2
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath = sys.argv[1]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    output = n_swaps(qml.CNOT(wires=[int(i) for i in inputs]))
    print(f"{output}")
