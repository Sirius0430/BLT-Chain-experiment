# -*- coding: UTF-8 -*-

import os.path
import sys

import numpy as np
from math import sqrt
import pickle


# Give the radius and determine the extent of the circle
# Basic idea: use the center symmetry of the circle to calculate only a quarter of the circle
from module import static


def findCircle(r, c):  # r=radius,c=center
    c = np.array(c)
    xmin = max(0, int(c[0] - r))
    xmax = min(static.mapSize, int(c[0] + r))
    ymin = max(0, int(c[1] - r))
    ymax = min(static.mapSize, int(c[1] + r))
    res = []  # Points in the range
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            if sqrt((x-c[0]) ** 2 + (y-c[1]) ** 2) <= r:
                res.extend([[x, y]])
    return res


def findEllipse(a, c1, c2,circle):
    center = (np.array(c1) + np.array(c2)) / 2
    res = []  # Points in the range
    x1 = c1[0]
    y1 = c1[1]
    x2 = c2[0]
    y2 = c2[1]
    xf = -abs(x1 - x2) / 2
    yf = abs(y1 - y2) / 2
    x0 = center[0]
    y0 = center[1]
    if 2 * a <= sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2):
        assert "a>c"
    xmax = min(static.mapSize, int(sqrt(a ** 2 - yf ** 2) + x0))
    xmin = max(0, int(-sqrt(a ** 2 - yf ** 2) + x0))
    ymax = min(static.mapSize, int(sqrt(a ** 2 - xf ** 2) + y0))
    ymin = max(0, int(-sqrt(a ** 2 - xf ** 2) + y0))
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            if (sqrt((x - x1) ** 2 + (y - y1) ** 2) + sqrt((x - x2) ** 2 + (y - y2) ** 2)) <= 2 * a:
                # res.extend([[x, y]])
                if [x,y] in circle:
                    return True
    # return res
    return False

def readObj(path):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(path))))  # Add the MapRecord definition to the environment variable
    f = open(path, "rb")
    record = pickle.load(f)
    return record


if __name__ == '__main__':
    # circle = findCircle(5,[10,10])
    # ellipse = findEllipse(5,[10,2],[10,8],circle)
    # res = np.zeros((20,20))
    # for x in range(20):
    #     for y in range(20):
    #         if [x,y] in circle:
    #             res[x,y]+=1
    #         if [x,y] in ellipse:
    #             res[x,y]+=1
    # print()

    a = True
    b = False
    print(not a^b)

