import json
import numpy as np

filePath = 'Python_integrated_photonics/12_mode_chip2_calibration4_1.75_2025_11_30_18.99_TEC.json'

with open(filePath, 'r') as file:
    data = json.load(file)

#print(data['phase_calibration']['K6_theta']['phase_params'])

phase_para = data['phase_calibration']['K6_theta']['phase_params']

def phase_to_power(theta):
    A = phase_para['amplitude']
    b = phase_para['omega']
    c = phase_para['phase']
    d = phase_para['offset']
    
    delta_phase = (theta - c) % 2
    P_mW = delta_phase * np.pi / b
    return P_mW

print(phase_to_power(.5))