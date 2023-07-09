# -*- coding: UTF-8 -*-

import time
import gc

import numpy as np
import pickle
import multiprocessing
import collections

from module import static
from TrackUtils import *

banList = []
lock = multiprocessing.Lock()


def iterate(uid, creditRate, depth, time):
    # uid = args[0]
    # creditRate = args[1]
    # depth = args[2]
    # time = args[3]
    if depth == static.Nround:
        return creditRate
    depth += 1
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map  # 证明者所处时刻的地图
    UuserList = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList  # 证明者所处时刻的用户列表
    user = UuserList[uid - 1]

    BTConnection = findBTConnection(user.uid, user.location, Umap)
    userNum = len(BTConnection)
    creditRate = 0
    selectedUser = []
    if userNum < static.userPerIter:
        selectedUser = BTConnection
    else:
        selectedUser = np.random.choice(BTConnection, size=static.userPerIter, replace=False)

    del Umap
    del UuserList
    del BTConnection
    gc.collect()

    UCircle = findCircle(int(static.bluetoothDistance / 10), user.location)  # 被证明者的蓝牙连接
    for s in selectedUser:
        SRecordPre = readObj("../mapAnalog/map/map{}.pkl".format(time - static.interval))  # 证明者前一个位置
        SUserPre = SRecordPre.userList[s - 1]
        SRecordBack = readObj("../mapAnalog/map/map{}.pkl".format(time + static.interval))  # 证明者后一个位置
        SUserBack = SRecordBack.userList[s - 1]
        # SEllipse = findEllipse(int(SUserPre.speed * module.time * 2 * module.interval / 10), SUserBack.location,
        #                        SUserPre.location)  # 证明者的运动范围
        # if len(np.intersect1d(UCircle, SEllipse)) > 0:  # 判断运动范围是否有交集
        hasIntersact = findEllipse(int(SUserPre.speed * static.time * 2 * static.interval / 10), SUserBack.location,
                                   SUserPre.location, UCircle)  # 判断证明者的运动范围是否有交集,中间隔了两个interval,所以时间要x2
        if hasIntersact:
            creditRate += 1
        else:
            creditRate = 0
            assert "蓝牙连接失败"

        del SRecordPre
        del SUserPre
        del SRecordBack
        del SUserBack
        # del SEllipse  #使用hasIntersact取代SEllipse
        gc.collect()
    creditRate /= static.userPerIter

    resCR = 0  # 最终可信度
    for u in selectedUser:
        resCR += iterate(u, creditRate, depth, time - static.interval)

    if len(selectedUser) == 0:
        resCR = 0
    else:
        resCR /= len(selectedUser)
    # print("uid:{} CR:{}".format(uid,resCR))

    return resCR


def addSelectedUser(BTConnection, selectedUserList):
    BTConnection = list(set(BTConnection) - set(banList))
    restBTConnection = list(set(BTConnection) - set(selectedUserList))
    addedUser = np.random.choice(restBTConnection, size=1, replace=False)
    selectedUserList.append(addedUser)
    return selectedUserList


def extraIter(uid, time):
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map  # 证明者所处时刻的地图
    UuserList = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList  # 证明者所处时刻的用户列表
    user = UuserList[uid - 1]

    BTConnection = findBTConnection(user.uid, user.location, Umap)
    BTConnection = list(set(BTConnection) - set(banList))
    userNum = len(BTConnection)
    selectedUser = []
    if userNum < static.userPerIter:
        selectedUser = BTConnection
    else:
        selectedUser = np.random.choice(BTConnection, size=static.userPerIter, replace=False)

    del Umap
    # del BTConnection
    gc.collect()
    sCreditIndex = 0  # 可信用户计数
    for s in selectedUser:
        sUser = UuserList[s - 1]
        sCredit = not (user.credit ^ sUser.credit)
        if sCredit == True:
            sCreditIndex += 1
    threshold = sCreditIndex / static.userPerIter
    if threshold >= static.extraThreshold:  # true的人数多
        return True
    else:
        return False


