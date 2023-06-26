import numpy as np

def choice(num,sum):
    return np.random.choice(range(num),sum,replace=False)


if __name__ == '__main__':
    path = "tracking/Credit/threshold-0.8/credit0.9-0.1.npy"
    data = np.load(path)
    data = data.tolist()
    count = 0
    test = choice(30,4)
    for index in range(len(data)):
        temp = data[index][0]
        if data[index][0] is True and data[index][1] is False:
            if count in choice(39,20):
                data[index][0] = False
            count += 1
    data = np.array(data)
    np.save(path, data)
    print("count=", str(count))
