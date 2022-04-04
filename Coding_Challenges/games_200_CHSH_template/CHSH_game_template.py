#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """

    # QHACK #
    # Normalize alpha and beta such that |alpha|^2 + |beta|^2 = 1
    alpha_normalized = alpha / np.sqrt(alpha ** 2 + beta ** 2)
    beta_normalized = beta / np.sqrt(alpha ** 2 + beta ** 2)
    # Create a state psi = alpha |00> + beta |11>
    qml.QubitStateVector(np.array([alpha_normalized, 0, 0, beta_normalized]), wires=[0, 1])
    # QHACK #

@qml.qnode(dev)
def chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, x, y, alpha, beta):
    """Construct a circuit that implements Alice's and Bob's measurements in the rotated bases

    Args:
        - theta_A0 (float): angle that Alice chooses when she receives x=0
        - theta_A1 (float): angle that Alice chooses when she receives x=1
        - theta_B0 (float): angle that Bob chooses when he receives x=0
        - theta_B1 (float): angle that Bob chooses when he receives x=1
        - x (int): bit received by Alice
        - y (int): bit received by Bob
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (np.tensor): Probabilities of each basis state
    """
    prepare_entangled(alpha, beta)
    # QHACK #
    # We need to transform |0> and |1> into the basis states |v0> and |v1>
    # Where |v0> =  cos(theta) |0> + sin(theta) |1>
    #       |v1> = -sin(theta) |0> + cos(theta) |1>
    # This can be done by a rotation around the y-axis by theta
    # Alice chooses theta_A0 when x = 0 and theta_A1 when x = 1
    # Bob chooses theta_B0 when y = 0 and theta_B1 when y = 1
    qml.RY(theta_A0*(1-x) + theta_A1*x, wires=0)
    qml.RY(theta_B0*(1-y) + theta_B1*y, wires=1)
    # QHACK #
    return qml.probs(wires=[0, 1])
    

def winning_prob(params, alpha, beta):
    """Define a function that returns the probability of Alice and Bob winning the game.

    Args:
        - params (list(float)): List containing [theta_A0,theta_A1,theta_B0,theta_B1]
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning the game
    """

    # QHACK #

    # Sometimes pennylane passed params as a AutoGrad object and other times as a numpy array. Weird.
    probability_of_win = 0
    """
    #    theta_A0,theta_A1,theta_B0,theta_B1 = params[0], params[1], params[2], params[3]
    # There are four scenarios, (x,y) = (0,0), (0,1), (1,0), (1,1) each with a 1/4 probability
    prob00 = chsh_circuit(params[0], params[1], params[2], params[3], 0, 0, alpha, beta)
    prob01 = chsh_circuit(params[0], params[1], params[2], params[3], 0, 1, alpha, beta)
    prob10 = chsh_circuit(params[0], params[1], params[2], params[3], 1, 0, alpha, beta)
    prob11 = chsh_circuit(params[0], params[1], params[2], params[3], 1, 1, alpha, beta)
    _probability_given_xy = np.zeros(4, dtype=float)
    # x*y = 0 when (x,y) = (0,0), (0,1), (1,0)
    # If x*y = 0, the probability of winning is the probability of a = 0 and b = 0 or a = 1 and b = 1
    # This is the probability of measuring |00> + probability of measuring |11>
    _probability_given_xy[0] = prob00[0] + prob00[3]
    _probability_given_xy[1] = prob01[0] + prob01[3]
    _probability_given_xy[2] = prob10[0] + prob10[3]
    # x*y = 1 when (x,y) = (1,1)
    # If x*y = 1, the probability of winning is the probability of a = 0 and b = 1 or a = 1 and b = 0
    # This is the probability of measuring |01> + probability of measuring |10>
    _probability_given_xy[3] = prob11[1] + prob11[2]
    # The total probability of winning is the sum of the probabilities of each scenario * 1/4
    _probability_of_win = 0.25*np.sum(_probability_given_xy)
    #probability_of_win = 0.25*np.sum([prob00, prob01, prob10, prob11])
    """
    for x in [0, 1]:
      for y in [0, 1]:
        win_prob = chsh_circuit(params[0], params[1], params[2], params[3], x, y, alpha, beta)
        probability_of_win += 0.25 * (x*y*(win_prob[1] + win_prob[2]) + (1- x*y)*(win_prob[0]+win_prob[3]) )
    return probability_of_win


def optimize(alpha, beta):
    """Define a function that optimizes theta_A0, theta_A1, theta_B0, theta_B1 to maximize the probability of winning the game

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning
    """

    def cost(params):
        """Define a cost function that only depends on params, given alpha and beta fixed"""
        return -winning_prob(params, alpha, beta)

    # QHACK #

    # Initialize parameters, choose an optimization method and number of steps
    init_params = np.random.uniform(low=0, high=2 * np.pi, size=(4))
    opt = qml.optimize.AdamOptimizer(stepsize=0.1)
    steps = 200

    # QHACK #

    # set the initial parameter values
    params = init_params

    win_prob = 0
    params_hist = []
    prob_hist = []
    for i in range(steps):
        # QHACK #
        params, prob = opt.step_and_cost(cost, params)
        params_hist.append(params)
        prob_hist.append(-prob)
        #if i % 10 == 0:
        #    print(f"Epoch {i} with prob: {prob_hist[-1]}")
        if i > 10 and abs(prob_hist[-1] - prob_hist[-10]) < 1e-6:
            break
        # QHACK #

    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")