#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np
import pandas as pd


def error_wire(circuit_output):
    """Function that returns an error readout.

    Args:
        - circuit_output (?): the output of the `circuit` function.

    Returns:
        - (np.ndarray): a length-4 array that reveals the statistics of the
        error channel. It should display your algorithm's statistical prediction for
        whether an error occurred on wire `k` (k in {1,2,3}). The zeroth element represents
        the probability that a bitflip error does not occur.

        e.g., [0.28, 0.0, 0.72, 0.0] means a 28% chance no bitflip error occurs, but if one
        does occur it occurs on qubit #2 with a 72% chance.
    """

    # QHACK #

    probs = abs(np.array([circuit_output[i][i] for i in range(0, len(circuit_output))]))
    print(probs)
    p_, p0, p1, p2 = 0, 0, 0, 0
    p_ = probs[0] + probs[4]
    if probs[7] != 0:
        p0 = probs[7] + probs[3]
    if probs[5] != 0:
        p1 = probs[5] + probs[3]
    if probs[6] != 0:
        p2 = probs[6] + probs[3]

    # QHACK #
    return [p_, p0, p1, p2]


dev = qml.device("default.mixed", wires=3)


@qml.qnode(dev)
def dm_circuit(p, alpha, tampered_wire):
    """A quantum circuit that will be able to identify bitflip errors.

    DO NOT MODIFY any already-written lines in this function.

    Args:
        p (float): The bit flip probability
        alpha (float): The parameter used to calculate `density_matrix(alpha)`
        tampered_wire (int): The wire that may or may not be flipped (zero-index)

    Returns:
        Some expectation value, state, probs, ... you decide!
    """

    qml.QubitDensityMatrix(density_matrix(alpha), wires=[0, 1, 2])


    others = [i for i in [0, 1, 2] if i != tampered_wire]

    # QHACK #

    qml.CNOT(wires=[tampered_wire, others[0]])
    qml.CNOT(wires=[tampered_wire, others[1]])

    qml.BitFlip(p, wires=int(tampered_wire))

    qml.CNOT(wires=[tampered_wire, others[0]])
    qml.CNOT(wires=[tampered_wire, others[1]])
    qml.Toffoli(wires=[others[0], others[1], tampered_wire])

    return qml.state()
    # QHACK #


def density_matrix(alpha):
    """Creates a density matrix from a pure state."""
    # DO NOT MODIFY anything in this code block
    psi = alpha * np.array([1, 0], dtype=float) + np.sqrt(1 - alpha**2) * np.array(
        [0, 1], dtype=float
    )
    psi = np.kron(psi, np.array([1, 0, 0, 0], dtype=float))
    return np.outer(psi, np.conj(psi))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    inputs = np.array(inputs, dtype=float)
    p, alpha, tampered_wire = inputs[0], inputs[1], int(inputs[2])
    error_readout = np.zeros(4, dtype=float)
    dms = {}
    for tampered_wire in [0, 1, 2]:
        dm = dm_circuit(p, alpha, tampered_wire)
        dms[tampered_wire] = pd.DataFrame(dm)
    # Probs given by diagonal of density matrix
    p, alpha, tampered_wire = inputs[0], inputs[1], int(inputs[2])
    dm = dm_circuit(p, alpha, tampered_wire)
    error_readout = error_wire(dm)

    print(*error_readout, sep=",")
    with open(answerpath, 'r') as f:
        answer = f.read()
    print(answer)
