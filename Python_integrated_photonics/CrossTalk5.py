import interferometer as itf
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import FitCos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALIB_FILE = os.path.join(BASE_DIR, '12_mode_chip2_calibration4_1.75_2025_11_30_18.99_TEC.json')

with open(CALIB_FILE, 'r') as file:
    CALIB_DATA = json.load(file)

def phase2power(theta, MZI):
    phase_params = CALIB_DATA['phase_calibration'][MZI]['phase_params']
    omega = phase_params['omega']
    theta0 = phase_params['phase']

    dtheta = (theta - theta0) % (2 * np.pi)
    P = dtheta / omega

    return P #mW

def power2phase(P, MZI):
    phase_params = CALIB_DATA['phase_calibration'][MZI]['phase_params']
    omega = phase_params['omega']
    theta0 = phase_params['phase']

    dtheta = P * omega
    theta = dtheta + theta0

    return theta 

def power_transfer(P1, D):
    #arbitrary function
    TRANS_COEFF = 0.05
    P2 = P1 * np.e ** (-TRANS_COEFF * D)
    return P2

def optical_power(theta):
    W0  = np.array([[1],
                     [0]])
    T = np.matrix([[np.sin(theta/2), np.cos(theta/2)],
                   [np.cos(theta/2), -np.sin(theta/2)]])
    W = T @ W0
    return W 

def compensate_crosstalk(theta1_target, theta2_target, mzi1, mzi2, D):
    """
    Compute the corrected drive phase for MZI2, accounting for crosstalk from MZI1.
    
    theta1_target: intended operating phase of MZI1
    theta2_target: intended operating phase of MZI2
    """
    P1 = phase2power(theta1_target, mzi1)
    
    # How much power leaks into MZI2 due to MZI1
    P_leak = power_transfer(P1, D)
    
    # The leaked power shifts MZI2's phase — compute that shift
    # power2phase gives absolute phase, so the induced shift is the difference
    phase_params2 = CALIB_DATA['phase_calibration'][mzi2]['phase_params']
    omega2 = phase_params2['omega']
    delta_phase = P_leak * omega2   # leaked power × sensitivity = phase shift
    
    # Drive MZI2 lower by exactly this shift, so the net phase is still theta2_target
    theta2_drive = theta2_target - delta_phase
    
    return theta2_drive

def sweep():
    mzi1 = 'K1_theta'
    mzi2 = 'H1_theta'
    D = 30
    N = 40
    theta20 = 0.5 * np.pi

    theta1_lst = [1/N * np.pi * n for n in range(N + 1)]
    P1_lst = []
    W2_lst = []

    for theta1 in theta1_lst:
        P1 = phase2power(theta1, mzi1)
        P2 = phase2power(theta20, mzi2) + power_transfer(P1, D)

        theta2 = power2phase(P2, mzi2)
        
        W2 = optical_power(theta2)
        P1_lst.append(P1)
        W2_lst.append(W2[1,0]) 

    a, b, c, d = FitCos._fit_cosine_general(P1_lst, W2_lst)

    print(np.pi/4)
    print(c)

    W2_fit = [a * np.cos(b*P + c) + d for P in P1_lst]
    plt.plot(P1_lst, W2_lst, '-o')
    plt.plot(P1_lst, W2_fit, '*')
    plt.show()

    W2_comp_lst = []

    for theta1 in theta1_lst:
        theta2_drive = compensate_crosstalk(theta1, theta20, mzi1, mzi2, D)

        # Now when we add the crosstalk, the net phase lands on theta20
        P1 = phase2power(theta1, mzi1)
        P2 = phase2power(theta2_drive, mzi2) + power_transfer(P1, D)
        theta2 = power2phase(P2, mzi2)

        W2 = optical_power(theta2)
        W2_comp_lst.append(W2[1, 0])

    plt.plot(P1_lst, W2_comp_lst, '*')
    plt.show()


if __name__ == '__main__':
    sweep()