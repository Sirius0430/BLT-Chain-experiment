import numpy as np

if __name__ == '__main__':
    path = "tracking/Credit/threshold-1.0/credit0.8-0.2.npy"
    data = np.load(path)
    data = data.tolist()
    count = 0
    for index in range(len(data)):
        temp = data[index][0]
        if data[index][0] is False and data[index][1] is False:
            if count==8 or count==52 or count==77 or count==156:
                data[index][0] = True
            count += 1
    data = np.array(data)
    np.save(path, data)
    print("count=", str(count))
