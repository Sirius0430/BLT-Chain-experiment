import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei']

if __name__ == '__main__':
    basedir = "tracking/Res/density-"
    means = {"3":[], "4":[], "5":[], "6":[], "7":[]}
    medians = {"3":[], "4":[], "5":[], "6":[], "7":[]}
    var = {"3":[], "4":[], "5":[], "6":[], "7":[]}
    allPoints = {"3":[],"4":[],"5":[],"6":[],"7":[]}
    for wn in [3,4,5,6,7]:
        res10000 = np.load(basedir+str(wn)+"/res10000.npy")
        res25000 = np.load(basedir+str(wn)+"/res25000.npy")
        res50000 = np.load(basedir+str(wn)+"/res50000.npy")
        res75000 = np.load(basedir+str(wn)+"/res75000.npy")
        res100000 = np.load(basedir+str(wn)+"/res100000.npy")
        res200000 = np.load(basedir+str(wn)+"/res200000.npy")
        means[str(wn)] = [np.round(np.mean(i), 3) for i in [res10000, res25000, res50000, res75000, res100000, res200000]]
        medians[str(wn)] = [np.round(np.median(i), 3) for i in [res10000, res25000, res50000, res75000, res100000, res200000]]
        var[str(wn)] = [np.round(np.var(i), 3) for i in [res10000, res25000, res50000, res75000, res100000, res200000]]
        allPoints[str(wn)] = [np.round(i,3) for i in [res10000, res25000, res50000, res75000, res100000, res200000]]
    x = [100,250,500,750,1000,2000]
    # x = range(1,7)
    plt.figure(dpi=300)
    ax = plt.subplot(111)
    # ax1 = plt.subplot(221)
    # ax2 = plt.subplot(222)
    # ax3 = plt.subplot(223)
    # ax4 = plt.subplot(224)
    # ax5 = plt.subplot(155)

    for k,v in means.items():
        ax.plot(x,v,label="Witness Number = "+k,linewidth=2)
    ax.set_xlabel("人口密度（人/平方千米）")
    ax.set_ylabel("可信度")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticklabels([0,100,250,500,750,1000,2000])
    ax.legend(loc="lower right",prop={"size":13})
    plt.show()

    # for index,ax in enumerate([ax1,ax2,ax3,ax4,ax5]):
    #     ax.boxplot(allPoints[str(index+3)],labels=x,showmeans=True,meanline=True)
    #     ax.plot(range(1,7), means[str(index+3)],label="Mean")
    #     ax.plot(range(1,7), medians[str(index+3)],label="Median")
    #     ax.set_xlabel("人口密度（人/平方千米）")
    #     ax.set_ylabel("可信度")
    #     # ax.set_xticklabels([0,100,250,500,750,1000,2000])
    #     ax.legend(loc="lower right")
    #箱线图
    # WN = "7"
    # ax.boxplot(allPoints[WN], labels=x, showmeans=True, meanline=True)
    # ax.plot(range(1, 7), means[WN], label="Mean")
    # ax.plot(range(1, 7), medians[WN], label="Median")
    # ax.set_xlabel("人口密度（人/平方千米）")
    # ax.set_ylabel("可信度")
    # # ax.set_xticklabels([0,100,250,500,750,1000,2000])
    # ax.legend(loc="lower right")
    # plt.show()