# -*- coding=utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.externals import joblib

TRAIN_DATA = 'feature/all.txt'
TEST_DATA = 'feature/test.txt'
SAVE_TO = 'model.pkl'

def readDataset(filepath):
    X, Y = [], []
    # read data set
    with open(filepath, 'r') as dataset:
        for line in dataset.readlines():
            X.append([int(x) for x in line.split(' ')[:-1]])
            Y.append(ord(line.strip()[-1]) - ord('A'))

    return X, Y


def normal_test():
    err = 0
    X, y = readDataset(TEST_DATA)
    for (r, ans) in zip(clf.predict(X), y):
        if r != ans:
            err += 1

    print('Correct rate: {rate}%'.format(rate = ((len(y)-err)*100.0/len(y) )))


def main():
    global clf
    ### training
    X, y = readDataset(TRAIN_DATA)
    # print(X[:10])
    clf = svm.SVC()
    ret = clf.fit(X, y)
    print(ret)
    joblib.dump(clf, SAVE_TO)

    ### testing
    normal_test()


if __name__ == '__main__':
    main()