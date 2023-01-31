import time

import numpy as np
import pickle

import static
from TrackUtils import *


# 证明者范围应该为圆，被证明者范围应该为椭圆，需要修改！！
def iterate(uid, creditRate, depth, time):
    if depth == 4:
        return creditRate
    depth += 1
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map  #证明者所处时刻的地图
    UuserLisr = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList  #证明者所处时刻的用户列表
    user = UuserLisr[uid-1]
    BTConnection = findBTConnection(user.uid, user.location, Umap)
    userNum = len(BTConnection)
    creditRate = 0
    selectedUser = []
    if userNum < static.userPerIter:
        selectedUser = BTConnection
    else:
        selectedUser = np.random.choice(BTConnection, size=static.userPerIter, replace=False)
    UCircle = findCircle(int(static.bluetoothDistance / 10), user.location)  # 被证明者的蓝牙连接

    for s in selectedUser:
        SRecordPre = readObj("../mapAnalog/map/map{}.pkl".format(time - 1))  # 证明者前一个位置
        SUserPre = SRecordPre.userList[s - 1]
        SRecordBack = readObj("../mapAnalog/map/map{}.pkl".format(time + 1))  # 证明者后一个位置
        SUserBack = SRecordBack.userList[s - 1]
        SEllipse = findEllipse(int(SUserPre.speed * static.time * 2 / 10), SUserBack.location, SUserPre.location)  # 证明者的运动范围
        if len(np.intersect1d(UCircle,SEllipse))>0: #判断运动范围是否有交集
            creditRate += 1
        else:
            creditRate = 0
            assert "蓝牙连接失败"
    creditRate /= static.userPerIter

    static.test+=1
    print(static.test)

    resCR = 0   #最终CreditRate
    for u in selectedUser:
        resCR+=iterate(u,creditRate,depth,time-1)
    resCR/=len(selectedUser)
    return resCR


def findBTConnection(uid, location, map):
    BTConnectionCircle = findCircle(int(static.bluetoothDistance / 10), location)
    BTConnection = []
    for point in BTConnectionCircle:
        BTConnection.extend(map[point[0]][point[1]])
    BTConnection.remove(uid)  # 去掉自己
    return BTConnection


if __name__ == '__main__':
    record = readObj("../mapAnalog/map/map50.pkl")
    map = record.map
    userList = record.userList
    user = userList[6]
    startTime = 50
    # uid = 50
    time1 = time.perf_counter()
    iterate(1000, 1, 0, time=startTime)
    time2 = time.perf_counter()
    print(time2-time1)
