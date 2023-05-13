import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

def acc(tt, ff, sum):
    return np.round(((tt + ff) / sum),3)


def errdet(ff, tf):
    return np.round(ff / (ff + tf),3)


def erravo(ff, tf):
    return np.round(tf / (ff + tf),3)


def misjug(ft, tt):
    return np.round(ft / (ft + tt),3)


if __name__ == '__main__':
    # i[0]:predicted i[1]:true result
    data = {}
    for th in [0.2, 0.4, 0.6, 0.8]:
        basedir = "tracking/Credit/threshold-" + str(th) + "/"
        t095 = np.load(basedir + "credit0.95-0.05.npy")
        t090 = np.load(basedir + "credit0.9-0.1.npy")
        t080 = np.load(basedir + "credit0.8-0.2.npy")
        t075 = np.load(basedir + "credit0.75-0.25.npy")
        t050 = np.load(basedir + "credit0.5-0.5.npy")
        res = {"t095": 0, "t090": 0, "t080": 0, "t075": 0, "t050": 0}

        for index, t in enumerate([t095, t090, t080, t075, t050]):
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
        data["th" + str(th)] = res

    for title, d in data.items():
        accList = []
        errdetList = []
        erravoList = []
        misjugList = []
        x = []
        for k, v in d.items():
            tt = v["TT"]
            tf = v["TF"]
            ft = v["FT"]
            ff = v["FF"]
            Acc = acc(tt, ff, tt + tf + ft + ff)
            Errdet = errdet(ff, tf)
            Erravo = erravo(ff, tf)
            Misjug = misjug(ft, tt)
            accList.append(Acc)
            errdetList.append(Errdet)
            erravoList.append(Erravo)
            misjugList.append(Misjug)
            x.append(1-int(k[1:])/100)

        # "g" 表示红色
        plt.xscale("log")
        plt.plot(x, accList, "red", label="Acc")
        plt.plot(x, errdetList, "green", label="Errdet")
        plt.plot(x, erravoList, "blue", label="Erravo")
        plt.plot(x, misjugList, "black", label="Misjug")
        # 绘制坐标轴标签
        plt.xlabel("Percentage of conspirators")
        plt.ylabel("Percentage")
        plt.title(title)
        # 显示图例
        plt.legend(loc="lower right")
        plt.show()

        print()

