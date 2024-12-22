# -*- coding: UTF-8 -*-

import numpy as np
from module import static


# 用户
class User:
    uid = -1
    location = [-1, -1]
    credit = True
    speed = 0
    orientation = "none"

    def __init__(self, pid):
        self.uid = pid
        self.location = self.__randomChooseStartLocation(np.load("../data/PopDistribution.npy"))  # Population distribution density for random user generation)
        self.credit = np.random.choice([True,False],p=static.creditPoss)
        self.speed = np.random.choice(static.speed)
        # print("User{} created,Orientation:{},speed:{},location:{}".format(self.uid, self.orientation, self.speed,self.location))

    # Random generation of starting positions (based on probability distribution)
    def __randomChooseStartLocation(self, data):
        index = np.arange(100 * 100)
        res = np.random.choice(index, p=data.flatten().ravel())
        x = int(res / 100)
        y = res % 100
        xAdd = np.random.choice(np.arange(0,10))
        yAdd = np.random.choice(np.arange(0,10))
        # To change the starting position of the array to 1
        return [10*x+xAdd+1, 10*y+yAdd+1]

    def move(self):
        if self.orientation == "none":
            self.orientation = self.__changeOrientation()
            return
        else:
            for _ in range(int(static.time/10)):
                dist = int(self.speed)  # Distance per move

                if self.orientation == "left":
                    # Whether the boundary is exceeded
                    temp = self.location[1] - dist
                    # Move if not exceeded
                    if temp > 0:
                        self.location = [self.location[0], temp]
                        # Change of direction if exceeded
                    else:
                        self.orientation = self.__changeOrientation()
                if self.orientation == "right":
                    # Whether the boundary is exceeded
                    temp = self.location[1] + dist
                    # Move if not exceeded
                    if temp <= static.mapSize:
                        self.location = [self.location[0], temp]
                    # Change of direction if exceeded
                    else:
                        self.orientation = self.__changeOrientation()
                if self.orientation == "up":
                    # Whether the boundary is exceeded
                    temp = self.location[0] - dist
                    # Move if not exceeded
                    if temp > 0:
                        self.location = [temp, self.location[1]]
                    # Change of direction if exceeded
                    else:
                        self.orientation = self.__changeOrientation()
                if self.orientation == "down":
                    # Whether the boundary is exceeded
                    temp = self.location[0] + dist
                    # Move if not exceeded
                    if temp < static.mapSize:
                        self.location = [temp, self.location[1]]
                    # Change of direction if exceeded
                    else:
                        self.orientation = self.__changeOrientation()
                # print("User{},Orientation:{},location:{}".format(self.uid, self.orientation, self.location))
            # Randomly change forward direction after each move
            self.orientation = self.__changeOrientation()

    def __changeOrientation(self):
        return np.random.choice(["left", "right", "up", "down", "none"], p=static.oriPoss)