def iterate2(uid, depth, time, Auid, trueRes):  # 计算验证准确率
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map  # 证明者所处时刻的地图
    UuserList = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList  # 证明者所处时刻的用户列表
    user = UuserList[uid - 1]
    if depth == static.Nround:
        Auser = UuserList[Auid - 1]
        return not (user.credit ^ Auser.credit), trueRes
    depth += 1

    BTConnection = findBTConnection(user.uid, user.location, Umap)
    BTConnection = list(set(BTConnection) - set(banList))
    userNum = len(BTConnection)
    selectedUser = []
    if userNum == 0:
        return False, trueRes
    if userNum < static.userPerIter:
        selectedUser = BTConnection
    else:
        selectedUser = np.random.choice(BTConnection, size=static.userPerIter, replace=False)

    del Umap
    # del BTConnection
    gc.collect()

    sCreditIndex = 0  # 可信用户计数
    sCreditDict = {}  # 记录每个用户是否可信
    for s in selectedUser:
        sUser = UuserList[s - 1]
        sCredit, _ = iterate2(s, depth, time, Auid, trueRes)
        sCreditDict[s] = sCredit

    for k, v in sCreditDict.items():
        if v == True:
            sCreditIndex += 1
        else:
            extraRes = extraIter(k, time)
            if extraRes == True:
                sCreditIndex += 1
                sCreditDict[k] = True
            else:
                lock.acquire()
                banList.append(k)
                lock.release()

    threshold = sCreditIndex / min(static.userPerIter, userNum)
    if threshold >= static.Threshold:  # true的人数多
        return True, trueRes
    else:
        return False, trueRes

    # if len(selectedUser) == 0:
    #     return "Detected"
    # elif len(selectedUser) == 1:
    #     if bool(sCreditIndex):
    #         return "True"
    #     else:
    #         return "False"
    # else:
    #     if sCreditIndex == 0:
    #         return "False"
    #     if sCreditIndex == 1:
    #         # 找到true，如果全部是false，返回false，否则返回detected
    #         extraUID = -1  # 不正常用户的uid
    #         for k, v in sCreditDict.items():
    #             if v == "True":
    #                 extraUID = k
    #         extraBTConnection = findBTConnection(extraUID, user.location, Umap)
    #         extraNum = len(extraBTConnection)
    #         extraSelectedUser = []
    #         if extraNum < module.userPerIter:
    #             extraSelectedUser = extraBTConnection
    #         else:
    #             extraSelectedUser = np.random.choice(extraBTConnection, size=module.userPerIter, replace=False)
    #         for s in extraSelectedUser:
    #             extraWitness = UuserList[s - 1]
    #             if extraWitness.credit == "True":
    #                 return "Detected"
    #         return "False"
    #
    #     if sCreditIndex == len(selectedUser) - 1:
    #         # 找到false，如果全部是true，返回true，否则返回detected
    #         extraUID = -1  # 不正常用户的uid
    #         for k, v in sCreditDict.items():
    #             if v == "False":
    #                 extraUID = k
    #         extraBTConnection = findBTConnection(extraUID, user.location, Umap)
    #         extraNum = len(extraBTConnection)
    #         extraSelectedUser = []
    #         if extraNum < module.userPerIter:
    #             extraSelectedUser = extraBTConnection
    #         else:
    #             extraSelectedUser = np.random.choice(extraBTConnection, size=module.userPerIter, replace=False)
    #         for s in extraSelectedUser:
    #             extraWitness = UuserList[s - 1]
    #             if extraWitness.credit == "False":
    #                 return "Detected"
    #         return "True"
    #     if sCreditIndex == len(selectedUser):
    #         return "True"
    #     else:
    #         return "Detected"


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


def callBack2(res):
    creditRes.append(res)


def errCallBack(err):
    print("ERROR! {}".format(err))


if __name__ == '__main__':
    time1 = time.perf_counter()
    userList = np.random.choice(np.arange(1, static.userNum + 1), size=static.EXPusernum, replace=False)
    pool = multiprocessing.Pool(static.cpu)
    # CR实验
    # CRres = []
    # for i in userList:
    #     startTime = np.random.choice(np.arange(25, 75))
    #     pool.apply_async(func=iterate, args=(i, 1, 0, startTime), callback=callBack, error_callback=errCallBack)
    # pool.close()
    # pool.join()
    # print("final res:{}".format(np.mean(CRres)))
    # np.save("Res/density-{}/res{}.npy".format(module.userPerIter, module.userNum), CRres)

    # Credit实验
    creditRes = []
    for i in userList:
        startTime = np.random.choice(np.arange(25, 75))
        UuserList = readObj("../mapAnalog/map/map{}.pkl".format(startTime)).userList
        trueRes = UuserList[i - 1].credit
        pool.apply_async(func=iterate2, args=(i, 0, startTime, i, trueRes), callback=callBack2,
                         error_callback=errCallBack)
    pool.close()
    pool.join()
    print(creditRes)

    time2 = time.perf_counter()
    np.save("Credit/threshold-{}/credit{}-{}.npy".format(static.Threshold, static.creditPoss[0], static.creditPoss[1]),
            creditRes)
    print("time:{}".format(time2 - time1))
