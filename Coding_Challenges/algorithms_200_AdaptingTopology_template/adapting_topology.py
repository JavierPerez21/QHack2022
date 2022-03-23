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
    edges = graph.copy()
    control = wires[0]
    target = wires[1]
    # We need to create 2 lists to keep track of visited nodes as we move through the graph and the distances to these nodes from the control qubit
    visited = [0] * len(edges)
    distance = [0] * len(edges)
    Q = [control] # Queue of nodes we can visit from current node
    visited[control] = True
    while len(Q) > 0:
        x = Q.pop(0)
        # Get first element of queue (node x)
        for i in range(len(edges[x])):
          # Iterate through nodes available from node x
            if visited[int(edges[x][i])]:
              # If we have already visited this node, we skip it, since that emans we already have a shorter connection to it
                continue
            # Otherwise the distance to this node i is equal to the current distance to node x, plus 1
            distance[int(edges[x][i])] = distance[x] + 1
            Q.append(int(edges[x][i])) # Add node i to the queue of available nodes
            visited[int(edges[x][i])] = True  # Label node i as visited
    # distance[target] will have the minimum number of edges between the control and target qubits.
    # To get the number of SWAPS we simply do 2*(edges-1)
    return (distance[target]-1)*2
    # QHACK


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath = sys.argv[1]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    output = n_swaps(qml.CNOT(wires=[int(i) for i in inputs]))
    print(f"{output}")
