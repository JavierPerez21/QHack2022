import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane import hf

print("It runs and finds the answer for 1 but not fot 2")
print("Make sure you update the beta before using it, check what i did")
print("FInding the exited state energy takws toooooo long")





def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.

    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian

    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

    # QHACK #
    num_qubits = len(H.wires)
    qubits = H.wires
    num_param_sets = (2 ** num_qubits) - 1
    # theta = np.random.uniform(low=-np.pi / 2, high=np.pi / 2, size=(num_param_sets, 3))
    theta = np.random.uniform(low=-np.pi / 2, high=np.pi / 2, size=(3))
    dev = qml.device("default.qubit", wires=num_qubits)

    energy = 0
    hf = np.array([1, 1, 0, 0])


    theta = np.random.uniform(low=-np.pi / 2, high=np.pi / 2, size=(1))

    def circuit(theta):
        qml.DoubleExcitation(theta[0], wires=qubits)


    @qml.qnode(dev)
    def cost_fn(theta):
        qml.BasisState(hf, wires=qubits)
        circuit(theta)
        return qml.expval(H)

    @qml.qnode(dev)
    def get_ground_state(theta):
        qml.BasisState(hf, wires=qubits)
        circuit(theta)
        return qml.state()

    opt = qml.optimize.AdamOptimizer(0.1)
    energy = [cost_fn(theta)]

    # store the values of the circuit parameter
    theta_col = [theta]
    states = [get_ground_state(theta)]

    max_iterations = 200
    conv_tol = 1e-06

    for n in range(max_iterations):
        theta, prev_energy = opt.step_and_cost(cost_fn, theta)

        energy.append(cost_fn(theta))
        theta_col.append(theta)
        states.append(get_ground_state(theta))

        conv = np.abs(energy[-1] - prev_energy)

        if n % 2 == 0:
            print(f"Step = {n},  Energy = {energy[-1]:.8f} HH")

        if conv <= conv_tol:
            break
    print("\n" f"Final value of the ground-state energy = {energy[-1]:.8f} HH")
    print("\n" f"Optimal value of the circuit parameters = {theta_col[-1]}")
    print("\n" f"Ground-state state vector = {states[-1]}")
    #QHACK #

    return energy[-1], states[-1]


def create_H1(ground_state, beta, H):
    """Create the H1 matrix, then use `qml.Hermitian(matrix)` to return an observable-form of H1.

    Args:
        - ground_state (np.ndarray): from the ground state VQE calculation
        - beta (float): the prefactor for the ground state projector term
        - H (qml.Hamiltonian): the result of hf.generate_hamiltonian(mol)()

    Returns:
        - (qml.Observable): The result of qml.Hermitian(H1_matrix)
    """

    # QHACK #
    # This could be useful
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

    gs = ground_state.reshape(-1, 1)
    new_coefficients, new_observables = decompose_hamiltonian(beta * (gs @ gs.T))
    new_coefficients = np.tensor(new_coefficients)
    new_coefficients = np.concatenate((new_coefficients, H.terms[0]))
    new_observables += H.terms[1]
    H1 = qml.Hamiltonian(new_coefficients, new_observables)
    return H1
    # QHACK #


def excited_state_VQE(H1):
    """Perform VQE using the "excited state" Hamiltonian.

    Args:
        - H1 (qml.Observable): result of create_H1

    Returns:
        - (float): The excited state energy
    """

    num_qubits = len(H1.wires)
    qubits = H1.wires
    num_param_sets = (2 ** num_qubits) - 1
    dev = qml.device("default.qubit", wires=num_qubits)

    energy = 0
    hf = np.array([1, 1, 0, 0])

    theta = np.random.uniform(low=-np.pi / 2, high=np.pi / 2, size=(1))

    def circuit(theta):
        #qml.DoubleExcitation(theta[0], wires=qubits)
        qml.SingleExcitation(theta[0], wires=[1, 2])
        #qml.SingleExcitation(theta[1], wires=[1, 3])



    @qml.qnode(dev)
    def cost_fn(theta):
        qml.BasisState(hf, wires=qubits)
        circuit(theta)
        return qml.expval(H1)

    @qml.qnode(dev)
    def get_ground_state(theta):
        qml.BasisState(hf, wires=qubits)
        circuit(theta)
        return qml.state()

    opt = qml.optimize.MomentumOptimizer()

    energy = [cost_fn(theta)]

    # store the values of the circuit parameter
    theta_col = [theta]
    states = [get_ground_state(theta)]

    max_iterations = 300
    conv_tol = 1e-05

    for n in range(max_iterations):
        theta, prev_energy = opt.step_and_cost(cost_fn, theta)

        energy.append(cost_fn(theta))
        theta_col.append(theta)
        states.append(get_ground_state(theta))

        conv = np.abs(energy[-1] - prev_energy)

        if n % 2 == 0:
            print(f"Step = {n},  Energy = {energy[-1]:.8f} HH")

        if conv <= conv_tol:
            break
    print("\n" f"Final value of the ground-state energy = {energy[-1]:.8f} HH")
    # print("\n" f"Optimal value of the circuit parameters = {theta_col[-1]}")
    # print("\n" f"Ground-state state vector = {states[-1]}")
    # QHACK #
    return energy[-1]


if __name__ == "__main__":
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read()
    coord = float(inputs)
    symbols = ["H", "H"]
    geometry = np.array([[0.0, 0.0, -coord], [0.0, 0.0, coord]], requires_grad=False)
    mol = hf.Molecule(symbols, geometry)

    H = hf.generate_hamiltonian(mol)()
    E0, ground_state = ground_state_VQE(H)

    beta = 15.0 + E0
    H1 = create_H1(ground_state, beta, H)
    E1 = excited_state_VQE(H1)

    answer = [np.real(E0), E1]
    print(*answer, sep=",")
    with open(answerpath, 'r') as f:
        answer = f.read()
    print(answer)
