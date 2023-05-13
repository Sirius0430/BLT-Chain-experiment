import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei']

if __name__ == '__main__':
    res10000 = np.load("tracking/Res/density-3/res10000.npy")
    res25000 = np.load("tracking/Res/density-3/res25000.npy")
    res50000 = np.load("tracking/Res/density-3/res50000.npy")
    res75000 = np.load("tracking/Res/density-3/res75000.npy")
    res100000 = np.load("tracking/Res/density-3/res100000.npy")
    res200000 = np.load("tracking/Res/density-3/res200000.npy")

    x = [100,250,500,750,1000,2000]
    res = [np.round(np.mean(i),3) for i in [res10000,res25000,res50000,res75000,res100000,res200000]]
    plt.figure(dpi=300)
    plt.plot(x,res)
    plt.xlabel("人口密度（人/平方千米）")
    plt.ylabel("可信度")
    plt.xscale("log")
    plt.show()