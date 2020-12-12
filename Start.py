import numpy as np
import cv2
import os
import pickle
import glob
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed
from moviepy.editor import VideoFileClip
from IPython.display import HTML
import matplotlib.image as mpimg
from collections import deque

def show_input_and_output_images(input_image, output_image):

    # Visualize input vs. pipeline img
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    fig.subplots_adjust(hspace=.2, wspace=.05)

    ax1.imshow(input_image)
    ax1.set_title('Input Image', fontsize=30)

    ax2.imshow(output_image)
    ax2.set_title('Output image', fontsize=30)

    plt.show()

# Camera calibration #

# Read in and make a list of calibration images
images = glob.glob('./camera_cal/calibration*.jpg')

# Arrays to store object points and image points from all the images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# prepare object points
nx = 9  # number of inside corners in x
ny = 6  # number of inside corners in y
objp = np.zeros((nx * ny, 3), np.float32)
objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

for fname in images:
    # read in each image
    img = cv2.imread(fname)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

    # If corners are found, add object points, image points
    if ret == True:
        imgpoints.append(corners)
        objpoints.append(objp)

        # draw and display the corners
        img_chessb = np.copy(img)
        img_chessb = cv2.drawChessboardCorners(img_chessb, (nx, ny), corners, ret)

        # show_input_and_output_images(img, img_chessb)
        # plt.show()

        # save the images
        # mpimg.imsave('./output_images/' + fname.replace("./camera_cal\\", ""), img_chessb)

# Distortion correction
test_image = cv2.imread('./camera_cal/calibration1.jpg')
axs_titles = ['Original', 'Undistorted']
# Camera calibration, given object points, image points, and the shape of the grayscale image:
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, test_image.shape[0:2], None, None)
# If grayscale image:
# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# Undistorting the test image:
undist = cv2.undistort(test_image, mtx, dist, None, mtx)
#show_input_and_output_images(test_image, undist)


