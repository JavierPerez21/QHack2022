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
        # qml.PauliX(wires=0)
        oracle()
        return qml.sample()

    @qml.qnode(dev)
    def circuit2():
        # QHACK #
        qml.PauliX(wires=1)
        oracle()
        # QHACK #
        return qml.sample()

    sol1 = circuit1()
    sol2 = circuit2()
    sol = [0, 0]
    if sol1[-1] == 1:
        sol[0] = 1
    if sol2[-1] == 1:
        sol[1] = 1

    return sol[1] * 2 + sol[0], sol1, sol2


    # QHACK #


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


    # ! /usr/bin/python3

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

        def difuser(i1, i2):
            for i in [0, 1]:
                qml.Hadamard(wires=i)
            if i1 == 1:
                qml.Z(wires=0)
            if i2 == 1:
                qml.Z(wires=1)
            qml.CZ(wires=[0, 1])
            for i in [0, 1]:
                qml.Hadamard(wires=i)

        @qml.qnode(dev)
        def circuit1():
            # QHACK #
            for i in [0, 1]:
                qml.Hadamard(wires=i)
            difuser(0, 0)
            # QHACK #
            return qml.sample()

        @qml.qnode(dev)
        def circuit2():
            # QHACK #

            # QHACK #
            return qml.sample()

        sol1 = circuit1()
        sol2 = circuit2()
        sol = [0, 0]
        if sol1[-1] == 1:
            sol[0] = 1
        if sol2[-1] == 1:
            sol[1] = 1

        return sol[1] * 2 + sol[0], sol1, sol2

    # QHACK #

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


    for numbers in [[0, 0], [1, 0], [0, 1], [1, 1]]:
        output, sol1, sol2 = find_the_car(oracle)
        print(numbers, output, sol1, sol2)

