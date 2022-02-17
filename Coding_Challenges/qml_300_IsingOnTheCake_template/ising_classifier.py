#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np
import pennylane.optimize as optimize

DATA_SIZE = 250


def square_loss(labels, predictions):
    """Computes the standard square loss between model predictions and true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - loss (float): the square loss
    """

    loss = 0
    for l, p in zip(labels, predictions):
        loss = loss + (l - p) ** 2
    loss = loss / len(labels)
    return loss


def accuracy(labels, predictions):
    """Computes the accuracy of the model's predictions against the true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - acc (float): The accuracy.
    """

    acc = 0
    for l, p in zip(labels, predictions):
        if abs(l - p) < 1e-5:
            acc = acc + 1
    acc = acc / len(labels)

    return acc


def classify_ising_data(ising_configs, labels):
    """Learn the phases of the classical Ising model.

    Args:
        - ising_configs (np.ndarray): 250 rows of binary (0 and 1) Ising model configurations
        - labels (np.ndarray): 250 rows of labels (1 or -1)

    Returns:
        - predictions (list(int)): Your final model predictions

    Feel free to add any other functions than `cost` and `circuit` within the "# QHACK #" markers
    that you might need.
    """

    # QHACK #

    num_wires = ising_configs.shape[1]
    device_type = "default.qubit"  # swap to "default.qubit"
    dev = qml.device(device_type, wires=num_wires)
    # print(f"num_wires {num_wires}, example = {ising_configs[0,:]}")

    # Define a variational circuit below with your needed arguments and return something meaningful
    @qml.qnode(dev)
    def circuit(weights, x):  # delete this comment and put arguments here):
        qml.BasisState(x, wires=range(num_wires))
        qml.templates.StronglyEntanglingLayers(weights, wires=range(num_wires))
        return qml.expval(qml.PauliZ(0))

    def variational_circuit(weights, bias, x):
        return circuit(weights, x) + bias

    # Define a cost function below with your needed arguments
    def cost(weights, bias, X, Y):  # delete this comment and put arguments here):
        # QHACK #

        # Insert an expression for your model predictions here
        predictions = [variational_circuit(weights, bias, x) for x in X]

        # QHACK #

        return square_loss(Y, predictions)  # DO NOT MODIFY this line

    # optimize your circuit here
    X = np.array(ising_configs, requires_grad=False)
    Y = np.array(labels, requires_grad=False)
    # Y = Y * 2 - np.ones(len(Y))  # shift label from {0, 1} to {-1, 1}

    # for i in range(5):
    #  print("X = {}, Y = {: d}".format(X[i], int(Y[i])))

    np.random.seed(0)
    num_layers = 3
    learning_rate = 0.1
    weights_init = np.random.uniform(
        low=0, high=2 * np.pi, size=(num_layers, num_wires, 3)
    )
    bias_init = np.array(0.0, requires_grad=True)
    opt = qml.AdamOptimizer(learning_rate)
    batch_size = 10
    weights = weights_init
    bias = bias_init

    for it in range(50):

        # Update the weights by one optimizer step
        batch_index = np.random.randint(0, len(X), (batch_size,))
        X_batch = X[batch_index]
        Y_batch = Y[batch_index]
        weights, bias, _, _ = opt.step(cost, weights, bias, X_batch, Y_batch)

        # Compute accuracy
        predictions = [int(np.sign(variational_circuit(weights, bias, x))) for x in X]
        acc = accuracy(Y, predictions)

        if acc > 0.9:
            break
        # print(
        #    "Iter: {:5d} | Cost: {:0.7f} | Accuracy: {:0.7f} ".format(
        #        it + 1, cost(weights, bias, X, Y), acc
        #    )
        # )
    # QHACK #

    return predictions


if __name__ == "__main__":
    inputs = np.array(
        sys.stdin.read().split(","), dtype=int, requires_grad=False
    ).reshape(DATA_SIZE, -1)
    ising_configs = inputs[:, :-1]
    labels = inputs[:, -1]
    predictions = classify_ising_data(ising_configs, labels)
    print(*predictions, sep=",")
