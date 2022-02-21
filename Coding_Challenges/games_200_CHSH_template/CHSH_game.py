#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


# Optimizer does not work
# Gets the right answer from for loop optimization

dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """
    
    # QHACK #
    #Normalize
    alpha_normalized = alpha/np.sqrt(alpha**2 + beta**2)
    beta_normalized = beta/np.sqrt(alpha**2 + beta**2)
    qml.QubitStateVector(np.array([alpha_normalized, 0, 0, beta_normalized]), wires=[0,1])
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

    # There are four scenarios, (x,y) = (0,0), (0,1), (1,0), (1,1) each with a 1/4 probability
    try:
        params = params._value
    except:
        pass

    #print("Now trying with params:", params)
    prob00 = chsh_circuit(params[0], params[1], params[2], params[3], 0, 0, alpha, beta)
    prob01 = chsh_circuit(params[0], params[1], params[2], params[3], 0, 1, alpha, beta)
    prob10 = chsh_circuit(params[0], params[1], params[2], params[3], 1, 0, alpha, beta)
    prob11 = chsh_circuit(params[0], params[1], params[2], params[3], 1, 1, alpha, beta)
    probability_given_xy = np.zeros(4, dtype=float)
    probability_given_xy[0] = prob00[0] + prob00[3]
    probability_given_xy[1] = prob01[0] + prob01[3]
    probability_given_xy[2] = prob10[0] + prob10[3]
    probability_given_xy[3] = prob11[1] + prob11[2]
    
    probability_of_win = 0.25*np.sum(probability_given_xy)

    return probability_of_win

    # QHACK #
    

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

    #Initialize parameters, choose an optimization method and number of steps
    init_params = np.array([0.5, 0.5, 0.5, 0.5], requires_grad=True)
    opt = qml.GradientDescentOptimizer(stepsize=0.1)
    steps = 20
    # QHACK #
    
    # set the initial parameter values
    params = init_params

    for i in range(steps):
        # update the circuit parameters 
        # QHACK #
        params = opt.step(cost, params)
        print("Winning Probability:", cost(params))

    #I'll just optimize it myself
    #win_prob = 0
    #best_params = np.array([0.5, 0.5, 0.5, 0.5])
    #for thetaA0 in np.linspace(0, np.pi, steps):
    #    if thetaA0 % (np.pi / 20) == 0:
    #        print("thetaA0:", thetaA0)
    #    for thetaA1 in np.linspace(0, np.pi, steps):
    #        for thetaB0 in np.linspace(0, np.pi, steps):
    #            for thetaB1 in np.linspace(0, np.pi, steps):
    #                params = np.array([thetaA0, thetaA1, thetaB0, thetaB1])
    #                if winning_prob(params, alpha, beta) > win_prob:
    #                    win_prob = winning_prob(params, alpha, beta)
    #                    best_params = params
    #                    print("Winning Probability:", win_prob)
    #                    print("Params:", params)
        # QHACK #

    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")