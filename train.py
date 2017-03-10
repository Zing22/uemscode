# -*- coding=utf8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split


TRAIN_DATA = 'feature/all.txt'
# TEST_DATA = 'feature/test.txt'
SAVE_TO = 'model.pkl'

def readDataset(filepath):
    X, Y = [], []
    # read data set
    with open(filepath, 'r') as dataset:
        for line in dataset.readlines():
            X.append([int(x) for x in line.split(' ')[:-1]])
            Y.append(ord(line.strip()[-1]) - ord('A'))

    return X, Y


def main():
    global clf
    ### training
    X, y = readDataset(TRAIN_DATA)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=2)

    clf = SVC()
    ret = clf.fit(X_train, y_train)

    yt = clf.predict(X_test)
    print("SVM:", np.sum(yt==y_test)*100.0/len(yt))

    joblib.dump(clf, SAVE_TO)
    print('SVM Model is saved.')

    clf = GradientBoostingClassifier()
    ret = clf.fit(X_train, y_train)

    yt = clf.predict(X_test)
    print("Gradient Boosting:", np.sum(yt==y_test)*100.0/len(yt))

    clf = DecisionTreeClassifier()
    ret = clf.fit(X_train, y_train)

    yt = clf.predict(X_test)
    print("Decision Tree:", np.sum(yt==y_test)*100.0/len(yt))


if __name__ == '__main__':
    main()