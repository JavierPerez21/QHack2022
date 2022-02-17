import sys
import pennylane as qml
from pennylane import numpy as np

NUM_WIRES = 6

print("Control gates don't work, think if we just change DoubleExcitation for ControledDoubleExcitation")
print("and TripleExcitation for ControledTripleExcitation")

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

    mat = qml.math.diag([1.0] * 15 + [c] + [1.0] * 32 + [c] + [1.0] * 15)
    mat = qml.math.scatter_element_add(mat, (15, 48), -s)
    mat = qml.math.scatter_element_add(mat, (48, 15), s)
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
    # qml.ctrl(qml.SingleExcitation, control=0)(alpha, wires=[0, 2])
    # DoubleExcitation gate
    #qml.ctrl(qml.DoubleExcitation, control=0)(beta, wires=[1, 4, 5])
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
