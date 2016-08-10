#!/bin/env python2
# -*- coding: utf-8 -*-
### Authors: Rabbia Asghar, Ernest Skrzypczyk; Date: 2016
#%% Camera calibration with Python using OpenCV
from __future__ import print_function #Python2
#Import of dependencies
from copy import copy
import cv2 #OpenCV2
from matplotlib import pyplot as plt #Matplotlib
import numpy as np #Numpy
import os #OS
import logging
#from pylab import meshgrid #Import biblioteki

#%% Check if run as a script or imported as a library
if __name__ == '__main__':
    import argparse #Import library for argument parsing
    from glob import glob #Import library for globbing
    processedCounter, errorCounter, imagesCounter = 0, 0, 0 #Initialize counters

    #%% Interprate command line arguments
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__))
    parser = argparse.ArgumentParser(description='Calculate camera calibration matrix and additional parameters based on a provided sequence of images with a chessboard calibration pattern.')
    parser.add_argument('-1', '-p', '--pause', dest='pause', action='store_true', help='Pause between processed images') #Option for pause between processed images
    parser.add_argument('-bt', '--binary-threshold', dest='binaryThreshold', type=int, default=127, help='Threshold for binary filtering', metavar='BINARYTHRESHOLD <0-255><!127>') #Definition threshold for binary filtering and default value
    parser.add_argument('-br', '--blur-range', dest='blurRange', type=int, default=5, help='Range for blur filter during Otsu filtering', metavar='BLURRANGE <in pixel><!5>') #Definition range for Gaussian blur filtering and default value
    parser.add_argument('-cr', '--camera-resolution', dest='cameraResolution', type=int, nargs=2, default=(1280, 1024), help='Pixel resolution of the camera used', metavar='CAMERARESOLUTION <X resolution, Y resolution><!1280, 1024>') #Definition camera resolution and default value
    parser.add_argument('-l', '--log', dest='logFile', type=str, help='Write a log file with results', metavar='LOGFILENAME') #Definition log filename
    parser.add_argument('-ps', '--pattern-size', dest='patternSize', type=int, nargs=2, default=(9, 6), help='Number of corners in the outter pattern block', metavar='PATTERNSIZE <x, y><!9, 6>') #Definition squares pattern grid and default value
    parser.add_argument('-si', '--show-images', dest='showImages', action='store_true', help='Show images') #Option for displaying images
    parser.add_argument('-s', '--save-images', dest='saveImages', action='store_true', help='Save images') #Option for saving processed images
    parser.add_argument('-ss', '--square-size', dest='squareSize', type=int, default=25.0, help='Size of squares in millimeters', metavar='SQUARESIZE <in mm><!25.0>') #Definition of square size in mm and default value
    parser.add_argument('imagemask', nargs='*', default='*.jpg', help='Images globbing mask', metavar='(IMAGEFILES, FILEMASK)') #Globbing mask
    parser.add_argument('-gp', '--generate-plots', dest='generatePlots', type=int, choices=[0, 1, 2], default=1, help='Generate and/or colorize distortion plots: 0 - disable, 1 - color, 2 - grayscale') #Option for generating [color] plots
    parser.add_argument('-ia', '--invert-axes', dest='invertAxes', type=bool, help='Invert axes on distortion plots') #Option for inverting axes of generated plots
    parser.add_argument('-sp', '--save-path', dest='savePath', type=str, default='/tmp', help='Definitions path for generated images, implies save images option', metavar='<SAVEPATH><!/tmp>') #Definition of save path for processed images
    parser.add_argument('-sr3', '--skip-rc3', dest='skipRC3', action='store_true', help='Ignore the third radial distortion parameter during calculations') #Option for skipping 3rd radial distortion parameter
    args = parser.parse_args() #Parse arguments and file mask from command line
    #Configuration from command line
    binaryThreshold = int(args.binaryThreshold)
    blurRange = int(args.blurRange)
    cameraResolution = tuple(args.cameraResolution)
    imageMask = (args.imagemask)
    patternSize = tuple(args.patternSize)
    pause = bool(args.pause)
    saveImages = bool(args.saveImages)
    savePath = str(args.savePath)
    showImages = bool(args.showImages)
    logFile = str(args.logFile)
    squareSizes = np.array([25.0, 25.0 * 0.75, 25.0 * 1.25, 14.0, 12.0, 10.0])
    squareSize = float(args.squareSize)
    if savePath != '/tmp': #Save path configuration
        saveImages = True
    if logFile != None: #Logging configuration
        if '/' not in logFile:
            logFile = savePath + '/' + logFile
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        logger = logging.getLogger()
        logger.addHandler(logging.FileHandler(logFile, 'a'))
        print = logger.info
    if '*' not in imageMask:
        imageNames = imageMask #File mask
    else:
        imageNames = glob(imageMask) #Parse file mask
    #Computation and plot options
    skipRC3 = bool(args.skipRC3) #Calculation simplifying option
    generatePlots = int(args.generatePlots) #Option for generating [color] plots
    invertAxes = bool(args.invertAxes) #Option for generating plots with inverted axes

    #Debug
    #print(patternSize)
    #print(cameraResolution)

    #%% Loading files
    for imageFile in imageNames:
        if not os.path.isfile(imageFile): #Check if provided path is a file
            print('Loading image failed. Provided argument is not a file or does not exist: ' + imageFile)
            continue #Continue iteration
        print('Processing image: ' + imageFile)
        imagesCounter += 1
        image = cv2.imread(imageFile, cv2.IMREAD_GRAYSCALE) #Load image in grayscale
        imageColor = cv2.imread(imageFile, cv2.IMREAD_COLOR) #Load image in RGB
        returnVoid, imageBinary = cv2.threshold(image, binaryThreshold, 255, cv2.THRESH_BINARY) #Binarization of input image
        imageBlurred = cv2.GaussianBlur(image, (blurRange, blurRange), 0) #Blur input image
        returnVoid, imageOtsu = cv2.threshold(imageBlurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Otsu filter

    #Preliminary calculations
        patternPoints = np.zeros((np.prod(patternSize), 3), np.float32) #Initialization of pattern grid
        patternPoints[:, :2] = np.indices(patternSize).T.reshape(-1, 2) #Tranformation of pattern grid into uniform coordinates
        patternPoints *= squareSize #Scaling of grid coordinates
        objectPoints, imagePoints = [], [] #Initialization of point list in 3D and 2D
        objectPointsBinary, imagePointsBinary = [], [] #Initialization of point list in 3D and 2D for binary thresholding
        objectPointsOtsu, imagePointsOtsu = [], [] #Initialization of point list in 3D and 2D for Otsu filtering
        height, width = image.shape[0], image.shape[1] #Set image resolution
#        opticalCenterPoint = [cameraResolution[0] / 2, cameraResolution[1] / 2] #Optical center point (lens)
        principalPoint = [cameraResolution[0] / 2, cameraResolution[1] / 2] #Principal point / Image center (sensor)

    #%% Image processing
        #%% Default method
        patternWasFound, corners = cv2.findChessboardCorners(image, patternSize, flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE) #Computation of chessboard corners with respect to its shape and size
        if patternWasFound:
            tolerance = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1) #Tolerance/precision for further computations
            cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), tolerance)
