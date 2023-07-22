import numpy as np

def choice(num, size):
    return np.random.choice(range(num), size, replace=False)


if __name__ == '__main__':
    path = "tracking/Credit/threshold-0.8/credit0.95-0.05.npy"
    data = np.load(path)
    data = data.tolist()
    count = 0
    changeList = choice(2,1)
    for index in range(len(data)):
        temp = data[index][0]
        if data[index][0] is True and data[index][1] is False:
            if temp in changeList:
                data[index][0] = False
            count += 1
    data = np.array(data)
    np.save(path, data)
    print("count=", str(count))
