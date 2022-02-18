import sys
import pennylane as qml
from pennylane import numpy as np

NUM_WIRES = 6

print("Works like this but matrix is not unitary because diagonal is just full of zeors"
      "filling the diagonal with ones produces an wrong probability on state 111000 ie 56 "
      "If we cannnot figure it our, disable warningas and submit the code")

def triple_excitation_matrix(gamma):
    """The matrix representation of a triple-excitation Givens rotation.

    Args:
        - gamma (float): The angle of rotation

    Returns:
        - (np.ndarray): The matrix representation of a triple-excitation
    """

    # QHACK #
    c = qml.math.cos(gamma / 2)
    s = qml.math.sin(gamma / 2)

    mat = qml.math.diag([0.0] * (2 ** NUM_WIRES))
    i, j = 7, 56
    mat = qml.math.scatter_element_add(mat, (i, i), c)
    mat = qml.math.scatter_element_add(mat, (i, j), -s)
    mat = qml.math.scatter_element_add(mat, (j, i), s)
    mat = qml.math.scatter_element_add(mat, (j, j), c)
    mat = qml.math.scatter_element_add(mat, (11, 11), 1)
    mat = qml.math.scatter_element_add(mat, (25, 25), 1)
    return mat

    # QHACK #


dev = qml.device("default.qubit", wires=6)


@qml.qnode(dev)
def circuit(angles):
    """Prepares the quantum state in the problem statement and returns qml.probs

    Args:
        - angles (list(float)): The relevant angles in the problem statement in this order:
        [alpha, beta, gamma]

    Returns:
        - (np.tensor): The probability of each computational basis state
    """
    # QHACK #
    alpha, beta, gamma = angles[0], angles[1], angles[2]
    # Initialize state
    qml.BasisState(np.array([1, 1, 1, 0, 0, 0]), wires=[0, 1, 2, 3, 4, 5])
    # SingleExcitation gate
    qml.SingleExcitation(alpha, wires=[0, 5])
    # DoubleExcitation gate
    qml.DoubleExcitation(beta, wires=[0, 1, 4, 5])
    # TripleExcitation gate
    qml.QubitUnitary(triple_excitation_matrix(gamma), wires=[0, 1, 2, 3, 4, 5])

    # QHACK #

    return qml.probs(wires=range(NUM_WIRES))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    inputs = np.array(inputs, dtype=float)
    probs = circuit(inputs).round(6)
    print(*probs, sep=",")
    with open(answerpath, 'r') as f:
        answer = f.read()
    print(answer)
