import json
import numpy as np

def phase2power(phase, MZI_name):

    theta = phase
    filePath = '12_mode_chip2_calibration4_1.75_2025_11_30_18.99_TEC.json'

    with open(filePath, 'r') as file:
        data = json.load(file)

    #print(data['phase_calibration']['K6_theta']['phase_params'])

    phase_para = data['phase_calibration'][str(MZI_name)]['phase_params']


    A = phase_para['amplitude']
    b = phase_para['omega']
    c = phase_para['phase']
    d = phase_para['offset']
    
    delta_phase = (theta - c) % 2
    P_mW = delta_phase * np.pi / b

    print('Power for '+MZI_name +' is ' +str(P_mW))


    return P_mW

phase2power(1,'K1_theta')

def power2temp(Q) #Returns delta_T
    c = 730 # J / (kg*K)
    m = 2300 * 
    return Q/(c*m)