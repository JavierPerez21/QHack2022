#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """

    # QHACK #
    
    dev = qml.device("default.qubit", wires=6, shots=1)

    @qml.qnode(dev)
    def circuit():

      # Apply Oracle
      for k in range(4):
        # Set up Deutsch-Josza
        qml.Hadamard(wires = 0)
        qml.Hadamard(wires = 1)
        qml.PauliX(wires = 2)
        qml.Hadamard(wires = 2)

        # Apply Oracle
        fs[k]([0, 1, 2])

        # Wrap-up Deutsch-Josza
        qml.Hadamard(wires = 0)
        qml.Hadamard(wires = 1)

        # Take conclusion -> 1 is
        qml.Toffoli(wires = [0, 1, 3])
        qml.PauliX(wires = 3)

        # Sum
        qml.Toffoli(wires = [3, 4, 5])
        qml.CNOT(wires = [3, 4])

        # Undo conclusion
        qml.PauliX(wires = 3)
        qml.Toffoli(wires = [0, 1, 3])

        # Undo work
        qml.Hadamard(wires = 1)
        qml.Hadamard(wires = 0)
        fs[k]([0, 1, 2])
        qml.Hadamard(wires = 2)
        qml.PauliX(wires = 2)
        qml.Hadamard(wires = 1)
        qml.Hadamard(wires = 0)


      return qml.sample(wires=[4, 5])

    # QHACK #
    sample = circuit()
    
    if np.sum(sample) == 0:
      return "4 same"
    else:
      return "2 and 2"


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")
