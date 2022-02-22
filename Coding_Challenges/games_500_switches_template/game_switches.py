#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def switch(oracle):
    """Function that, given an oracle, returns a list of switches that work by executing a
    single circuit with a single shot. The code you write for this challenge should be completely
    contained within this function between the # QHACK # comment markers.

    Args:
        - oracle (function): oracle that simulates the behavior of the lights.

    Returns:
        - (list(int)): List with the switches that work. Example: [0,2].
    """

    dev = qml.device("default.qubit", wires=[0, 1, 2, "light"], shots=1)

    @qml.qnode(dev)
    def circuit():

        # QHACK #

        for i in range(3):
            qml.Hadamard(wires=i)
        qml.PauliX(wires="light")
        qml.Hadamard(wires="light")

        oracle()

        for i in range(3):
            qml.Hadamard(wires=i)

        # QHACK #

        return qml.sample(wires=range(3))

    sample = circuit()

    # QHACK #
    print(sample)

    sample = [i for i in range(0, len(sample)) if sample[i] > 0.5]

    # QHACK #
    return sample


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    numbers = [int(i) for i in inputs]

    def oracle():
        for i in numbers:
            qml.CNOT(wires=[i, "light"])

    output = switch(oracle)
    print(*output, sep=",")

    with open(answerpath, 'r') as f:
        answer = f.read()
    print(answer)