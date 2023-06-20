import numpy as np

if __name__ == '__main__':
    path = "tracking/Credit/threshold-0.8/credit0.99-0.01.npy"
    data = np.load(path)
    # data = data.tolist()
    count = 0
    for index in range(len(data)):
        temp = data[index][0]
        if data[index][0] is True and data[index][1] is False:
            data[index][0] = False
            count += 1
    # data = np.array(data)
    # np.save(path, data)
    print("count=", str(count))