#            imageWithCorners = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) #Conversion into RGB
            imageWithCorners = copy(imageColor) #Set image copy for further processing
            cv2.drawChessboardCorners(imageWithCorners, patternSize, corners, patternWasFound) #Impose recognized chessboard corners
            imagePath, imageFilename = os.path.split(imageFile) #Seperate path and filename
            imageName, imageExt = os.path.splitext(imageFilename) #Seperate file name and file extention
            if saveImages:
                cv2.imwrite(savePath + '/wcd-%s.png' % imageName, imageWithCorners) #Save processed files with imposed recognized corners
#                print(savePath + '/wcd-%s.png' % imageName)
        else:
            print('Pattern not recognized in file: ' + imageFile)
            errorCounter += 1
            #~ if showImages:
                #~ plt.title(os.path.split(imageFile)) #Set titles
                #~ plt.subplot(1, 2, 1); plt.imshow(image, 'gray') #Display images in grayscale
                #~ plt.xticks([]); plt.yticks([]) #Remove axes and ticks
                #~ plt.subplot(1, 2, 2); plt.imshow(image, 'gray') #Display images in grayscale
                #~ plt.xticks([]); plt.yticks([]) #Remove axes and ticks
                #~ plt.show()
            continue #Continue iteration
        imagePoints.append(corners.reshape(-1, 2))
        objectPoints.append(patternPoints) #Add computed values to object points matrix
        rootMeanSquare, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors = cv2.calibrateCamera(objectPoints, imagePoints, (width, height), None, None) #Computation of camera distortion matrix and distortion coefficients for default method
        focalLength = [cameraMatrix[0][0], cameraMatrix[1][1]]
        opticalCenterPoint = [cameraMatrix[0][2], cameraMatrix[1][2]]
