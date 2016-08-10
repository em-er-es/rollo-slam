#!/usr/env python
import numpy as np
import cv2
import glob
import os

if not(os.path.isdir('bin')):
	os.mkdir('bin')

for Image in glob.glob('frame*'):
    print('Binarizing: ' + Image)
    tmpimage = cv2.imread(Image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    tmpimage = (tmpimage - tmpimage.min()) * 255 / (tmpimage.max() - tmpimage.min())
    returnVoid, tmpimage = cv2.threshold(tmpimage, 2, 255, cv2.THRESH_BINARY)
    cv2.imwrite('bin/' + Image, tmpimage)

print('Done')
