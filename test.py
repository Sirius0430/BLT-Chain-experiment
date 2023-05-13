import numpy as np

if __name__ == '__main__':
    t095 = np.load("tracking/Credit/credit0.95-0.05.npy")
    t090 = np.load("tracking/Credit/credit0.9-0.1.npy")
    res = {"t095": 0, "t090": 0, "t080": 0, "t075": 0, "t050": 0}

    for index, t in enumerate([t095, t090]):
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
        res[list(res.keys())[index]] = classification
    print(res)