import sys
import pennylane as qml
from pennylane import numpy as np

print("Coeff and observable finder workes in other problems. Gives some error here. Everything else is donw so just re-implement that.")

def hamiltonian_coeffs_and_obs(graph):
    """Creates an ordered list of coefficients and observables used to construct
    the UDMIS Hamiltonian.

    Args:
        - graph (list((float, float))): A list of x,y coordinates. e.g. graph = [(1.0, 1.1), (4.5, 3.1)]

    Returns:
        - coeffs (list): List of coefficients for elementary parts of the UDMIS Hamiltonian
        - obs (list(qml.ops)): List of qml.ops
    """

    # QHACK #
    num_vertices = len(graph)
    E, num_edges = edges(graph)
    for node in graph:
        print(node)

    u = 1.35

    num_vertices = len(graph)
    M = np.zeros((num_vertices, num_vertices))
    for i in range(0, num_vertices):
        for j in range(0, num_vertices):
            n1 = graph[i]
            n2 = graph[j]
            M[i, j] = np.sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2)

    from functools import reduce
    from itertools import product
    from operator import matmul
    def decompose_hamiltonian(H):
        N = int(np.log2(len(H)))
        paulis = [qml.Identity, qml.PauliX, qml.PauliY, qml.PauliZ]

        obs = []
        coeffs = []

        for term in product(paulis, repeat=N):
            matrices = [i._matrix() for i in term]
            coeff = np.trace(reduce(np.kron, matrices) @ H) / (2 ** N)

            if not np.allclose(coeff, 0):
                coeffs.append(coeff)

                if not all(t is qml.Identity for t in term):
                    obs.append(reduce(matmul, [t(i) for i, t in enumerate(term) if t is not qml.Identity]))
                else:
                    obs.append(reduce(matmul, [t(i) for i, t in enumerate(term)]))

        return coeffs, obs

    M = (M < u)*1
    print(M)
    coeffs, obs = decompose_hamiltonian(M)

    # create the Hamiltonian coeffs and obs variables here

    # QHACK #

    return coeffs, obs


def edges(graph):
    """Creates a matrix of bools that are interpreted as the existence/non-existence (True/False)
    of edges between vertices (i,j).

    Args:
        - graph (list((float, float))): A list of x,y coordinates. e.g. graph = [(1.0, 1.1), (4.5, 3.1)]

    Returns:
        - num_edges (int): The total number of edges in the graph
        - E (np.ndarray): A Matrix of edges
    """

    # DO NOT MODIFY anything in this code block
    num_vertices = len(graph)
    E = np.zeros((num_vertices, num_vertices), dtype=bool)
    for vertex_i in range(num_vertices - 1):
        xi, yi = graph[vertex_i]  # coordinates

        for vertex_j in range(vertex_i + 1, num_vertices):
            xj, yj = graph[vertex_j]  # coordinates
            dij = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
            E[vertex_i, vertex_j] = 1 if dij <= 1.0 else 0

    return E, np.sum(E, axis=(0, 1))


def variational_circuit(params, num_vertices):
    """A variational circuit.

    Args:
        - params (np.ndarray): your variational parameters
        - num_vertices (int): The number of vertices in the graph. Also used for number of wires.
    """


    # QHACK #
    half = int(num_vertices / 2)
    k = 0
    for i in range(0, num_vertices):
        if i % 2 == 0:
            qml.DoubleExcitation(params[k], wires=[x for x in range(i, i +4)])
            k += 1
    for i in range(0, half):
        qml.SingleExcitation(params[k], wires=[i, half-1+i])
        k += 1
    # QHACK #


def train_circuit(num_vertices, H):
    """Trains a quantum circuit to learn the ground state of the UDMIS Hamiltonian.

    Args:
        - num_vertices (int): The number of vertices/wires in the graph
        - H (qml.Hamiltonian): The result of qml.Hamiltonian(coeffs, obs)

    Returns:
        - E / num_vertices (float): The ground state energy density.
    """

    dev = qml.device("default.qubit", wires=num_vertices)

    @qml.qnode(dev)
    def cost(params):
        """The energy expectation value of a Hamiltonian"""
        variational_circuit(params, num_vertices)
        return qml.expval(H)

    # QHACK #

    # define your trainable parameters and optimizer here
    # change the number of training iterations, `epochs`, if you want to
    # just be aware of the 80s time limit!

    epochs = 500
    params = np.random.uniform(low=-np.pi / 2, high=np.pi / 2, size=(num_vertices))
    opt = qml.optimize.AdamOptimizer(0.1)

    # QHACK #

    for i in range(epochs):
        params, E = opt.step_and_cost(cost, params)

    return E / float(num_vertices)


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read()
    inputs = np.array(inputs.split(","), dtype=float, requires_grad=False)
    num_vertices = int(len(inputs) / 2)
    x = inputs[:num_vertices]
    y = inputs[num_vertices:]
    graph = []
    for n in range(num_vertices):
        graph.append((x[n].item(), y[n].item()))
    coeffs, obs = hamiltonian_coeffs_and_obs(graph)
    H = qml.Hamiltonian(coeffs, obs)

    energy_density = train_circuit(num_vertices, H)
    print(f"{energy_density:.6f}")
    with open(answerpath, 'r') as f:
        answer = f.read()
    print(answer)
