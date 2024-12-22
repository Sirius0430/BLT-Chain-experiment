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
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map  # Map of Applicant's moment in time
    UuserList = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList  # Map of Applicant's user list in time
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

    UCircle = findCircle(int(static.bluetoothDistance / 10), user.location)  # Bluetooth connectivity of Witness
    for s in selectedUser:
        SRecordPre = readObj("../mapAnalog/map/map{}.pkl".format(time - static.interval))  # Previous position of Applicant
        SUserPre = SRecordPre.userList[s - 1]
        SRecordBack = readObj("../mapAnalog/map/map{}.pkl".format(time + static.interval))  # latter position of Applicant
        SUserBack = SRecordBack.userList[s - 1]
        # SEllipse = findEllipse(int(SUserPre.speed * module.time * 2 * module.interval / 10), SUserBack.location,
        #                        SUserPre.location)  # moving range of applicant
        # if len(np.intersect1d(UCircle, SEllipse)) > 0:  # Determine if the ranges of motion intersect
        # Determine whether the range of motion of the provers intersects, separated by two intervals, so the time has to be x2
        hasIntersact = findEllipse(int(SUserPre.speed * static.time * 2 * static.interval / 10), SUserBack.location,
                                   SUserPre.location, UCircle)
        if hasIntersact:
            creditRate += 1
        else:
            creditRate = 0
            assert "Error in Bluetooth connection"

        del SRecordPre
        del SUserPre
        del SRecordBack
        del SUserBack
        # del SEllipse
        gc.collect()
    creditRate /= static.userPerIter

    resCR = 0  # Final CR
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
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map  # Map of Applicant's moment in time
    UuserList = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList  # Map of Applicant's user list in time
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
    sCreditIndex = 0  # Trusted User Count
    for s in selectedUser:
        sUser = UuserList[s - 1]
        sCredit = not (user.credit ^ sUser.credit)
        if sCredit == True:
            sCreditIndex += 1
    threshold = sCreditIndex / static.userPerIter
    if threshold >= static.extraThreshold:  #
        return True
    else:
        return False


def iterate2(uid, depth, time, Auid, trueRes):  # Calculate verification accuracy
    Umap = readObj("../mapAnalog/map/map{}.pkl".format(time)).map
    UuserList = readObj("../mapAnalog/map/map{}.pkl".format(time)).userList
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

    sCreditIndex = 0  # Trusted User Count
    sCreditDict = {}  # Record whether each user is trustworthy
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
    if threshold >= static.Threshold:
        return True, trueRes
    else:
        return False, trueRes

    extraSelectedUser = []
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
    BTConnection.remove(uid)
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
    # CR Experiment
    # CRres = []
    # for i in userList:
    #     startTime = np.random.choice(np.arange(25, 75))
    #     pool.apply_async(func=iterate, args=(i, 1, 0, startTime), callback=callBack, error_callback=errCallBack)
    # pool.close()
    # pool.join()
    # print("final res:{}".format(np.mean(CRres)))
    # np.save("Res/density-{}/res{}.npy".format(module.userPerIter, module.userNum), CRres)

    # Credit Experiment
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
