import json
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALIB_FILE = os.path.join(BASE_DIR, '12_mode_chip2_calibration4_1.75_2025_11_30_18.99_TEC.json')


def phase2power(phases, MZI1name):

    with open(CALIB_FILE, 'r') as file:
        data = json.load(file)

    phase_para = data['phase_calibration'][str(MZI1name)]['phase_params']

    A = phase_para['amplitude']
    b = phase_para['omega']
    c = phase_para['phase']
    d = phase_para['offset']
    
    power1 = list()
    for phase in phases:

        delta_phase = (phase - c) % 2
        P_mW = delta_phase * np.pi / b

        power1.append(P_mW)

    #print('Power for '+MZI1name +' is ' +str(P_mW))

    return power1

def power2phase(powers,MZI2name):
    
    with open(CALIB_FILE, 'r') as file:
        data = json.load(file)

    #print(data['phase_calibration']['K6_theta']['phase_params'])

    phase_para = data['phase_calibration'][str(MZI2name)]['phase_params']


    A = phase_para['amplitude']
    b = phase_para['omega']
    c = phase_para['phase']
    d = phase_para['offset']

    power2 = list()
    for power in powers:

        delta_phase = power * b / np.pi
        phase_out = delta_phase + c
        power2.append(power)
    
    #delta_phase = (theta - c) % 2
    #P_mW = delta_phase * np.pi / b

    #print('CT addon term for '+MZI2name +' is ' +str(phase_out) + ' rad.')

    return power2

def temp2power(dT):
    V = .001 #Chip volume m^3
    c = 730 # J / (kg*K)
    m = 2300 * V

    temp2 = list()
    for temp in dT:
        temp2.append(c*m*temp)

    return temp2

def power2temp(Q): #Returns delta_T
    V = .001 #Chip volume m^3
    c = 730 # J / (kg*K)
    m = 2300 * V

    temp1 = list()

    for power in Q:
        temp1.append(power/(c*m))

    return temp1

def transferHeat(temp1):

    temp2 = list()
    for temp in temp1:
        temp2.append(temp*0.001)

    return temp2

def CTterm(MZI1name,MZI2name,phaseIn):
    heating_powers = phase2power(phaseIn,MZI1name)

    MZI1_temps = power2temp(heating_powers)

    MZI2_temps = transferHeat(MZI1_temps) #Change this later to some kind of exponetial

    MZI2_powers = temp2power(MZI2_temps)

    CTaddon = power2phase(MZI2_powers,MZI2name)

    return CTaddon

if __name__ == '__main__':
    sweepSteps = 10
    sweepPhase = np.linspace(0, np.pi, sweepSteps)

    l = CTterm('K1_theta','H1_theta',sweepPhase)