import time

import numpy as np
import pickle
import multiprocessing

import static
from TrackUtils import *


def iterate(uid,creditRate,depth,time):
    # uid = args[0]
    # creditRate = args[1]
    # depth = args[2]
    # time = args[3]
    if depth == 4:
        return creditRate
    depth += 1
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map  # 证明者所处时刻的地图
    UuserLisr = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList  # 证明者所处时刻的用户列表
    user = UuserLisr[uid - 1]
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
        SEllipse = findEllipse(int(SUserPre.speed * static.time * 2 / 10), SUserBack.location,
                               SUserPre.location)  # 证明者的运动范围
        if len(np.intersect1d(UCircle, SEllipse)) > 0:  # 判断运动范围是否有交集
            creditRate += 1
        else:
            creditRate = 0
            assert "蓝牙连接失败"
    creditRate /= static.userPerIter

    resCR = 0  # 最终CreditRate
    for u in selectedUser:
        resCR += iterate(u, creditRate, depth, time - 1)
    resCR /= len(selectedUser)

    print("uid:{} done!".format(uid))
    return resCR


def findBTConnection(uid, location, map):
    BTConnectionCircle = findCircle(int(static.bluetoothDistance / 10), location)
    BTConnection = []
    for point in BTConnectionCircle:
        BTConnection.extend(map[point[0]][point[1]])
    BTConnection.remove(uid)  # 去掉自己
    return BTConnection


def mpStarter(args):
    uid = args[0]
    creditRate = args[1]
    depth = args[2]
    startTime = args[3]
    # return iterate(uid, creditRate, depth, time=startTime)

if __name__ == '__main__':
    startTime = 50
    uid = 500
    time1 = time.perf_counter()

    userList = np.random.choice(np.arange(1,static.userNum+1),size=100,replace=False)
    pool = multiprocessing.Pool(static.cpu)
    CRres = []
    for i in userList:
        startTime = np.random.choice(np.arange(5,96))
        res = pool.apply_async(func=iterate,args=(i,1,3,startTime))
        CRres.append(res.get())
    pool.close()
    pool.join()
    print(np.mean(CRres))
    # iterate(uid, 1, 0, time=startTime)
    time2 = time.perf_counter()
    print(time2 - time1)
