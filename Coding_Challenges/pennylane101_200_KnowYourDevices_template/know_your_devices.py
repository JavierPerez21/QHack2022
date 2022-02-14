#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def matrix_norm(mixed_state, pure_state):
    """Computes the matrix one-norm of the difference between mixed and pure states.

    Args:
        - mixed_state (np.tensor): A density matrix
        - pure_state (np.tensor): A pure state

    Returns:
        - (float): The matrix one-norm
    """

    return np.sum(np.abs(mixed_state - np.outer(pure_state, np.conj(pure_state))))


def compare_circuits(num_wires, params):
    """Function that returns the matrix norm between the mixed- and pure-state versions of the same state.

    Args:
        - num_wires (int): The number of qubits / wires
        - params (list(np.ndarray)): Two arrays with num_wires floats that correspond to angles of y-rotations
        for each wire

    Returns:
        - mat_norm (float): The matrix one-norm
    """

    # QHACK #
    # You have to
    # decorate each function correspondingly to return a pure state or a density matrix.
    # In other words, you need to determine the quantum devices that store the output
    # state as a density matrix (which is required for mixed_circuit) and as a state
    # vector (which is required for pure_circuit).
    # define devices
    #dev1 = qml.device("default.qubit", wires=num_wires)
    #dev2 = qml.device("default.qubit", wires=num_wires)
    dev1 = qml.device("default.qubit", wires=num_wires)
    dev2 = qml.device("default.qubit", wires=num_wires)

    # defin e quantum circuits
    @qml.qnode(dev1)
    def pure_circuit():
        """A circuit that contains `num_wires` y-rotation gates.
        The argument params[0] are the parameters you should use here to define the y-rotations.

        Returns:
            - (np.tensor): A state vector
        """
        for i in range(0, num_wires):
            qml.RY(params[0][i], wires=i)
        return qml.state()

    @qml.qnode(dev2, diff_method="backprop")
    def mixed_circuit():
        """A circuit that contains `num_wires` y-rotation gates.
        The argument params[1] are the parameters you should use here to define the y-rotations.

        Returns:
            - (np.tensor): A density matrix
        """
        for i in range(0, num_wires):
            qml.RY(params[1][i], wires=i)
        return qml.density_matrix([x for x in range(0, num_wires)])

    # QHACK #

    # DO NOT MODIFY any of the next lines in this scope
    mixed_state = mixed_circuit()
    pure_state = pure_circuit()
    mat_norm = matrix_norm(mixed_state, pure_state)

    return mat_norm


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath = sys.argv[1]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    num_wires = int(inputs[0])
    l = int(len(inputs[1:]) / 2)
    params = [
        np.array(inputs[1 : (l + 1)], dtype=float),  # for pure circuit
        np.array(inputs[(l + 1) :], dtype=float),  # for mixed circuit
    ]

    output = compare_circuits(num_wires, params)
    print(f"{output:.6f}")
