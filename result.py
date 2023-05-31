import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os


def acc(tt, ff, sum):
    return np.round(((tt + ff) / sum), 3)


def errdet(ff, tf):
    return np.round(ff / (ff + tf), 3)


def erravo(ff, tf,sum):
    return np.round(tf / sum, 3)


def misjug(ft, tt):
    return np.round(ft / (ft + tt), 3)


if __name__ == '__main__':
    # i[0]:predicted i[1]:true result
    data = {}
    for th in [0.4, 0.6,0.8, 1.0]:
        basedir = "tracking/Credit/threshold-" + str(th) + "/"
        t0990 = np.load(basedir + "credit0.99-0.01.npy")
        t0975 = np.load(basedir + "credit0.975-0.025.npy")
        t0950 = np.load(basedir + "credit0.95-0.05.npy")
        t0900 = np.load(basedir + "credit0.9-0.1.npy")
        t0800 = np.load(basedir + "credit0.8-0.2.npy")
        t0500 = np.load(basedir + "credit0.5-0.5.npy")
        res = {"t0990": 0, "t0975": 0, "t0950": 0, "t0900": 0, "t0800": 0, "t0500": 0}

        for index, t in enumerate([t0990, t0975, t0950, t0900, t0800, t0500]):
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
            sum = tt + tf + ft + ff
            Acc = acc(tt, ff, sum)
            Errdet = errdet(ff, tf)
            Erravo = erravo(ff, tf,sum)
            Misjug = misjug(ft, tt)
            accList.append(Acc)
            errdetList.append(Errdet)
            erravoList.append(Erravo)
            misjugList.append(Misjug)
            x.append(1 - int(k[1:]) / 1000)

        x = np.array(x).round(3)

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

