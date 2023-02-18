import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei']

res10000 = np.load("tracking/Res/density-7/res10000.npy")
res25000 = np.load("tracking/Res/density-7/res25000.npy")
res50000 = np.load("tracking/Res/density-7/res50000.npy")
res75000 = np.load("tracking/Res/density-7/res75000.npy")
res100000 = np.load("tracking/Res/density-7/res100000.npy")
res200000 = np.load("tracking/Res/density-7/res200000.npy")

x = [100,250,500,750,1000,2000]
res = [np.round(np.mean(i),3) for i in [res10000,res25000,res50000,res75000,res100000,res200000]]
plt.figure(figsize=(20,10),dpi=300)
plt.plot(x,res)
plt.xlabel("人口密度（人/平方千米）")
plt.ylabel("可信度")
plt.show()