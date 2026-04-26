import json
import numpy as np
import os
import interferometer as itf
import matplotlib.pyplot as plt
import FitCos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALIB_FILE = os.path.join(BASE_DIR, '12_mode_chip2_calibration4_1.75_2025_11_30_18.99_TEC.json')

def phase2power(theta, MZI):

    with open(CALIB_FILE, 'r') as file:
        data = json.load(file)

    phase_params = data['phase_calibration'][MZI]['phase_params']
    omega = phase_params['omega']
    theta0 = phase_params['phase']

    dtheta = (theta - theta0) % 2
    P = dtheta * np.pi / omega

    return P #mW

def power2phase(P, MZI):
    
    with open(CALIB_FILE, 'r') as file:
        data = json.load(file)

    phase_params = data['phase_calibration'][MZI]['phase_params']
    omega = phase_params['omega']
    theta0 = phase_params['phase']

    dtheta = P * omega / np.pi
    theta = dtheta + theta0

    return theta 

def power_transfer(P1, d):
    #arbitrary function
    P2 = P1 * np.e ** (-0.05 * d)
    return P2

def optical_power(theta):
    W0  = np.matrix([[1],
                     [0]])
    T = np.matrix([[np.sin(theta/2), np.cos(theta/2)],
                   [np.cos(theta/2), -np.sin(theta/2)]])
    W = T * W0 
    return W 

def sweep():
    mzi1 = 'K1_theta'
    mzi2 = 'H1_theta'
    D = 30
    N = 40

    theta1_lst = [1/N * n for n in range(N + 1)]
    P_lst = []
    W_lst = []

    for theta1 in theta1_lst:
        P1 = phase2power(theta1, mzi1)
        P2 = phase2power(0.5, mzi2) + power_transfer(P1, D)

        theta2 = power2phase(P2, mzi2)
        
        W = optical_power(theta2)
        P_lst.append(P1)
        W_lst.append(W[1,0]) 

    a, b, c, d = FitCos._fit_cosine_general(P_lst, W_lst)
    W_fit = [a * np.cos(b*P + c) + d for P in P_lst]
    plt.plot(P_lst, W_fit, '*')
    plt.plot(P_lst, W_lst, '-o')
    plt.show()

    P2_lst = []
    W2_lst = []

    for theta1 in theta1_lst:
        P1 = phase2power(theta1, mzi1)

        theta2 = 0.5 + b * P1

        P2 = phase2power(theta2, mzi2) + power_transfer(P1, D)

        theta2 = power2phase(P2, mzi2)

        W = optical_power(theta2)
        P2_lst.append(P1)
        W2_lst.append(W[1,0])

    plt.plot(P2_lst, W2_lst, '-o')
    plt.show()

def main():
    sweep()

if __name__ == '__main__':
    main()
