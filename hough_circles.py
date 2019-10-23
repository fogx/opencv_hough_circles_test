# import the necessary packages
from pathlib import Path

import numpy as np
import cv2 as cv
import os

dp = 1
param1 = 100
param2 = 100
mindist = 200
minR = 1
maxR = 1


def on_hough_dp_trackbar(val):
    global dp
    dp = val


def on_hough_param_1_trackbar(val):
    global param1
    param1 = val


def on_hough_param_2_trackbar(val):
    global param2
    param2 = val


def on_hough_min_dist_trackbar(val):
    global mindist
    mindist = val


def on_hough_min_r_trackbar(val):
    global minR
    global maxR
    low_V = min(maxR - 1, minR)


def on_hough_max_r_trackbar(val):
    global maxR
    global minR
    high_V = max(maxR, minR + 1)
    maxR = val


# load the image, clone it for output, and then convert it to grayscale
image_name = "hough_test.png"
path_to_image = Path.cwd() / "images"/ image_name
img = cv.imread(path_to_image.as_posix())
output = img
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.namedWindow("hough_circles")
cv.createTrackbar("dp", "hough_circles", dp, 3, on_hough_dp_trackbar)
cv.createTrackbar("param1", "hough_circles", param1, 2000, on_hough_param_1_trackbar)
cv.createTrackbar("param2", "hough_circles", param2, 2000, on_hough_param_2_trackbar)
cv.createTrackbar("mindist", "hough_circles", mindist, 2000, on_hough_min_dist_trackbar)
cv.createTrackbar("min R", "hough_circles", minR, 500, on_hough_min_r_trackbar)
cv.createTrackbar("max R", "hough_circles", maxR, 500, on_hough_max_r_trackbar)

while True:
    img_GRAY = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # img_GRAY = cv.Blur(img_GRAY, (5, 5))
    img_GRAY = cv.medianBlur(img_GRAY, 5)
    # inv_img = cv.bitwise_not(img_GRAY)
    inv_img = img_GRAY
    circles = cv.HoughCircles(inv_img, cv.HOUGH_GRADIENT, dp, mindist, param1, param2, minR, maxR)
    circles = np.uint16(np.around(circles))
    result = inv_img
    for i in circles[0, :]:
        # draw the outer circle
        cv.circle(result, (i[0], i[1]), i[2], (50, 50, 50), 2)
        # draw the center of the circle
        # cv.circle(result, (i[0], i[1]), 2, (0, 0, 255), 3)
    result_out = cv.cvtColor(inv_img, cv.COLOR_GRAY2BGR)
    result = np.vstack((img, result_out))
    cv.imshow("hough_circles", result_out)
    key = cv.waitKey(500)
    if key == ord('q') or key == 27:
        break