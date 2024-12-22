# -*- coding: UTF-8 -*-

# constants
import numpy as np


# Now Using
# popDistribution = np.load("data/PopDistribution2.npy")  # Population distribution density for random user generation
speed = [1, 5, 15]  # speed m/s, in practice one frame = 10m, need to divide by 10 (or specify 10s to be recorded once)
# speedPoss = [0.6 / 3, 0.6 / 3, 0.6 / 3, 0.4]  # Possibility to choose the speed for controlling how many people move normally
oriPoss = [0.2, 0.2, 0.2, 0.2, 0.2]  # Possibilities when choosing the way forward
time = 60  # Interval between each iteration (in s)
mapSize = 1000  # Map size
userNum = 100000  # user num
creditPoss = [0.5,0.5]  # Distribution of real and cheating users

interval = 5  # Interval of finding someone (several TIME)
bluetoothDistance = 50  # Bluetooth connection distance
userPerIter = 5  # Number of verification per cycle
EXPusernum = 1000  # Number of user
Nround = 3
Threshold = 0.4  # Confidence threshold, what percentage of verifiers think it is true to pass the
extraThreshold = Threshold    #threshold of extra round

cpu = 16  # 线程数
