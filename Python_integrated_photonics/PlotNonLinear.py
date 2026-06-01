import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALIB_FILE = os.path.join(BASE_DIR, '8-mode-autocal-20260209.json')

with open(CALIB_FILE, 'r') as file:
    CALIB_DATA = json.load(file)


def power(I, mzi):
    res_params = CALIB_DATA['resistance_calibration'][mzi]['resistance_params']
    a = res_params['a_res']
    c = res_params['c_res']
    d = res_params['d_res']
    return a * I ** 4 + c * I * 3 + d * I

def power_l(I, mzi):
    res_params = CALIB_DATA['resistance_calibration'][mzi]['resistance_params']
    a = res_params['a_res']
    c = res_params['c_res']
    d = res_params['d_res']
    return c * I * 3 + d * I

def phase(P, mzi):
    phase_params = CALIB_DATA['phase_calibration'][mzi]['phase_params']
    omega = phase_params['omega']
    theta0 = phase_params['phase']
    dtheta = (P * omega)
    theta = dtheta + theta0 
    return theta 

def plot(mzi):
    currents = CALIB_DATA['phase_calibration'][mzi]['measurement_data']['currents']
    currents = np.array(currents)
    powers = [power(I, mzi) for I in currents]
    phases = [phase(P, mzi) for P in powers]
    powers_l = [power_l(I, mzi) for I in currents]
    phases_l = [phase(P, mzi) for P in powers_l]

    plt.plot(currents, phases, 'bo', label='Data')
    plt.plot(currents, phases, 'r-', label='Quadratic model')
    plt.plot(currents, phases_l, 'k--', label='Linear model')
    plt.grid()
    plt.legend()
    plt.xlabel('Current [mA]')
    plt.ylabel('Phase [rad]')
    plt.show()

plot('G4_theta')