import os.path
import sys

import numpy as np
from math import sqrt
import pickle


# 给半径，确定圆的范围
# 基本思路:利用圆的中心对称，只计算四分之一个圆
def findCircle(r, c):  # r=radius,c=center
    c = np.array(c)
    res = []  # 在范围内的点
    for x in range(0, r + 1):
        for y in range(0, r + 1):
            if sqrt(x ** 2 + y ** 2) <= r:
                points = np.array([[x, y], [-x, y], [x, -y], [-x, -y]])  # 判定在圆内的点
                points = np.unique(points, axis=0)  # 数组去重
                res.extend(points)
    c_reshaped = c.reshape(1, 2)
    c_reshaped = np.repeat(c_reshaped, len(res), axis=0)
    return res + c_reshaped


def findEllipse(a, c1, c2):
    center = (c1 + c2) / 2
    res = []  # 在范围内的点
    for x in range(0, a + 1):
        for y in range(0, b + 1):
            if sqrt((x - c) ** 2 + y ** 2) + <= r:
                points = np.array([[x, y], [-x, y], [x, -y], [-x, -y]])  # 判定在圆内的点
                points = np.unique(points, axis=0)  # 数组去重
                res.extend(points)
    center_reshaped = center.reshape(1, 2)
    center_reshaped = np.repeat(center_reshaped, len(res), axis=0)
    return []


def readObj(path):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(path))))  # 将MapRecord定义添加到环境变量
    f = open(path, "rb")
    record = pickle.load(f)
    return record
