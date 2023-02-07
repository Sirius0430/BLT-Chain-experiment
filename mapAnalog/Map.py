import numpy as np
from User import User
import static
from collections import Counter
class Map:
    size = static.mapSize #地图大小
    userNum = static.userNum   #用户数量
    userList = []  #用户列表
    records = []    #每个时间地图上用户位置的集合

    def __init__(self):
        self.size = self.size
        # create users
        for i in range(self.userNum):
            user = User(i+1)
            self.userList.append(user)
        # init map
        startMap = self.__initMap()
        for u in self.userList:
            startMap[u.location[0]][u.location[1]].append(u.uid)
        self.records.append(startMap)

    def __initMap(self):
        startMap = np.zeros((self.size+1, self.size+1))
        startMap = startMap.tolist()
        for i in range(len(startMap)):
            for j in range(len(startMap)):
                startMap[i][j] = []
        return startMap

    def forward(self):
        map = self.__initMap()
        for u in self.userList:
            u.move()
            map[u.location[0]][u.location[1]].append(u.uid)
        self.records.append(map)
        # print(map[500][500])


class MapRecord:
    def __init__(self, map, userList):
        self.map = map
        self.userList = userList






