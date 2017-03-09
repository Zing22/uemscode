# -*- coding=utf-8 -*-
#### for testing steps

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.externals import joblib
from PIL import Image

from process import toBin, cropLetters
from img2feature import toFeature
from main import readAllFiles


TEMP_DIR = 'tmp/'

def test_onePic():
    path = input('Pic path:')
    img = Image.open(path)
    bimg = toBin(img)
    bimg.save(TEMP_DIR+ 'bimg.jpg')
    success, letters = cropLetters(bimg)
    if not success:
        print('Crop failed.')
        print(letters)
        return

    features = []
    for l in letters:
        features.append([int(x) for x in toFeature(l).split(' ')])
        l.save(TEMP_DIR + '%d.jpg' % len(features))

    pre = clf.predict(features)
    code = ''.join([chr(x + ord('A')) for x in pre])

    print(code)


def test_tmp_dir():
    filenames = readAllFiles(TEMP_DIR)
    for file in filenames:
        img = Image.open(TEMP_DIR + file)
        bimg = toBin(img)
        bimg.save(TEMP_DIR + 'tmp_' + file)
        success, letters = cropLetters(bimg)
        if not success:
            print('Crop failed.')
            print(letters)
            return

        features = []
        for l in letters:
            features.append([int(x) for x in toFeature(l).split(' ')])
            # l.save(TEMP_DIR + '%d.jpg' % len(features))

        pre = clf.predict(features)
        code = ''.join([chr(x + ord('A')) for x in pre])

        print(code)


SAVE_TO = 'model.pkl'
def main():
    global clf
    clf = joblib.load(SAVE_TO)
    test_onePic()
    # test_tmp_dir()


if __name__ == '__main__':
    main()