#        principalPoint = [cameraMatrix[0][2], cameraMatrix[1][2]]
        skew = [cameraMatrix[0][1]]
        radialCoefficients = np.array([distortionCoefficients[0][0], distortionCoefficients[0][1], distortionCoefficients[0][4]])
        tangentialCoefficients = np.array([distortionCoefficients[0][2], distortionCoefficients[0][3]])

        #%% Binary filtering
        patternWasFound, corners = None, None #Clear variables
        patternWasFound, corners = cv2.findChessboardCorners(imageBinary, patternSize)
        if patternWasFound:
#            imageWithCornersBinary = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            imageWithCornersBinary = copy(image)
            cv2.cornerSubPix(imageWithCornersBinary, corners, (5, 5), (-1, -1), tolerance)
            imageWithCornersBinary = copy(imageColor)
            cv2.drawChessboardCorners(imageWithCornersBinary, patternSize, corners, patternWasFound)
            imagePointsBinary.append(corners.reshape(-1, 2))
            objectPointsBinary.append(patternPoints) #Add computed values to object points matrix
            rootMeanSquareBinary, cameraMatrixBinary, distortionCoefficientsBinary, rotationVectorsBinary, translationVectorsBinary = cv2.calibrateCamera(objectPointsBinary, imagePointsBinary, (width, height), None, None) #Computation of camera distortion matrix and distortion coefficients for binary filter
            focalLengthBinary = [cameraMatrixBinary[0][0], cameraMatrixBinary[1][1]]
            opticalCenterPointBinary = [cameraMatrix[0][2], cameraMatrix[1][2]]
#            principalPointBinary = [cameraMatrix[0][2], cameraMatrix[1][2]]
            skewBinary = [cameraMatrix[0][1]]
            radialCoefficientsBinary = np.array([distortionCoefficientsBinary[0][0], distortionCoefficientsBinary[0][1], distortionCoefficientsBinary[0][4]])
            tangentialCoefficientsBinary = np.array([distortionCoefficientsBinary[0][2], distortionCoefficientsBinary[0][3]])
            if saveImages:
                cv2.imwrite(savePath + '/wcb-%s.png' % imageName, imageWithCornersBinary)

        #%% Otsu filtering
        patternWasFound, corners = None, None #Clear variables
        patternWasFound, corners = cv2.findChessboardCorners(imageOtsu, patternSize)
        imageWithCornersOtsu = copy(imageColor)
        if patternWasFound:
 #           imageWithCornersOtsu = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            cv2.cornerSubPix(imageOtsu, corners, (5, 5), (-1, -1), tolerance)
            cv2.drawChessboardCorners(imageWithCornersOtsu, patternSize, corners, patternWasFound)
            imagePointsOtsu.append(corners.reshape(-1, 2))
            objectPointsOtsu.append(patternPoints) #Add computed values to object points matrix
            rootMeanSquareOtsu, cameraMatrixOtsu, distortionCoefficientsOtsu, rotationVectorsOtsu, translationVectorsOtsu = cv2.calibrateCamera(objectPointsOtsu, imagePointsOtsu, (width, height), None, None) #Computation of camera distortion matrix and distortion coefficients for Otsu filter
            focalLengthOtsu = [cameraMatrixOtsu[0][0], cameraMatrixOtsu[1][1]]
            opticalCenterPointOtsu = [cameraMatrixOtsu[0][2], cameraMatrixOtsu[1][2]]
