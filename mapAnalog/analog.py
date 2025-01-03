import sys

from Map import Map, MapRecord
import numpy as np
import pickle


def main():
    m = Map()
    obj0 = pickle.dumps(MapRecord(m.records[-1], m.userList))
    with open("map/map0.pkl", "wb") as f:
        f.write(obj0)
    for i in range(1, 101):
        m.forward()
        obj = pickle.dumps(MapRecord(m.records[-1], m.userList))
        with open("map/map{}.pkl".format(i), "wb") as f:
            f.write(obj)
        print("map{} done".format(i))


if __name__ == '__main__':
    main()
