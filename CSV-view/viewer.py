import csv
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'CSVdata\source-h2theta_target-h3theta_100steps.csv')

def plot_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lst = [i for i in reader]

    phase = []
    out7 = []
    out8 = []
    
    for row in lst[1:]:
        phase.append(float(row[0]))
        out7.append(float(row[2]))
        out8.append(float(row[4]))

    plt.plot(phase, out7, '-o', label = lst[0][2])
    plt.plot(phase, out8, '-o', label = lst[0][4])
    plt.legend()
    plt.grid()
    plt.savefig('source-h2theta_target-h3theta_100steps.png')
    plt.show()

if __name__ == "__main__":
    plot_csv(CSV_FILE)