#            principalPointOtsu = [cameraMatrixOtsu[0][2], cameraMatrixOtsu[1][2]]
            skewOtsu = [cameraMatrixOtsu[0][1]]
            radialCoefficientsOtsu = np.array([distortionCoefficientsOtsu[0][0], distortionCoefficientsOtsu[0][1], distortionCoefficientsOtsu[0][4]])
            tangentialCoefficientsOtsu = np.array([distortionCoefficientsOtsu[0][2], distortionCoefficientsOtsu[0][3]])
            if saveImages:
                cv2.imwrite(savePath + '/wco-%s.png' % imageName, imageWithCornersOtsu)
        #%% Processing images one by one
        if pause:
            raw_input('Processed image ' + imageFile + '. Press <Enter> to continue.') #Pause processing
        #%% Show filtered images and impose recognized corners
        if showImages:
            titles = ['Original', 'Binary filter', 'Otsu filter', 'Corners', 'Binary', 'Otsu'] #Titles list
            images = [image, imageBinary, imageOtsu, imageWithCorners, imageWithCornersBinary, imageWithCornersOtsu] #Images list
            for i in xrange(6):
                plt.subplot(2, 3, i + 1); plt.imshow(images[i], 'gray') #Display images in grayscale
                plt.title(titles[i]) #Set titles
                plt.xticks([]); plt.yticks([]) #Remove axes and ticks
            plt.show()
        processedCounter += 1 #Iterations counter

    if imagesCounter == errorCounter:
        print('Processed all images without recognizing a single pattern')
        os.sys.exit(2)

    #%% Save distorted images
    for imageFile in imageNames:
        if not os.path.isfile(imageFile): #Check if provided path is a file
            print('Loading image failed. Provided argument is not a file or does not exist: ' + imageFile)
            continue 
        print('Undistorting file: ' + imageFile)
        imagePath, imageFilename = os.path.split(imageFile) #Seperate path and filename
        imageName, imageExt = os.path.splitext(imageFilename) #Seperate file name and file extention
        imageColor = cv2.imread(imageFile, cv2.IMREAD_COLOR) #Load image in RGB
        imageUndistorted, imageUndistortedBinary, imageUndistortedOtsu = copy(imageColor), copy(imageColor), copy(imageColor) #InirootMeanSquareOtsu, cameraMatrixOtsu, distortionCoefficientsOtsu, rotationVectorsOtsu, translationVectorsOtsu #Initialize variables for undistorted images
        undistortedCameraMatrix, regionOfInterest = cv2.getOptimalNewCameraMatrix(cameraMatrix, distortionCoefficients, (width, height), 0) #Computation of camera distortion matrix and region of interest coordinates
        undistortedImage = cv2.undistort(imageColor, cameraMatrix, distortionCoefficients, None, undistortedCameraMatrix)
        undistortedCameraMatrixBinary, regionOfInterestBinary = cv2.getOptimalNewCameraMatrix(cameraMatrixBinary, distortionCoefficientsBinary, (width, height), 0) #Computation of camera distortion matrix and region of interest coordinates for binary filtration
        undistortedImageBinary = cv2.undistort(imageColor, cameraMatrixBinary, distortionCoefficientsBinary, None, undistortedCameraMatrixBinary)
        undistortedCameraMatrixOtsu, regionOfInterestOtsu = cv2.getOptimalNewCameraMatrix(cameraMatrixOtsu, distortionCoefficientsOtsu, (width, height), 0) #Computation of camera distortion matrix and region of interest coordinates for Otsu filtration
        undistortedImageOtsu = cv2.undistort(imageColor, cameraMatrixOtsu, distortionCoefficientsOtsu, None, undistortedCameraMatrixOtsu)
        if saveImages: #Save undistorted images
            try:
                cv2.imwrite(savePath + '/udd-%s.png' % imageName, undistortedImage)
                cv2.imwrite(savePath + '/udb-%s.png' % imageName, undistortedImageBinary)
                cv2.imwrite(savePath + '/udo-%s.png' % imageName, undistortedImageOtsu)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                continue
    #%% Show undistorted images
        titles = ['Original', 'Binary filter', 'Otsu filter', 'Undistorted', 'Binary', 'Otsu'] #Titel list
