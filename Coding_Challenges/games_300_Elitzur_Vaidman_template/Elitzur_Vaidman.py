#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=1, shots=1)


@qml.qnode(dev)
def is_bomb(angle):
    """Construct a circuit at implements a one shot measurement at the bomb.

    Args:
        - angle (float): transmissivity of the Beam splitter, corresponding
        to a rotation around the Y axis.

    Returns:
        - (np.ndarray): a length-1 array representing result of the one-shot measurement
    """

    # QHACK #
    qml.RY(2 * angle, wires=0)
    # QHACK #

    return qml.sample(qml.PauliZ(0))


@qml.qnode(dev)
def bomb_tester(angle):
    """Construct a circuit that implements a final one-shot measurement, given that the bomb does not explode

    Args:
        - angle (float): transmissivity of the Beam splitter right before the final detectors

    Returns:
        - (np.ndarray): a length-1 array representing result of the one-shot measurement
    """

    # QHACK #
    qml.RY(2 * angle, wires=0)
    # QHACK #

    return qml.sample(qml.PauliZ(0))


def simulate(angle, n):
    """Concatenate n bomb circuits and a final measurement, and return the results of 10000 one-shot measurements

    Args:
        - angle (float): transmissivity of all the beam splitters, taken to be identical.
        - n (int): number of bomb circuits concatenated

    Returns:
        - (float): number of bombs successfully tested / number of bombs that didn't explode.
    """

    # QHACK #
    results = {'C': 0, 'D': 0, 'explosion': 0}
    for k in range(0, 10000):
        bomb_exploded = False
        for i in range(n):
            sample = is_bomb(angle)
            if sample == 1:
                bomb_exploded = True
            if bomb_exploded:
                results['explosion'] += 1
                break
        if bomb_exploded:
            continue
        if not bomb_exploded:
            out = bomb_tester(angle)
            if out == 1:
                results['C'] += 1
            else:
                results['D'] += 1

    return results['D'] / (10000 - results['explosion'])
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    output = simulate(float(inputs[0]), int(inputs[1]))
    print(f"{output}")

    with open(answerpath, 'r') as f:
        answer = f.read()
    print(answer)

