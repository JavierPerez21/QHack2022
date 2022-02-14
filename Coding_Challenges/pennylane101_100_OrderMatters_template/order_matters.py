#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def compare_circuits(angles):
    """Given two angles, compare two circuit outputs that have their order of operations flipped: RX then RY VERSUS RY then RX.

    Args:
        - angles (np.ndarray): Two angles

    Returns:
        - (float): | < \sigma^x >_1 - < \sigma^x >_2 |
    """

    # QHACK #
    num_wires = 1
    dev = qml.device('default.qubit', wires=num_wires)

    @qml.qnode(dev)
    def circuit1(angles):
        qml.RX(angles[0], wires=0)
        qml.RY(angles[1], wires=0)
        return qml.expval(qml.PauliX(0))

    out1 = float(circuit1(angles))

    @qml.qnode(dev)
    def circuit2(angles):
        qml.RY(angles[1], wires=0)
        qml.RX(angles[0], wires=0)
        return qml.expval(qml.PauliX(0))

    out2 = float(circuit2(angles))

    absdif = abs(out1 - out2)
    # QHACK #

    return absdif


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath = sys.argv[1]
    with open(filepath, 'r') as f:
        angles = f.read()
    angles = np.array(angles.split(","), dtype=float)
    output = compare_circuits(angles)
    print(f"{output:.6f}")
