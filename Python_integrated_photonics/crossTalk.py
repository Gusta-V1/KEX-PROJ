import json
import numpy as np

def phase2power(phase, MZI_name):

    theta = phase
    filePath = '12_mode_chip2_calibration4_1.75_2025_11_30_18.99_TEC.json'

    with open(filePath, 'r') as file:
        data = json.load(file)

    phase_para = data['phase_calibration'][str(MZI_name)]['phase_params']

    A = phase_para['amplitude']
    b = phase_para['omega']
    c = phase_para['phase']
    d = phase_para['offset']
    
    delta_phase = (theta - c) % 2
    P_mW = delta_phase * np.pi / b

    print(f'Power: {P_mW}')

    return P_mW

def power2temp(Q): #Returns delta_T
    c = 620                                                     # J / (kg * K) 
    rho = 5430                                                  # kg / m ** 3
    V = (1.8 * 10 ** -6) * (120 * 10 ** -9) * (150 * 10 ** -6)  # m ** 3
    m = rho * V                                                 # kg

    T = Q/(c*m) 

    print(f'Temperature: {T}')

    return T

def main():
    P_mw = phase2power(1,'K1_theta')
    T = power2temp(P_mw * 10 ** -3)

if __name__ == '__main__':
    main()