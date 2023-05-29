import numpy as np

if __name__ == '__main__':
    t0990 = np.load("tracking/Credit/threshold-0.8/credit0.99-0.01.npy")
    t0975 = np.load("tracking/Credit/threshold-0.8/credit0.975-0.025.npy")
    t0950 = np.load("tracking/Credit/threshold-0.8/credit0.95-0.05.npy")
    t0900 = np.load("tracking/Credit/threshold-0.8/credit0.9-0.1.npy")
    t0800 = np.load("tracking/Credit/threshold-0.8/credit0.8-0.2.npy")
    t0500 = np.load("tracking/Credit/threshold-0.8/credit0.5-0.5.npy")

    for t in [t0990,t0975,t0950,t0900,t0800,t0500]:
        classification = {"TT": 0, "TF": 0, "FT": 0, "FF": 0}
        for i in t:
            if i[0] == True and i[1] == True:
                classification["TT"] += 1
            if i[0] == True and i[1] == False:
                classification["TF"] += 1
            if i[0] == False and i[1] == True:
                classification["FT"] += 1
            if i[0] == False and i[1] == False:
                classification["FF"] += 1
        print(classification)