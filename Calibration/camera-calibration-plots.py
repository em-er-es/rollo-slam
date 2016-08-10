# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:31:53 2015

@author: Rabbia Asghar
@author: Ernest Skrzypczyk
"""
#Import of dependencies
from copy import copy
import cv2
from matplotlib import pyplot as plt
import matplotlib.patheffects as pathfx
import numpy as np
import os
from pylab import meshgrid

#Default settings
try:
    generatePlots
except NameError:
    print('Not generating plots')
    generatePlots = 1
else:
    print('Generating plots')
#    generatePlots = 1
invertAxes = 1
skipRC3 = 1
contourLevels = 6

#Predefined settings
if __name__ == '__main__':
    radialCoefficients = np.array([0.2402, -0.6861, 0])
    tangentialCoefficients = np.array([-0.0015, 0.0003])
    principalPoint = [316.7, 238.5]
    focalLength = [520.9, 521.0]
    #Camera resolution
    cameraResolution = tuple((640,480))

principalPoint = [cameraResolution[0] / 2, cameraResolution[1] / 2] #Computation of image center / principal points (sensor)
opticalCenterPoint = [cameraResolution[0] / 2, cameraResolution[1] / 2] #Computation of optical center (lense)

if skipRC3:
    radialCoefficients[2] = 0

markerScale = np.sqrt(cameraResolution[0]**2 + cameraResolution[1]**2) / ((cameraResolution[0] + cameraResolution[1]) / 10) #Scaling of optical center point marker
d = 64; dq = 1 #Point grid resolution d and computation step dq
#x, y = meshgrid(np.arange(-cameraResolution[0]/2, cameraResolution[0]/2, d), np.arange(-cameraResolution[1]/2, cameraResolution[1]/2, d))
x, y = meshgrid(np.arange(0, cameraResolution[0], d), np.arange(0, cameraResolution[1], d))
r = np.zeros((np.size(x,0), np.size(x,1)))
xR, yR, zR = copy(r), copy(r), copy(r)
xT, yT, zT = copy(r), copy(r), copy(r)
xC, yC, zC = copy(r), copy(r), copy(r)
uC, vC, rC = copy(r), copy(r), copy(r)
fC, sCX, sCY = 1, 1, 1
rCx, rCy = cameraResolution[1] / d / 2, cameraResolution[0] / d / 2
for i in np.arange(0, np.size(x, 0), dq):
    for j in np.arange(0, np.size(y, 1), dq):
#        print(i, j)
        r[i][j] = float(np.sqrt(np.abs(rCx - i)**2 + np.abs(rCy - j)**2)) #Radial
        #Radial distortion
        xR[i][j] = float(x[i][j] * (1 + radialCoefficients[0] * r[i][j]**2 + radialCoefficients[1] * r[i][j]**4 + radialCoefficients[2] * r[i][j]**6))
        yR[i][j] = float(y[i][j] * (1 + radialCoefficients[0] * r[i][j]**2 + radialCoefficients[1] * r[i][j]**4 + radialCoefficients[2] * r[i][j]**6))
        zR[i][j] = float(np.sqrt(np.abs(xR[i][j])**2 + np.abs(yR[i][j])**2))
        #Tangential distortion
        xT[i][j] = float(x[i][j] + (2 * tangentialCoefficients[0] * y[i][j] + tangentialCoefficients[1] * (r[i][j]**2 + 2 * x[i][j]**2)))
        yT[i][j] = float(y[i][j] + (2 * tangentialCoefficients[1] * x[i][j] + tangentialCoefficients[0] * (r[i][j]**2 + 2 * y[i][j]**2)))
        zT[i][j] = float(np.sqrt(np.abs(xT[i][j])**2 + np.abs(yT[i][j])**2))
        #Distortion model
        uC[i][j] = float((x[i][j] - opticalCenterPoint[0]) / (fC / sCX))
        vC[i][j] = float((y[i][j] - opticalCenterPoint[1]) / (fC / sCY))
#        uC[i][j] = float((x[i][j] - principalPoint[0]) / (fC / sCX))
#        vC[i][j] = float((y[i][j] - principalPoint[1]) / (fC / sCY))
        rC[i][j] = float(np.sqrt(np.abs(uC[i][j])**2 + np.abs(vC[i][j])**2))
        xC[i][j] = float((x[i][j] - opticalCenterPoint[0]) * (1 + radialCoefficients[0] * rC[i][j]**2 + radialCoefficients[1] * rC[i][j]**4 + radialCoefficients[2] * rC[i][j]**6) + 2 * tangentialCoefficients[0] * uC[i][j] * vC[i][j] + tangentialCoefficients[1] * (rC[i][j]**2 + 2 * uC[i][j]**2))
        yC[i][j] = float((y[i][j] - opticalCenterPoint[1]) * (1 + radialCoefficients[0] * rC[i][j]**2 + radialCoefficients[1] * rC[i][j]**4 + radialCoefficients[2] * rC[i][j]**6) + 2 * tangentialCoefficients[1] * uC[i][j] * vC[i][j] + tangentialCoefficients[0] * (rC[i][j]**2 + 2 * vC[i][j]**2))
#        xC[i][j] = float((x[i][j] - principalPoint[0]) * (1 + radialCoefficients[0] * rC[i][j]**2 + radialCoefficients[1] * rC[i][j]**4 + radialCoefficients[2] * rC[i][j]**6) + 2 * tangentialCoefficients[0] * uC[i][j] * vC[i][j] + tangentialCoefficients[1] * (rC[i][j]**2 + 2 * uC[i][j]**2))
#        yC[i][j] = float((y[i][j] - principalPoint[1]) * (1 + radialCoefficients[0] * rC[i][j]**2 + radialCoefficients[1] * rC[i][j]**4 + radialCoefficients[2] * rC[i][j]**6) + 2 * tangentialCoefficients[1] * uC[i][j] * vC[i][j] + tangentialCoefficients[0] * (rC[i][j]**2 + 2 * vC[i][j]**2))
        zC[i][j] = float(np.sqrt(np.abs(xC[i][j])**2 + np.abs(yC[i][j])**2))

radialDistortionsFigure = plt.figure(1)
if generatePlots == 1:
    radialDistortionsPlot = plt.quiver(x, y, xR, yR, r)
    radialDistortionsPlotContour = plt.contour(x, y, zR)
    plt.plot(principalPoint[0], principalPoint[1], color='#ff0000', marker='o')
    plt.plot(opticalCenterPoint[0], opticalCenterPoint[1], color='#000000', marker='x', markersize=markerScale)
elif generatePlots == 2:
    radialDistortionsPlot = plt.quiver(x, y, xR, yR, cmap='gray')
    radialDistortionsPlotContour = plt.contour(x, y, zR, cmap='gray')
    plt.plot(principalPoint[0], principalPoint[1], color='#a0a0a0', marker='o')
    plt.plot(opticalCenterPoint[0], opticalCenterPoint[1], color='#000000', marker='x', markersize=markerScale)
#circlePrincipalPointRadial = plt.Circle((principalPoint[0],principalPoint[1]),radius=32,color='b',fill=False)
#radialDistortionsFigure.gca().add_artist(circlePrincipalPointRadial)
#plt.matplotlib.markers.MarkerStyle(marker=u'o', fillstyle=u'none')
#plt.matplotlib.markers.MarkerStyle(marker='$\bigcirc$')
plt.clabel(radialDistortionsPlotContour, inline = 1, fontsize = 8)
if invertAxes:
    plt.axis([0, cameraResolution[0], 0, cameraResolution[1]])
else:
    plt.axis([0, cameraResolution[0], cameraResolution[1], 0])
#    plt.grid(1,'both')
plt.show()
radialDistortionsFigure.savefig('radialDistortionsFigure.png')

tangentialDistortionsFigure = plt.figure(2)
if generatePlots == 1:
    tangentialDistortionsPlot = plt.quiver(x, y, xT, yT, r)
    plt.plot(principalPoint[0], principalPoint[1], color='#ff0000', marker='o')
    plt.plot(opticalCenterPoint[0], opticalCenterPoint[1], color='#000000', marker='x', markersize=markerScale)
    tangentialDistortionsPlotContour = plt.contour(x, y, zT)
elif generatePlots == 2:
    tangentialDistortionsPlot = plt.quiver(x, y, xT, yT, cmap='gray')
    plt.plot(principalPoint[0], principalPoint[1], color='#a0a0a0', marker='o')
    plt.plot(opticalCenterPoint[0], opticalCenterPoint[1], color='#000000', marker='x', markersize=markerScale)
    tangentialDistortionsPlotContour = plt.contour(x, y, zT, cmap='gray')
plt.clabel(tangentialDistortionsPlotContour, inline = 1, fontsize = 8)
if invertAxes:
    plt.axis([0, cameraResolution[0], 0, cameraResolution[1]])
else:
    plt.axis([0, cameraResolution[0], cameraResolution[1], 0])
plt.show()
tangentialDistortionsFigure.savefig('tangentialDistortionsFigkure.png')

completeDistortionsFigure = plt.figure(3)
if generatePlots == 1:
    completeDistortionsPlot = plt.quiver(x, y, xC, yC, r)
    completeDistortionsPlotContour = plt.contour(x, y, zC)
#    completeDistortionsPlotContour = plt.contour(x, y, zC, contourLevels, pathfx=[pathfx.SimpleLineShadow(), pathfx.Normal()])
    plt.plot(principalPoint[0], principalPoint[1], color='#ff0000', marker='o')
    plt.plot(opticalCenterPoint[0], opticalCenterPoint[1], color='#000000', marker='x', markersize=markerScale)
elif generatePlots == 2:
    completeDistortionsPlot = plt.quiver(x, y, xC, yC, cmap='gray')
    completeDistortionsPlotContour = plt.contour(x, y, zC, cmap='gray')
    plt.plot(principalPoint[0], principalPoint[1], color='#a0a0a0', marker='o')
    plt.plot(opticalCenterPoint[0], opticalCenterPoint[1], color='#000000', marker='x', markersize=markerScale)
plt.clabel(completeDistortionsPlotContour, inline = 1, fontsize = 8)
if invertAxes:
    plt.axis([0, cameraResolution[0], 0, cameraResolution[1]])
else:
    plt.axis([0, cameraResolution[0], cameraResolution[1], 0])
plt.show()
completeDistortionsFigure.savefig('completeDistortionsFigure.png')

plt.close('all')
