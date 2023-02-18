import time
import gc

import numpy as np
import pickle
import multiprocessing

import static
from TrackUtils import *


def iterate(uid, creditRate, depth, time):
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

    del Umap
    del UuserLisr
    del BTConnection
    gc.collect()

    # 作弊用户
    fakeUser = []

    UCircle = findCircle(int(static.bluetoothDistance / 10), user.location)  # 被证明者的蓝牙连接
    for s in selectedUser:
        SRecordPre = readObj("../mapAnalog/map/map{}.pkl".format(time - static.interval))  # 证明者前一个位置
        SUserPre = SRecordPre.userList[s - 1]
        SRecordBack = readObj("../mapAnalog/map/map{}.pkl".format(time + static.interval))  # 证明者后一个位置
        SUserBack = SRecordBack.userList[s - 1]
        # SEllipse = findEllipse(int(SUserPre.speed * static.time * 2 * static.interval / 10), SUserBack.location,
        #                        SUserPre.location)  # 证明者的运动范围
        # if len(np.intersect1d(UCircle, SEllipse)) > 0:  # 判断运动范围是否有交集
        hasIntersact = findEllipse(int(SUserPre.speed * static.time * 2 * static.interval / 10), SUserBack.location,
                               SUserPre.location,UCircle)  # 判断证明者的运动范围是否有交集,中间隔了两个interval,所以时间要x2
        if hasIntersact:
            creditRate += 1
        else:
            creditRate = 0
            assert "蓝牙连接失败"

        # 记录作弊用户
        fakeUser.append(s)

        del SRecordPre
        del SUserPre
        del SRecordBack
        del SUserBack
        # del SEllipse
        gc.collect()
    creditRate /= static.userPerIter

    resCR = 0  # 最终CreditRate
    for u in selectedUser:
        resCR += iterate(u, creditRate, depth, time - static.interval)
    if len(selectedUser) == 0:
        resCR = 0
    else:
        resCR /= len(selectedUser)
    # print("uid:{} CR:{}".format(uid,resCR))

    #计算发现作弊的可能性
    # if len(fakeUser)==0:



    return resCR


def findBTConnection(uid, location, map):
    BTConnectionCircle = findCircle(int(static.bluetoothDistance / 10), location)
    BTConnection = []
    for point in BTConnectionCircle:
        BTConnection.extend(map[point[0]][point[1]])
    BTConnection.remove(uid)  # 去掉自己
    return BTConnection


def callBack(res):
    CRres.append(res)
    print("uid:{},CR:{}".format(i, res))


def errCallBack(err):
    print("ERROR! {}".format(err))



if __name__ == '__main__':
    time1 = time.perf_counter()

    userList = np.random.choice(np.arange(1, static.userNum + 1), size=20, replace=False)
    pool = multiprocessing.Pool(static.cpu)
    CRres = []
    for i in userList:
        startTime = np.random.choice(np.arange(25, 75))
        pool.apply_async(func=iterate, args=(i, 1, 1, startTime), callback=callBack, error_callback=errCallBack)
        # CRres.append(res.get())
    pool.close()
    pool.join()
    print("final res:{}".format(np.mean(CRres)))
    # iterate(uid, 1, 0, time=startTime)
    time2 = time.perf_counter()
    print("time:{}".format(time2 - time1))
    # np.save("Res/density-5/res100000.npy", CRres)
