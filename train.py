import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

DATA = 'feature/all.txt'

def main():
    X, Y = [], []
    # read data set
    with open(DATA, 'r') as dataset:
        for line in dataset.readlines():
            X.append([int(x) for x in line.split(' ')[:-1]])
            Y.append(ord(line.strip()[-1]) - ord('A'))

    # print(X[:10])

    clf = svm.SVC()
    ret = clf.fit(X, Y)
    print(ret)

    print(clf.predict([[9,12,50,0,8,9,3,2,2,2,2,2,2,1,8,9,4,6,6,6,6,6,7,6,3,0,0,0,0]]))


if __name__ == '__main__':
    main()