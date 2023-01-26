import numpy as np
import pickle

import static
from TrackUtils import *

def iterate(uid,location,map):
    BTConnection = findBTConnection(uid,location,map)
    print(len(BTConnection))
    selectedUser = np.random.choice(BTConnection,size=static.userPerIter,replace=False)
    print()

def findBTConnection(uid,location,map):
    BTConnectionCircle = findCircle(int(static.bluetoothDistance / 10), location)
    BTConnection = []
    for point in BTConnectionCircle:
        BTConnection.extend(map[point[0]][point[1]])
    BTConnection.remove(uid)    #去掉自己
    return BTConnection


if __name__ == '__main__':
    record = readObj("../mapAnalog/map/map0.pkl")
    map = record.map
    userList = record.userList
    # startTime = 50
    # uid = 50

    iterate(5,userList[4].location,map)

