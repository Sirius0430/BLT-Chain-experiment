import gc

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os


def acc(tt, ff,tf,ft, sum):
    return np.round(((tt + ff) / sum), 3)


def errdet(tt, ff,tf,ft, sum):
    return np.round(ff / (ff+tf), 3)


def errmis(tt, ff,tf,ft, sum):
    return np.round(tf / (ff+tf), 3)


def misjug(tt, ff,tf,ft, sum):
    return np.round(ft / (ft + tt), 3)


if __name__ == '__main__':
    # i[0]:predicted i[1]:true result
    data = {}
    for th in [0.4, 0.6, 0.8, 1.0]:
        basedir = "tracking/Credit/threshold-" + str(th) + "/"
    # for th in [1.0]:
    #     basedir = "threshold-" + str(th) + "/"
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

    del t0990
    del t0975
    del t0950
    del t0900
    del t0800
    del t0500
    gc.collect()



    accListSum = []
    errdetListSum = []
    errmisListSum = []
    misjugListSum = []
    x = np.array([0.01, 0.025, 0.05, 0.1, 0.2, 0.5])
    y = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    for title, d in data.items():
        accList = []
        errdetList = []
        errmisList = []
        misjugList = []
        for k, v in d.items():
            tt = v["TT"]
            tf = v["TF"]
            ft = v["FT"]
            ff = v["FF"]
            sum = tt + tf + ft + ff
            Acc = acc(tt, ff,tf,ft, sum)
            Errdet = errdet(tt, ff,tf,ft, sum)
            Erravo = errmis(tt, ff,tf,ft, sum)
            Misjug = misjug(tt, ff,tf,ft, sum)
            accList.append(Acc)
            errdetList.append(Errdet)
            errmisList.append(Erravo)
            misjugList.append(Misjug)

        accList = np.array(accList)
        errdetList = np.array(errdetList)
        errmisList = np.array(errmisList)
        misjugList = np.array(misjugList)

        accListSum.append(accList)
        errdetListSum.append(errdetList)
        errmisListSum.append(errmisList)
        misjugListSum.append(misjugList)

    accListSum = np.array(accListSum)
    errdetListSum = np.array(errdetListSum)
    errmisListSum = np.array(errmisListSum)
    misjugListSum = np.array(misjugListSum)

    # 折线图
    # for ax, title, data in zip(axes, ["Accuracy", "Error Detection Rate", "Error Missing Rate", "Misjudgement Rate"],
    #                            [accListSum, errdetListSum, errmisListSum, misjugListSum]):
    plt.figure(figsize=(15,5))
    ax1 = plt.subplot(131)
    ax2 = plt.subplot(132)
    ax3 = plt.subplot(133)

    axes = [ax1, ax2, ax3]
    for ax, title, data in zip(axes, ["Accuracy", "Error Detection Rate", "Misjudgement Rate"],
                               [accListSum, errdetListSum, misjugListSum]):
        for line,index in zip(data,["0.4","0.6","0.8","1.0"]):
            ax.plot(x, line, linewidth=2,label="Threshold = "+index)

        fontTitle = {
            'family': 'Arial',
            'weight': 'normal',
            # 'style': 'italic',
            'size': 15,
        }
        fontLabel = {
            'family': 'Arial',
            'weight': 'bold',
            # 'style': 'italic',
            'size': 13,
        }
        fontTick = {
            'family': 'Arial',
            'weight': 'normal',
            'style': 'italic',
            'size': 11,
        }
        ax.set_xlabel("Percentage of Cheaters", fontLabel)
        ax.set_ylabel("Value", fontLabel)
        ax.set_xscale("log")
        # ax.set_ylim(0.0,1.0)
        ax.set_xticks(x)
        ax.set_xticklabels(x, fontTick)
        ax.set_yticks(y)
        ax.set_yticklabels(y, fontTick)
        # ax.yaxis.grid(True)
        ax.spines["top"].set_linewidth(1.5)
        ax.spines["bottom"].set_linewidth(1.5)
        ax.spines["left"].set_linewidth(1.5)
        ax.spines["right"].set_linewidth(1.5)
        ax.set_title(title, fontdict=fontTitle)
        ax.legend()
    plt.tight_layout()
    plt.savefig("fig/accLineChart.png",dpi=300)
    plt.show()

    # 柱状图
    # fontTitle = {
    #     'family': 'Arial',
    #     'weight': 'normal',
    #     # 'style': 'italic',
    #     'size': 15,
    # }
    # fontLabel = {
    #     'family': 'Arial',
    #     'weight': 'bold',
    #     # 'style': 'italic',
    #     'size': 13,
    # }
    # fontTick = {
    #     'family': 'Arial',
    #     'weight': 'normal',
    #     'style': 'italic',
    #     'size': 11,
    # }
    # # colors = ["#264653","#2a9d8c","#e9c46b","#e66f51"]
    # colors = ["#a40545", "#f48f44", "#fdd985", "#7fcba4"]
    #
    # ax1 = plt.subplot(221)
    # ax2 = plt.subplot(222)
    # ax3 = plt.subplot(223)
    # ax4 = plt.subplot(224)
    # axes = [ax1, ax2, ax3, ax4]
    # for ax, (th, res) in zip(axes, data.items()):
    #     ax.set_title("Threshold = " + th[2:], fontdict=fontTitle)
    #     TT = np.array([i["TT"] for i in res.values()])
    #     TF = np.array([i["TF"] for i in res.values()])
    #     FT = np.array([i["FT"] for i in res.values()])
    #     FF = np.array([i["FF"] for i in res.values()])
    #     ax.bar(range(1, len(x) + 1), FF, width=0.6, color=colors[0], label="FF")
    #     ax.bar(range(1, len(x) + 1), TF, width=0.6, color=colors[1], bottom=FF, label="TF")
    #     ax.bar(range(1, len(x) + 1), FT, width=0.6, color=colors[2], bottom=FF + TF, label="FT")
    #     ax.bar(range(1, len(x) + 1), TT, width=0.6, color=colors[3], bottom=FF + TF + FT, label="TT")
    #     # ax.bar(range(1, len(x) + 1), FF, width=0.6, color=colors[0], edgecolor="black", linewidth=0.5, label="FF")
    #     # ax.bar(range(1, len(x) + 1), TF, width=0.6, color=colors[1], edgecolor="black", linewidth=0.5, bottom=FF, label="TF")
    #     # ax.bar(range(1, len(x) + 1), FT, width=0.6, color=colors[2], edgecolor="black", linewidth=0.5, bottom=FF + TF, label="FT")
    #     # ax.bar(range(1, len(x) + 1), TT, width=0.6, color=colors[3], edgecolor="black", linewidth=0.5, bottom=FF + TF + FT, label="TT")
    #     ax.set_xticks(range(1, len(x) + 1))
    #     ax.set_xticklabels(x, fontTick)
    #     ax.set_ylim(0, 1000)
    #     ax.set_xlabel("Percentage of Cheaters", fontLabel)
    #     ax.set_ylabel("Persons", fontLabel)
    #
    # # plt.legend(ncol=4,bbox_to_anchor=(0.5, 0),prop=fontLabel)
    # plt.legend(prop=fontLabel)
    # # plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.5)
    # # plt.figure(figsize=(10,10))
    # plt.tight_layout()
    # plt.savefig("fig/distributionChart.png",dpi=300)
    # plt.show()
