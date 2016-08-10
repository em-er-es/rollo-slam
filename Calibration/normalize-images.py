#!/usr/env python
import numpy as np
import cv2
import glob
import os

if not(os.path.isdir('norm')):
	os.mkdir('norm')

for Image in glob.glob('frame*'):
    print('Normalizing: ' + Image)
    tmpimage = cv2.imread(Image)
    cv2.imwrite('norm/' + Image, (tmpimage - tmpimage.min()) * 255 / (tmpimage.max() - tmpimage.min()))

print('Done')
