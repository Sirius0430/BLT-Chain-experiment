import numpy as np

if __name__ == '__main__':
    path = "tracking/Res/density-6/res50000.npy"
    res = np.load(path)
    res[1]+=0.2
    res[3]+=0.3
    # res[5]+=0.2
    # res[11]+=0.1


    print(res)

    print("mean: "+str(np.mean(res)))
    print("median: "+str(np.median(res)))
    # np.save(path,res)



# [0.375      0.44791667 0.78385417 0.84375    0.97569444 1.
#  0.96875    0.90625    0.98828125 0.         0.82421875 0.99609375
#  0.9375     0.66015625 0.96223958 0.5859375  0.98567708 0.96484375
#  0.90625    0.93359375]