import os.path
from PIL import Image
import numpy as np


#Deprecated
# def readTif(path):
#     img = Image.open(path)
#     data = np.array(img)
#     data = data[:100, :100]
#     data[data < 0] = 0
#     data = np.repeat(data, 10, axis=1)
#     data = np.repeat(data, 10, axis=0)
#     data = data / data.sum()
#     return data

def readTif(path):
    img = Image.open(path)
    data = np.array(img)
    data = data[:100, :100]
    data[data < 0] = 0
    data = data / data.sum()
    return data


def select(data):
    index = np.arange(100 * 100 + 1)[1:]
    res = np.random.choice(index, p=data.flatten().ravel())
    x = int(res / 100)
    y = res % 100
    return x, y


if __name__ == '__main__':
    path = "WuhanData.tif"
    data = readTif(path)
    if not os.path.exists("PopDistribution.npy"):
        np.save("PopDistribution.npy", data)
    print(len(data))
    x,y = select(data)
