# -*- coding=utf8 -*-
## process the images from `raw/` into single letters, save them in `processed/`
from PIL import Image
from os import walk
from rawimg import randomName

RAW_PATH = 'raw/'
TEMP_PATH = 'monochrome/'
TARGET_PATH = 'processed/'
THRESHOLD = 150 # gray pixel threshold
# SURROUNDING = [(x, y) for y in [-1,0,1] for x in [-1,0,1]]
SURROUNDING = [(0,1), (0,-1), (-1,0), (1,0), (0,0)] # define the isolated points


def rotate(img, angle):
    width, height = img.size
    background = Image.new('L', (width+100, height+100), 255)
    # put it onto a large white background,
    # in order to avoid black rim after rotation
    background.paste(img, (50, 50))
    background = background.rotate(angle)
    background = background.crop((50, 50, 50+width, 50+height))
    return background


# convert image object to binarization image.
def toBin(img):
    # crop first
    width, height = img.size
    gray = img.convert('L') # to gray
    pix = gray.load()
    # remove the rim
    for x in range(width):
        pix[x, 0] = pix[x, height-1] = 255
    for y in range(height):
        pix[0, y] = pix[width-1, y] = 255

    # binarization
    for y in range(height):
        for x in range(width):
            pix[x, y] = 255 if pix[x, y] > THRESHOLD else 0

    # remove isolated points
    isolated = []
    for y in range(1, height-1):
        for x in range(1, width-1):
            if pix[x,y] == 0 and sum([pix[x+ox, y+oy] == 0 for (ox, oy) in SURROUNDING]) == 1:
                isolated.append((x, y))
    for (x,y) in isolated:
        pix[x, y] = 255

    # remove horizontal noise
    for y in range(height):
        s = sum([pix[x, y]==0 for x in range(width)])
        if s > 0 and s < 5:
            for x in range(width):
                pix[x, y] = 255

    # rotation makes the letter upright
    gray = rotate(gray, 7)
    pix = gray.load() # reload pixels

    # remove vertical connection between two letters
    for x in range(width):
        s = sum([pix[x, y]==0 for y in range(height)])
        if s > 0 and s < 2:
            for y in range(height):
                pix[x, y] = 255

    return gray

# crop a image to four letter images
def cropLetters(img):
    MAXIMUN_SIZE = 13 # max width/height is 13px
    # find vertical lines
    width, height = img.size

    ### (delete) we don't find the gaps between letter, we decide!
    # gaps = [8+i*MAXIMUN_SIZE for i in range(4)]
    #### fine, let's find the gaps
    pix = img.load()
    gaps = [] # contain four letters' start position on width axes
    onLetter = False
    for x in range(width):
        s = sum([pix[x, y]==0 for y in range(height)])
        # if (s != 0 and onLetter == False) or (len(gaps) and x-gaps[-1] > MAXIMUN_SIZE):
        if (s != 0 and onLetter == False):
            gaps.append(x)
            onLetter = True
        elif s==0 and onLetter == True and x-gaps[-1] >= MAXIMUN_SIZE:
            onLetter = False
    
    if len(gaps)<4:
        return False, gaps
    
    letters = []
    # crop to four letters
    for l in gaps[:4]:
        # 13 is the max width of one letter
        letter = img.crop((l, 0, l+MAXIMUN_SIZE, height))
        lpix = letter.load()
        # scan from down-to-up, deal with 'J' and 'I'
        for y in range(height)[::-1]:
            s = sum([lpix[x, y]==0 for x in range(MAXIMUN_SIZE)]) # [0, 13), the width
            if s!=0:
                # 13 is the max height of one letter, interesting :)
                if y-MAXIMUN_SIZE+1 < 0:
                    letters.append(letter.crop((0, 0, MAXIMUN_SIZE, MAXIMUN_SIZE)))
                else:
                    letters.append(letter.crop((0, y-MAXIMUN_SIZE+1, MAXIMUN_SIZE, y+1)))
                break

    return True, letters


def main():
    f = []
    for (dirpath, dirnames, filenames) in walk(RAW_PATH):
        f.extend(filenames)
        break

    # using len() has better controllability
    err_count = 0
    for i in range(len(f)):
        img = Image.open(RAW_PATH + f[i])
        bimg = toBin(img) # convert to `1` mode
        # bimg.save(TEMP_PATH + f[i], 'JPEG') # just for testing toBin()
        success, letters = cropLetters(bimg)
        
        if success:
            for l in letters:
                l.save(TARGET_PATH + randomName(9) + '.jpg', 'JPEG')
        else:
            err_count+=1
            # print('Error crop: {name}, {lines}'.format(name=f[i], lines=str(letters)))

    print('Error:', err_count)


if __name__ == '__main__':
    main()