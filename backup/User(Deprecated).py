import numpy as np
from static import *


# 用户父类
class User:
    uid = -1  # id
    location = [-1, -1]  # 位置
    credit = True  # 可信度
    speed = 0  # 移动速度
    orientation = "none"  # 当前行进的方向


# 在建筑间沿特定道路移动的用户
class BuildingUser(User):
    willing = "none"  # 想去的地方
    current = "none"  # 当前在的建筑
    orientation = "none"  # 当前行进的方向
    route = []  # 当前的路径
    endpoint = 0  # 路径的转折点在route数组中的序列
    speed = 3  # 移动速度

    finish = 0  # 测试用，若为1，则表示当前路径已经结束，用于一次性路径测试

    def __init__(self, pid, location, credit, current):
        self.uid = pid
        self.location = location
        self.credit = credit
        self.current = current

    # 决定目标地点
    def decideDes(self):
        if self.willing == "none":
            index = np.random.choice([1, 2, 3, 4, "none"], p=buildingP.ravel())
            if index != "none" and index != str(self.current):
                self.willing = int(index)
                self.route = road[self.current][self.willing]
                self.endpoint = 1
                # 确定起始方向
                # 横坐标相同则横向走
                if self.route[0][0] == self.route[1][0]:
                    # 判断左右方向
                    if self.route[0][1] < self.route[1][1]:
                        self.orientation = "right"
                    else:
                        self.orientation = "left"
                # 纵坐标相同则纵向走
                if self.route[0][1] == self.route[1][1]:
                    # 判断上下方向
                    if self.route[0][0] < self.route[1][0]:
                        self.orientation = "down"
                    else:
                        self.orientation = "up"
                # print("Person {} will go to building{} from building{}.orientation:{},route:{}"
                #       .format(self.uid, self.willing, self.current, self.orientation, self.route))
        else:
            return

    def move(self):
        # 测试用
        if self.finish == 1:
            return 0
        self.decideDes()
        if self.orientation == "left":
            res = self.location[1] - self.speed
            # 到达端点
            if res < self.route[self.endpoint][1]:
                self.location[1] = self.route[self.endpoint][1]
                self.__changeOrientation()
            else:
                self.location[1] = res
        if self.orientation == "right":
            res = self.location[1] + self.speed
            # 到达端点
            if res > self.route[self.endpoint][1]:
                self.location[1] = self.route[self.endpoint][1]
                self.__changeOrientation()
            else:
                self.location[1] = res
        if self.orientation == "up":
            res = self.location[0] - self.speed
            # 到达端点
            if res < self.route[self.endpoint][0]:
                self.location[0] = self.route[self.endpoint][0]
                self.__changeOrientation()
            else:
                self.location[0] = res
        if self.orientation == "down":
            res = self.location[0] + self.speed
            # 到达端点
            if res > self.route[self.endpoint][0]:
                self.location[0] = self.route[self.endpoint][0]
                self.__changeOrientation()
            else:
                self.location[0] = res

    def __changeOrientation(self):
        if self.endpoint + 1 >= len(self.route):
            return self.__arrive()
        else:
            thisEndpoint = np.array(self.route[self.endpoint])
            nextEndpoint = np.array(self.route[self.endpoint + 1])
            res = np.subtract(nextEndpoint, thisEndpoint)
            if res[0] == 0:
                if res[1] > 0:
                    self.orientation = "right"
                if res[1] < 0:
                    self.orientation = "left"
            elif res[1] == 0:
                if res[0] > 0:
                    self.orientation = "down"
                if res[0] < 0:
                    self.orientation = "up"
        self.endpoint += 1

    def __arrive(self):
        self.current = self.willing
        self.willing = "none"
        self.orientation = "none"
        self.route = []
        self.endpoint = 0
        self.finish = 1
        # print("Person {} have arrived building{},location:{}".format(self.uid, self.current, self.location))


# 在地图上随机游荡的用户
class RandomUser(User):
    speedRange = np.arange(5)[1:]

    def __init__(self, pid, credit):
        self.uid = pid
        self.location = np.random.choice(1000, 2, replace=True)
        self.credit = credit

    def move(self):
        self.__setParams()
        print(self.orientation + " " + str(self.speed))

    # 设置方向、速度等参数
    def __setParams(self):
        p = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        self.orientation = np.random.choice(["left", "right", "up", "down", "none"], p=p.ravel())
        if self.orientation == "none":
            self.speed = 0
        else:
            self.speed = np.random.choice(self.speedRange)
