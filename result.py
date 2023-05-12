import numpy as np
import os

if __name__ == '__main__':
    # i[0]:predicted i[1]:true result
    for th in [0.2, 0.4, 0.6, 0.8]:
        basedir = "tracking/Credit/threshold-" + str(th)+"/"
        t095 = np.load(basedir+"credit0.95-0.05.npy")
        t090 = np.load(basedir+"credit0.9-0.1.npy")
        t080 = np.load(basedir+"credit0.8-0.2.npy")
        t075 = np.load(basedir+"credit0.75-0.25.npy")
        t050 = np.load(basedir+"credit0.5-0.5.npy")
        res = {"t095":0,"t090":0,"t080":0,"t075":0,"t050":0}

        for index,t in enumerate([t095, t090, t080, t075, t050]):
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
        print("th"+str(th))
        print(res)
