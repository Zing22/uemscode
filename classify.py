# -*- coding=utf8 -*-
## classify letters one by one
from rawimg import randomName
import string

#### source image directory
DIR = 'processed/'
#### decide the destination
# DIST_DIR = 'train/'
DIST_DIR = 'test/'

from os import walk
from shutil import move

def rename(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break

    for file in filenames:
        move(path+file, path+randomName(9)+'.jpg')


def main():
    f = []
    for (dirpath, dirnames, filenames) in walk(DIR):
        f.extend(filenames)
        break

    # for file in filenames:
    #     move(DIR+file, DIR+randomName(9)+'.jpg')

    for file in filenames[::-1]:
        dist = input(file+':')
        move(DIR+file, DIST_DIR+dist)

    # for x in string.ascii_uppercase:
    #     rename(DIST_DIR + x + '/')

if __name__ == '__main__':
    main()