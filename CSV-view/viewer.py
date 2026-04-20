import csv
import numpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'CSVdata\source-g2theta_target-g4theta.csv')

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)  # Or process the row as needed

# Example usage
if __name__ == "__main__":
    read_csv(CSV_FILE)