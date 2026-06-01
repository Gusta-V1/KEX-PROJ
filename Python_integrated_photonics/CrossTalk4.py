import interferometer as itf
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import FitCos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALIB_FILE = os.path.join(BASE_DIR, '8-mode-autocal-20260209.json')

with open(CALIB_FILE, 'r') as file:
    CALIB_DATA = json.load(file)

def phase2power(theta, mzi):
    phase_params = CALIB_DATA['phase_calibration'][mzi]['phase_params']
    omega = phase_params['omega']
    theta0 = phase_params['phase']
    dtheta = (theta - theta0)
    P = dtheta / omega
    return P

def power2phase(P, mzi):
    phase_params = CALIB_DATA['phase_calibration'][mzi]['phase_params']
    omega = phase_params['omega']
    theta0 = phase_params['phase']
    dtheta = P * omega
    theta = dtheta + theta0
    return theta 

def power_transfer(P1):
    TRANS_COEFF_2 = 0.05
    P2 = P1 * TRANS_COEFF_2
    return P2

def optical_power(theta):
    W0  = np.array([[1],
                     [0]])
    T = np.array([[np.sin(theta/2), np.cos(theta/2)],
                   [np.cos(theta/2), -np.sin(theta/2)]])
    W = T @ W0
    powers = np.abs(W[:, 0]) ** 2 
    total_power = float(np.sum(powers))

    if total_power <= 0:
        return np.zeros(2, dtype=float)
    
    return powers / total_power

def sweep():
    mzi1 = 'G3_theta'
    mzi2 = 'G4_theta'
    N = 240
    theta20 = 0.5 * np.pi

    theta1_lst = [(1/N) * np.pi * n for n in range(N * 2 + 1) ]
    P1_lst = []
    W2_lst = []

    for theta1 in theta1_lst:
        P1 = phase2power(theta1, mzi1)
        if P1 >= 0:
            P2 = phase2power(theta20, mzi2) + power_transfer(P1)
            theta2 = power2phase(P2, mzi2)
            W2 = optical_power(theta2)
            P1_lst.append(P1)
            W2_lst.append(W2[1]) 

    a, b, c, d = FitCos._fit_cosine_general(P1_lst, W2_lst)
    print('a', a, 'b', b, 'c', c, 'd', d)

    W2_fit = [a * np.cos(b*P + c) + d for P in P1_lst]
    plt.plot(P1_lst, W2_lst, '-o', label = 'Simulated data')
    plt.plot(P1_lst, W2_fit, '--', label = 'Fitted curve')
    plt.xlabel('Heating power (mW)')
    plt.ylabel('Optical power (normalized)')
    plt.grid()
    plt.tight_layout()
    plt.legend()
    plt.show()

    W2_target = a * np.cos(c) + d

    W2_corrected_lst = []
    for theta1 in theta1_lst:
        P1 = phase2power(theta1, mzi1)
        if P1 >= 0:
            theta2_correction = theta20 - b * P1
            P2_correction = phase2power(theta2_correction, mzi2)

            P2 = P2_correction + power_transfer(P1)
            theta2 = power2phase(P2, mzi2)
            W2 = optical_power(theta2)
            W2_corrected_lst.append(W2[1])

    plt.plot(P1_lst, W2_lst, '-o', label='uncompensated')
    plt.plot(P1_lst, W2_corrected_lst, '-o', label='compensated')
    plt.axhline(W2_target, color='r', linestyle='--', label='target')
    plt.xlabel('Heating power (mW)')
    plt.ylabel('Optical power (normalized)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':

    theta = 0.5
    ct_theta = theta + 0.0176774193548

    print(optical_power(ct_theta * np.pi)[0]/optical_power(theta * np.pi)[0] - 1)