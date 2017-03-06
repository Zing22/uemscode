# -*- coding=utf-8 -*-
## input: images
## output: their features(string), letter's width, height, pixels number, and pixels number on each row and column.

from PIL import Image
from os import walk
import string

DIR = 'train/'
FEATURE_PATH = 'feature/'


def toFeature(img):
    pix = img.convert('1').load()
    width, height = img.size
    rows, cols = [], []
    for x in range(width):
        cols.append(str(sum([pix[x, y]==0 for y in range(height)])))
    for y in range(height):
        rows.append(str(sum([pix[x, y]==0 for x in range(width)])))

    w = len(''.join(['1' if x!='0' else '0' for x in cols]).strip('0'))
    h = len(''.join(['1' if x!='0' else '0' for x in rows]).strip('0'))
    total = sum([sum([pix[x, y]==0 for y in range(height)]) for x in range(width)])

    return '{width} {height} {pixels} {rows} {cols}'.format(width=w, height=h, 
        pixels=total, rows=' '.join(rows), cols=' '.join(cols))


def main():
    all_data = ""
    for path in string.ascii_uppercase:
        f = []
        for (dirpath, dirnames, filenames) in walk(DIR+path+'/'):
            f.extend(filenames)
            break

        data = ""
        for file in filenames:
            img = Image.open(DIR+path+'/'+file)
            fea = toFeature(img)
            data += fea + ' ' + path + '\n'
        with open(FEATURE_PATH + path + '.txt', 'w') as d:
            d.writelines(data)

        all_data += data

    with open(FEATURE_PATH + 'all.txt', 'w') as ad:
        ad.writelines(all_data)


if __name__ == '__main__':
    main()