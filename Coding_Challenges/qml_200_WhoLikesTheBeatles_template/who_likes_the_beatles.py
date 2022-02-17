#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def distance(A, B):
    """Function that returns the distance between two vectors.

    Args:
        - A (list[int]): person's information: [age, minutes spent watching TV].
        - B (list[int]): person's information: [age, minutes spent watching TV].

    Returns:
        - (float): distance between the two feature vectors.
    """

    # QHACK #

    # The Swap test is a method that allows you to calculate |<A|B>|^2 , you could use it to help you.
    # The qml.AmplitudeEmbedding operator could help you too.

    dev = qml.device("default.qubit", 3)
    @qml.qnode(dev)
    def circuit():
      #qml.AmplitudeEmbedding(features=A, wires=1, normalize=True)
      #qml.AmplitudeEmbedding(features=B, wires=2, normalize=True)
      #print(A, [A[0]/np.sqrt(A[0]**2 + A[1]**2), A[1]/np.sqrt(A[0]**2 + A[1]**2)])
      qml.templates.state_preparations.MottonenStatePreparation(
          [A[0]/np.sqrt(A[0]**2 + A[1]**2), A[1]/np.sqrt(A[0]**2 + A[1]**2)], wires = 1
      )
      qml.templates.state_preparations.MottonenStatePreparation(
          [B[0]/np.sqrt(B[0]**2 + B[1]**2), B[1]/np.sqrt(B[0]**2 + B[1]**2)], wires = 2
      )
      qml.Hadamard(wires = 0)
      qml.CSWAP(wires = [0, 1, 2])
      qml.Hadamard(wires = 0)
      return qml.probs(wires = 0)

    # QHACK #
    circ_result = circuit()[0]
    # print(f"Circ Result: {circ_result}")
    swap_test_sq = 2*circ_result - 1
    inner_product =  np.sqrt(swap_test_sq)
    answer = np.sqrt(2 * (1 - inner_product))
    return answer


def predict(dataset, new, k):
    """Function that given a dataset, determines if a new person do like Beatles or not.

    Args:
        - dataset (list): List with the age, minutes that different people watch TV, and if they like Beatles.
        - new (list(int)): Age and TV minutes of the person we want to classify.
        - k (int): number of nearby neighbors to be taken into account.

    Returns:
        - (str): "YES" if they like Beatles, "NO" otherwise.
    """

    # DO NOT MODIFY anything in this code block

    def k_nearest_classes():
        """Function that returns a list of k near neighbors."""
        distances = []
        for data in dataset:
            distances.append(distance(data[0], new))
        nearest = []
        for _ in range(k):
            indx = np.argmin(distances)
            nearest.append(indx)
            distances[indx] += 2

        return [dataset[i][1] for i in nearest]

    output = k_nearest_classes()

    return (
        "YES" if len([i for i in output if i == "YES"]) > len(output) / 2 else "NO",
        float(distance(dataset[0][0], new)),
    )


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    dataset = []
    new = [int(inputs[0]), int(inputs[1])]
    k = int(inputs[2])
    for i in range(3, len(inputs), 3):
        dataset.append([[int(inputs[i + 0]), int(inputs[i + 1])], str(inputs[i + 2])])

    output = predict(dataset, new, k)
    sol = 0 if output[0] == "YES" else 1
    print(f"{sol},{output[1]}")
