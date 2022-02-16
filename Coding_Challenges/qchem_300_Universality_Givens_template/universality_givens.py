#! /usr/bin/python3

import sys
import numpy as np


def givens_rotations(a, b, c, d):
    """Calculates the angles needed for a Givens rotation to out put the state with amplitudes a,b,c and d

    Args:
        - a,b,c,d (float): real numbers which represent the amplitude of the relevant basis states (see problem statement). Assume they are normalized.

    Returns:
        - (list(float)): a list of real numbers ranging in the intervals provided in the challenge statement, which represent the angles in the Givens rotations,
        in order, that must be applied.
    """

    # QHACK #
    #a = cos(X)cos(Z)
    #b = -sin(X)cos(Y)
    #c = sin(X)sin(Y)
    #d = -cos(X)sin(Z)
    Z = np.arctan(-d/a)

    Y = np.arctan(- c / b)

    """
    x = a / np.sin(Y)
    if abs(x) > 1:
        x = -b / np.cos(Y)
    if abs(x) > 1:
        x =  c / np.sin(Y)
    if abs(x) > 1:
        x = -d / np.cos(Y)
    X = np.arcsin(x)
    """
    X = np.arctan(-(c * np.sin(Z)) / (d * np.sin(Y)))

    return X*2, Y*2, Z*2

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    filepath, answerpath = sys.argv[1], sys.argv[2]
    with open(filepath, 'r') as f:
        inputs = f.read().split(",")
    theta_1, theta_2, theta_3 = givens_rotations(
        float(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[3])
    )
    print(*[theta_1, theta_2, theta_3], sep=",")
    with open(answerpath, 'r') as f:
        print(f.read())
