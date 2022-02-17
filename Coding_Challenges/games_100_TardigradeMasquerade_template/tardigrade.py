import sys
import pennylane as qml
from pennylane import numpy as np


def second_renyi_entropy(rho):
    """Computes the second Renyi entropy of a given density matrix."""
    # DO NOT MODIFY anything in this code block
    rho_diag_2 = np.diagonal(rho) ** 2.0
    return -np.real(np.log(np.sum(rho_diag_2)))


def compute_entanglement(theta):
    """Computes the second Renyi entropy of circuits with and without a tardigrade present.

    Args:
        - theta (float): the angle that defines the state psi_ABT

    Returns:
        - (float): The entanglement entropy of qubit B with no tardigrade
        initially present
        - (float): The entanglement entropy of qubit B where the tardigrade
        was initially present
    """

    dev = qml.device("default.qubit", wires=3)

    G = np.identity(4)
    G[1, 1] = np.cos(theta/2)
    G[1, 2] = np.sin(theta/2)
    G[2, 1] = -np.sin(theta/2)
    G[2, 2] = np.cos(theta/2)

    # QHACK #
    @qml.qnode(dev)
    def circuit_ab():
        qml.Hadamard(wires=0)
        qml.PauliX(wires=1)
        qml.CNOT(wires=[0, 1])
        #return qml.state()
        return qml.density_matrix([1])


    @qml.qnode(dev)
    def circuit_abt():
        qml.Hadamard(wires=0)
        qml.PauliX(wires=1)
        qml.CNOT(wires=[0, 1])
        qml.QubitUnitary(G, wires=[1, 2])
        return qml.density_matrix([1])

    return second_renyi_entropy(circuit_ab()), second_renyi_entropy(circuit_abt())

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read()
    theta = np.array(inputs, dtype=float)

    S2_without_tardigrade, S2_with_tardigrade = compute_entanglement(theta)
    print(*[S2_without_tardigrade, S2_with_tardigrade], sep=",")
    with open(answerpath, 'r') as f:
        answer = f.read()
    print(answer)
