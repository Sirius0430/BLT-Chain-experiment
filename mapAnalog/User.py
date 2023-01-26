import numpy as np
import static


# 用户
class User:
    uid = -1  # id
    location = [-1, -1]  # 位置
    credit = True  # 可信度
    speed = 0  # 移动速度
    orientation = "none"  # 当前行进的方向

    def __init__(self, pid, credit=True):
        self.uid = pid
        self.location = self.__randomChooseStartLocation(np.load("../data/PopDistribution.npy"))  # 人口分布密度，用于随机生成用户)
        self.credit = credit
        self.speed = np.random.choice(static.speed)
        # print("User{} created,Orientation:{},speed:{},location:{}".format(self.uid, self.orientation, self.speed,self.location))

    # 随机生成起始位置(根据概率分布）
    def __randomChooseStartLocation(self, data):
        index = np.arange(1000 * 1000 + 1)[1:]
        res = np.random.choice(index, p=data.flatten().ravel())
        # +1是为了将数组起始位置改为1
        x = int(res / 1000) + 1
        y = res % 1000 + 1
        return [x, y]

    def move(self):
        if self.orientation == "none":
            self.orientation = self.__changeOrientation()
            return
        else:
            dist = int(self.speed * static.time / 10)  # 每次移动的格子数

            if self.orientation == "left":
                # 是否超出边界
                temp = self.location[1] - dist
                # 不超出则移动
                if temp > 0:
                    self.location = [self.location[0], temp]
                    # 超出则改变方向
                else:
                    self.orientation = self.__changeOrientation()
            if self.orientation == "right":
                # 是否超出边界
                temp = self.location[1] + dist
                # 不超出则移动
                if temp <= static.mapSize:
                    self.location = [self.location[0], temp]
                # 超出则改变方向
                else:
                    self.orientation = self.__changeOrientation()
            if self.orientation == "up":
                # 是否超出边界
                temp = self.location[0] - dist
                # 不超出则移动
                if temp > 0:
                    self.location = [temp, self.location[1]]
                # 超出则改变方向
                else:
                    self.orientation = self.__changeOrientation()
            if self.orientation == "down":
                # 是否超出边界
                temp = self.location[0] + dist
                # 不超出则移动
                if temp < 1000:
                    self.location = [temp, self.location[1]]
                # 超出则改变方向
                else:
                    self.orientation = self.__changeOrientation()
            # print("User{},Orientation:{},location:{}".format(self.uid, self.orientation, self.location))
            # 每次移动结束之后，有一定概率改变前进方向
            self.orientation = self.__randomChangeOrientation()

    def __changeOrientation(self):
        return np.random.choice(["left", "right", "up", "down", "none"], p=static.oriPoss)

    def __randomChangeOrientation(self):
        ifChange = np.random.choice([True, False], p=static.changeOriPoss)
        if ifChange:
            newOri = self.__changeOrientation()
            if newOri == self.orientation:
                return self.__randomChangeOrientation()
            else:
                # print("Orientation Changed:{}".format(newOri))
                return newOri
        else:
            return self.orientation
