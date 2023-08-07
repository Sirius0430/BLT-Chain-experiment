import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['Arial']

fontTitle = {
    'family': 'Arial',
    'weight': 'normal',
    # 'style': 'italic',
    'size': 18,
}
fontLabel = {
    'family': 'Arial',
    'weight': 'bold',
    # 'style': 'italic',
    'size': 15,
}
fontTick = {
    'family': 'Arial',
    'weight': 'normal',
    'style': 'italic',
    'size': 12,
}
if __name__ == '__main__':
    basedir = "tracking/Res/density-"
    means = {"3": [], "4": [], "5": [], "6": [], "7": []}
    medians = {"3": [], "4": [], "5": [], "6": [], "7": []}
    var = {"3": [], "4": [], "5": [], "6": [], "7": []}
    allPoints = {"3": [], "4": [], "5": [], "6": [], "7": []}
    for wn in [3, 4, 5, 6, 7]:
        res10000 = np.load(basedir + str(wn) + "/res10000.npy")
        res25000 = np.load(basedir + str(wn) + "/res25000.npy")
        res50000 = np.load(basedir + str(wn) + "/res50000.npy")
        res75000 = np.load(basedir + str(wn) + "/res75000.npy")
        res100000 = np.load(basedir + str(wn) + "/res100000.npy")
        res200000 = np.load(basedir + str(wn) + "/res200000.npy")
        means[str(wn)] = [np.round(np.mean(i), 3) for i in
                          [res10000, res25000, res50000, res75000, res100000, res200000]]
        medians[str(wn)] = [np.round(np.median(i), 3) for i in
                            [res10000, res25000, res50000, res75000, res100000, res200000]]
        var[str(wn)] = [np.round(np.var(i), 3) for i in [res10000, res25000, res50000, res75000, res100000, res200000]]
        allPoints[str(wn)] = [np.round(i, 3) for i in [res10000, res25000, res50000, res75000, res100000, res200000]]
    x = np.array([100, 250, 500, 750, 1000, 2000])
    y = np.array([0.2,0.4,0.6,0.8,1.0])

    plt.figure(dpi=300)

    #WN和CR合成一个指标
    wn = np.array([3,4,5,6,7]).reshape(1,5)
    cr = np.array(list(means.values()))
    y=np.log(wn)*cr
    print(y)

    # 平均值折线图
    # ax = plt.subplot(111)
    # colors = ['#264653', '#2a9d8e', '#e9c46b','#f3a261','#e66f51']
    # for (k,v),c in zip(means.items(),colors):
    #     #拟合曲线图
    #     # f = np.polyfit(x, v, 3)
    #     # x2 = np.linspace(0, 2000, 2001, endpoint=True)
    #     # p = np.poly1d(f)
    #     # y2 = p(x2)
    #     # ax.plot(x2,y2,label="Witness = "+k,linewidth=2)
    #
    #     #折线图
    #     ax.plot(x,v,label="Witness = "+k,linewidth=2,color = c)
    # ax.set_xlabel("Population Density (persons/km2)",fontLabel)
    # ax.set_ylabel("Credibility",fontLabel)
    # ax.set_xscale("log")
    # # ax.set_yscale("log")
    # ax.set_xticks(x)
    # ax.set_xticklabels(x, fontTick)
    # ax.set_yticks(y)
    # ax.set_yticklabels(y, fontTick)
    # ax.legend(loc="lower right",prop={"size":13})
    # plt.savefig("fig/lineChart.png",dpi=300)
    # plt.show()

    # 总图
    plt.figure(figsize=(15,10))
    ax = plt.subplot(2,3,1)
    ax1 = plt.subplot(2,3,2)
    ax2 = plt.subplot(2,3,3)
    ax3 = plt.subplot(2,3,4)
    ax4 = plt.subplot(2,3,5)
    ax5 = plt.subplot(2,3,6)

    #折线图
    # colors = ['#264653', '#2a9d8e', '#e9c46b','#f3a261','#e66f51']
    # for (k,v),c in zip(means.items(),colors):
    #     #拟合曲线图
    #     # f = np.polyfit(x, v, 3)
    #     # x2 = np.linspace(0, 2000, 2001, endpoint=True)
    #     # p = np.poly1d(f)
    #     # y2 = p(x2)
    #     # ax.plot(x2,y2,label="Witness = "+k,linewidth=2)
    #
    #     #折线图
    #     ax.plot(x,v,label="Witness = "+k,linewidth=2,color = c)
    # ax.set_xlabel("Population Density (persons/km2)",fontLabel)
    # ax.set_ylabel("Credibility",fontLabel)
    # ax.set_xscale("log")
    # # ax.set_yscale("log")
    # ax.set_xticks(x)
    # ax.set_xticklabels(x, fontTick)
    # ax.set_yticks(y)
    # ax.set_yticklabels(y, fontTick)
    # ax.legend(loc="lower right", prop={"size": 13})
    # ax.set_title("")

    #箱线图
    # axes = [ax1,ax2,ax3,ax4,ax5]
    # for ax,WN in zip(axes,range(3,8)):
    #     WN = str(WN)
    #     bp = ax.boxplot(allPoints[WN],
    #                     labels=x,
    #                     vert=True,
    #                     patch_artist=True,
    #                     showmeans=True,
    #                     meanline=True,
    #                     zorder=1,
    #                     flierprops=dict(marker='o', markerfacecolor='black'),
    #                     medianprops={"linewidth":1.5},
    #                     meanprops={"linewidth":1.5,"color":"#1f77b4"})
    #     ax.plot(range(1, 7), means[WN], label="Mean", linewidth=2,zorder=2)
    #     ax.plot(range(1, 7), medians[WN], label="Median", linewidth=2,zorder=2)
    #     # 颜色填充
    #     boxcolors = ['#4eab90A0', '#8eb69cA0', '#edddc3A0', '#eebf6dA0', '#d94f33A0', '#834026A0']
    #     colors = ['#4eab90', '#8eb69c', '#edddc3', '#eebf6d', '#d94f33', '#834026']
    #     for patch, boxcolor,color in zip(bp['boxes'], boxcolors,colors):
    #         # patch.set_color(color)
    #         patch.set_facecolor(boxcolor)
    #
    #     ax.set_xlabel("Population Density (persons/km²)", fontLabel)
    #     ax.set_ylabel("Credibility", fontLabel)
    #     ax.set_xticklabels(x, fontTick)
    #     ax.set_yticks(y)
    #     ax.set_yticklabels(y,fontTick)
    #     ax.spines["top"].set_linewidth(1.5)
    #     ax.spines["bottom"].set_linewidth(1.5)
    #     ax.spines["left"].set_linewidth(1.5)
    #     ax.spines["right"].set_linewidth(1.5)
    #     ax.legend(loc="lower right", prop={"size": 13})
    #     ax.set_title("Witness = " + WN,fontdict=fontTitle)
    # plt.tight_layout()
    # plt.savefig("fig/boxChart.png",dpi=300)
    # plt.show()
