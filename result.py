import numpy as np
import os

if __name__ == '__main__':
    os.chdir("tracking/Credit/threshold-0.2")
    t095 = np.load("credit0.95-0.05.npy")
    t090 = np.load("credit0.9-0.1.npy")
    t085 = np.load("credit0.8-0.2.npy")
    t075 = np.load("credit0.75-0.25.npy")
    t050 = np.load("credit0.5-0.5.npy")

