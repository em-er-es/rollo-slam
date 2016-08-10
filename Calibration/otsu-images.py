#!/usr/env python
import numpy as np
import cv2
import glob
import os

if not(os.path.isdir('otsu')):
	os.mkdir('otsu')

for Image in glob.glob('frame*'):
    print('Otsu filtering: ' + Image)
    tmpimage = cv2.imread(Image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    tmpimage = (tmpimage - tmpimage.min()) * 255 / (tmpimage.max() - tmpimage.min())
    tmpimage = cv2.GaussianBlur(tmpimage, (5, 5), 0) #Blur input image
    returnVoid, tmpimage = cv2.threshold(tmpimage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Otsu filter
    cv2.imwrite('otsu/' + Image, tmpimage)

print('Done')
