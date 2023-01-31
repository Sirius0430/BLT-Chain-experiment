import numpy as np
import pickle

import static
from TrackUtils import *


def iterate(user, map, creditRate, depth, time):
    if depth == 4:
        return creditRate
    depth += 1
    BTConnection = findBTConnection(user.uid, user.location, map)
    userNum = len(BTConnection)
    creditRate = 0
    selectedUser = []
    if userNum < static.userPerIter:
        creditRate = userNum / static.userPerIter
        selectedUser = BTConnection
    else:
        creditRate = 1
        selectedUser = np.random.choice(BTConnection, size=static.userPerIter, replace=False)
    UCircle = findCircle(int(user.speed * static.time / 10),user.location)  # 被证明者的运动范围
    for s in selectedUser:
        SRecordPre = readObj("../mapAnalog/map/map{}.pkl".format(time - 1))  # 证明者前一个位置
        SUserPre = SRecordPre.userList[s - 1]
        SRecordBack = readObj("../mapAnalog/map/map{}.pkl".format(time + 1))  # 证明者后一个位置
        SUserBack = SRecordBack.userList[s - 1]
        SEllipse = findEllipse(int(SUserPre.speed * static.time * 2 / 10), SUserBack.location, SUserPre.location)  # 证明者的运动范围
        if len(np.intersect1d(UCircle,SEllipse))>0: #判断运动范围是否有交集
            creditRate = 1
        else:
            creditRate = 0
            raise EOFError
        print()


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
    user = userList[6]
    startTime = 3
    # uid = 50

    iterate(user, map, 1, 1, time=startTime)
