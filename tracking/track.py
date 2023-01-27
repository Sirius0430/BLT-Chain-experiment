import numpy as np
import pickle

import static
from TrackUtils import *


def iterate(uid, location, map, creditRate, depth,time):
    if depth == 4:
        return creditRate
    depth += 1
    BTConnection = findBTConnection(uid, location, map)
    userNum = len(BTConnection)
    creditRate = 0
    selectedUser = []
    if userNum < static.userPerIter:
        creditRate = userNum / static.userPerIter
        selectedUser = BTConnection
    else:
        creditRate = 1
        selectedUser = np.random.choice(BTConnection, size=static.userPerIter, replace=False)
    for u in selectedUser:
        readObj("../mapAnalog/map/map{}".format(time))


def findBTConnection(uid, location, map):
    BTConnectionCircle = findCircle(int(static.bluetoothDistance / 10), location)
    BTConnection = []
    for point in BTConnectionCircle:
        BTConnection.extend(map[point[0]][point[1]])
    BTConnection.remove(uid)  # 去掉自己
    return BTConnection


if __name__ == '__main__':
    record = readObj("../mapAnalog/map/map0.pkl")
    map = record.map
    userList = record.userList
    startTime = 50
    # uid = 50

    iterate(5, userList[4].location, map, 1, 1,time=startTime)
