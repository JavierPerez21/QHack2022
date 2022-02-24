#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


dev = qml.device("default.qubit", wires=[0, 1, "sol"], shots=1)


def find_the_car(oracle):
    """Function which, given an oracle, returns which door that the car is behind.

    Args:
        - oracle (function): function that will act as an oracle. The first two qubits (0,1)
        will refer to the door and the third ("sol") to the answer.

    Returns:
        - (int): 0, 1, 2, or 3. The door that the car is behind.
    """
    @qml.qnode(dev)
    def circuit1():
        # QHACK #
        qml.Hadamard(wires=0)
        qml.PauliX(wires="sol")
        qml.Hadamard(wires="sol")
        oracle()
        qml.Hadamard(wires="sol")
        qml.PauliX(wires="sol")
        qml.Hadamard(wires=0)
        # QHACK #
        return qml.sample()

    @qml.qnode(dev)
    def circuit2():
        # QHACK #
        qml.Hadamard(wires=1)
        qml.PauliX(wires="sol")
        qml.Hadamard(wires="sol")
        oracle()
        qml.Hadamard(wires="sol")
        qml.PauliX(wires="sol")
        qml.Hadamard(wires=1)
        # QHACK #
        return qml.sample()

    sol1 = circuit1()
    sol2 = circuit2()

    # QHACK #

    bit1 = sol1[0]
    bit2 = sol2[1]

    # QHACK #
    if bit1 == 0 and bit2 == 0:
      return 3
    elif bit1 == 1 and bit2 == 1:
      return 0
    elif bit1 == 1 and bit2 == 0:
      return 2
    else:
      return 1


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    def oracle():
        if numbers[0] == 1:
            qml.PauliX(wires=0)
        if numbers[1] == 1:
            qml.PauliX(wires=1)
        qml.Toffoli(wires=[0, 1, "sol"])
        if numbers[0] == 1:
            qml.PauliX(wires=0)
        if numbers[1] == 1:
            qml.PauliX(wires=1)

    output = find_the_car(oracle)
    print(f"{output}")
