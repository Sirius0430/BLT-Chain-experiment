import numpy as np

if __name__ == '__main__':


    test = np.load("test.npy",allow_pickle=True)
    for i in range(len(test)):
        temp = test[i]
        # test = test.tolist()
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if len(temp[i][j])>0:
                    print("[{},{}]:{}".format(i,j,len(temp[i][j])))
        print(" ")
