# -*- coding=utf8 -*-
## This file download images from uems to `raw/` ##

import random, string
# if python 2: from urllib import urlretrieve
from urllib.request import urlretrieve
from time import sleep

# return a random string with N upper case leeters and digits
def randomName(N):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(N))


def main():
    count = int(input('Number of images:')) # the total count of images you need
    imgurl = 'http://uems.sysu.edu.cn/elect/login/code' # no offense
    path = './raw/'
    for x in range(count):
        urlretrieve(imgurl, path + randomName(7) + '.jpg')
        print('#', end='', flush=True)
        sleep(1.1) # for my IP's safe :)
    return

if __name__ == '__main__':
    main()