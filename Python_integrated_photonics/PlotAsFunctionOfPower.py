import matplotlib.pyplot as plt
import numpy as np
import json
import csv
import os

import FitCos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALIB_FILE = os.path.join(BASE_DIR, '8-mode-autocal-20260209.json')
CT_FILE = os.path.join(BASE_DIR, 'source-g3theta_target-g4theta.csv')

with open(CALIB_FILE, 'r') as file:
    CALIB_DATA = json.load(file)

with open(CT_FILE, 'r', encoding='utf-8') as file:
    CT_DATA = list(csv.reader(file))

def power(phase_value, mzi):
    phase_params = CALIB_DATA['phase_calibration'][mzi]['phase_params']
    b = phase_params['omega']
    c = phase_params['phase']
    delta_phase = (phase_value - c) % 2
    P_mW = delta_phase * np.pi / b  # Power in mW
    return P_mW

def plot():
    mzi1 = 'G3_theta'
    mzi2 = 'G4_theta'

    legend1 = CT_DATA[0][2]
    legend2 = CT_DATA[0][4]

    W1 = []
    W2 = []
    P = []
    for row in CT_DATA[1:]:
        P.append(power(float(row[0]), mzi1))
        W1.append(float(row[2]))
        W2.append(float(row[4]))

    #plt.plot(P, W1,'o',label = legend1, color = 'tab:blue')
    plt.plot(P, W2,'o',label = legend2, color = 'tab:orange')
    plt.legend()
    plt.xlabel('Heating power (mW)')
    plt.ylabel('Optical power (normalized)')
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_compensated():
    mzi1 = 'G3_theta'

    W1 = []
    P = []
    for row in CT_DATA[1:]:
        P.append(power(float(row[0]), mzi1))
        W1.append(float(row[2]))

    a, b, c, d = FitCos._fit_cosine_general(P, W1)
    W1_fit = [a * np.cos(b*p + c) + d for p in P]

    print(c)
    print(np.pi/2)

    plt.plot(P, W1, 'o', label = 'Simulated data',)
    plt.plot(P, W1_fit, '*', label = 'Fitted curve')
    plt.xlabel('Heating power (mW)')
    plt.ylabel('Optical power (normalized)')
    plt.legend()
    plt.show()

plot()