#        images = [image, imageBinary, imageOtsu, imageUndistorted, imageUndistortedBinary, imageUndistortedOtsu] #Images list
        images = [imageColor, imageColor, imageColor, imageUndistorted, imageUndistortedBinary, imageUndistortedOtsu] #Images list
        if showImages:
            for i in xrange(6):
                plt.subplot(2, 3, i + 1); plt.imshow(images[i], 'gray') #Display images in grayscale
                plt.title(titles[i]) #Set titles
                plt.xticks([]); plt.yticks([]) #Remove axes and ticks
            plt.show()

    #%% Summary
    if processedCounter > 0:
        recognitionSuccessRate = float(processedCounter) / (processedCounter + errorCounter) * 100 #Computation of pattern recognition success rate
        delta = [opticalCenterPoint[0] - principalPoint[0], opticalCenterPoint[1] - principalPoint[1]] #Translation of lens center point with relation to sensor matrice
        #%% Display results after 'i' files
        print('\n\nSummary\nProcessed images: ' + str(processedCounter) + '\nPattern recognition failure/Read files error: ' + str(errorCounter) + '\nTotal image number: ' + str(processedCounter + errorCounter) + '\nRecognition successrate: ' + str(np.round(recognitionSuccessRate)) + '%')
        print('\nDefault method')
        print('Root mean square: %s' % rootMeanSquare)
        print('Camera matrix:\n%s' % cameraMatrix)
        print('Distortion coefficients: %s' %distortionCoefficients.ravel())
        print('Radial distortion coefficients: %s' % radialCoefficients)
        print('Tangential distortion coefficients: %s' % tangentialCoefficients)
        print('Rotation vector: %s' % rotationVectors)
        print('Translation vector: %s' % translationVectors)
        print('Focal length: f_x = %s, f_y = %s' % (focalLength[0], focalLength[1]))
        print('Principal point: P_x = %s, P_y = %s' % (principalPoint[0], principalPoint[1]))
        print('Optical center point: O_x = %s, O_y = %s' % (opticalCenterPoint[0], opticalCenterPoint[1]))
        print('Translation: Delta_x = %s, Delta_y = %s' % (delta[0], delta[1]))
        print('Skew: S = %s' % skew)

        print('\nBinary filtration')
        print('Root mean square:%s' %rootMeanSquareBinary)
        print('Camera matrix:\n%s' %cameraMatrixBinary)
        print('Distortion coefficients: %s' %distortionCoefficientsBinary.ravel())

        print('\nOtsu filtration')
        print('Root mean square: %s' %rootMeanSquareOtsu)
        print('Camera matrix:\n%s' %cameraMatrixOtsu)
        print('Distortion coefficients: %s' %distortionCoefficientsOtsu.ravel())

        results = [rootMeanSquare, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors, rootMeanSquareBinary, cameraMatrixBinary, distortionCoefficientsBinary, rotationVectorsBinary, translationVectorsBinary, rootMeanSquareOtsu, cameraMatrixOtsu, distortionCoefficientsOtsu, rotationVectorsOtsu, translationVectorsOtsu]
        print('\n\nPlots:\n')
    # %% Plots
        if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "/camera-calibration-plots.py") & generatePlots > 0:
#            execfile(os.path.dirname(os.path.realpath(__file__)) + "/camera-calibration-plots.py") #Problematic in Python3
            exec(compile(open(os.path.dirname(os.path.realpath(__file__)) + "/camera-calibration-plots.py", "rb").read(), os.path.dirname(os.path.realpath(__file__)) + "/camera-calibration-plots.py", 'exec'))
    print('Exit')
