# -*- coding=utf8 -*-
## This file will process all images in 'RAW_DONE' directory into train dataset


from PIL import Image

from rawimg import randomName
from process import toBin, cropLetters
from img2feature import toFeature
from main import readAllFiles


# Presume all file in RAW_DONE were corrected, whose filenames are the same as the code.
RAW_DONE = 'raw_done/'
TARIN_DIR = 'train/'

def main():
    filenames = readAllFiles(RAW_DONE)

    for file in filenames:
        # the right code
        error_code = [x for x in file[:4]]
        answer = [x for x in file[5:9]]

        img = Image.open(RAW_DONE + file)
        bimg = toBin(img)
        # bimg.save(TEMP_DIR+ 'bimg.jpg')
        success, letters = cropLetters(bimg)
        if not success:
            print('Crop failed.')
            return

        for (letter, code, ans) in zip(letters, error_code, answer):
            if code != ans:
                save_to = TARIN_DIR + ans + '/' + randomName(9) + '.jpg'
                letter.save(save_to)
                print(save_to)

    print('Done, do img2feature and train again.')


if __name__ == '__main__':
    main()