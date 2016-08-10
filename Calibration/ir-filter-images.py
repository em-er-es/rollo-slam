#!/usr/env python
import numpy as np
import cv2
import glob
import os

if not(os.path.isdir('ir')):
    os.mkdir('ir')

for Image in glob.glob('frame*'):
    print('Infrared images preprocessing and filtering: ' + Image)
# Custom kernels
#    kernel = np.array([[0, 1, 0], [1, 4, 1], [0, 1, 0]], np.uint8)
#    kernel = np.array([[0, 0, 1, 0, 0],
#                       [0, 0, 2, 0, 0],
#                       [1, 2, 4, 2, 1],
#                       [0, 0, 2, 0, 0],
#                       [0, 0, 1, 0, 0]],
#                       np.uint8)
    tmpimage = cv2.imread(Image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    scalef = 2
    osx, osy = tmpimage.shape[1], tmpimage.shape[0]
    nsx, nsy = osx * scalef, osy * scalef
    tmpimage = cv2.resize(tmpimage, (nsx, nsy))
#    tmpimageA = (tmpimage - tmpimage.min()) * 255 / (tmpimage.max() - tmpimage.min())
#    tmpimageB = cv2.morphologyEx(tmpimage, cv2.MORPH_GRADIENT, kernel)
    tmpimageE = cv2.Canny(tmpimage, 200, 220)
#    imagesum = tmpimage + tmpimageA + tmpimageB + tmpimageC + tmpimageD + tmpimageE
    kernel = np.ones((3, 3), np.uint8)

#Blur input image
#    tmpimageD = cv2.GaussianBlur(tmpimageC, (5, 5), 0)
#    tmpimageD = cv2.medianBlur((3 * tmpimage - tmpimageB + 2 * tmpimageE) / 3, 3)
    tmpimageD = cv2.medianBlur(tmpimage, 3)
    #~ tmpimageD = cv2.medianBlur(tmpimageD, 7)
#    tmpimageE = cv2.morphologyEx(tmpimageD, cv2.MORPH_CLOSE, kernel)
    #~ returnVoid, tmpimage = cv2.threshold(tmpimage + tmpimage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Otsu filter
    tmpimageC = cv2.morphologyEx(tmpimageD, cv2.MORPH_CLOSE, kernel)
    tmpimage = cv2.GaussianBlur(tmpimageC + tmpimageE, (11, 11), 0) #Blur input image
    returnVoid, tmpimage = cv2.threshold(tmpimage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Otsu filter
#    returnVoid, tmpimageB = cv2.threshold(tmpimage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Otsu filter
#    tmpimage = cv2.Canny(img, 100, 200)
#    (thresh, tmpimage) = cv2.threshold(tmpimage, 2, 255, cv2.THRESH_BINARY)
#    tmpimage = ((tmpimageA + tmpimageB + tmpimageC) - (tmpimageA.min() + tmpimageB.min() + tmpimageC.min()) * 255 / ((tmpimageA.max() + tmpimageB.max() + tmpimageC.max()) - (tmpimageA.min() + tmpimageB.min() + tmpimageC.min())))
#   tmpimage = (tmpimage + tmpimageA) / 2

    tmpimage = cv2.resize(tmpimage, (osx, osy))

    cv2.imwrite('ir/' + Image, tmpimage)

print('Done')
