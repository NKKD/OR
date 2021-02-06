# -*- coding: utf-8 -*-
'''
Feature matching and Homography find objects:
 1. Mix feature matching and calib3d modules to find objects in complex images.
 2. Match and findHomography features from the calib3d module
 3. You can use cv2.findHomography(). If it finds a set of points in these two images, it will find each transformation of the object.
 4. Then use cv2.perspectTransform() to find the object. It needs at least four correct points to find the conversion.
 5. There may be a loss error when matching.
 Chestnuts:
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 3

img1 = cv2.imread('image_1.JPG', 0)  # Query picture
img2 = cv2.imread('image_2.JPG', 0)  # training picture

# Initialize SIFT detector
sift = cv2.xfeatures2d.SURF_create()

# Use SIFT to find key points and descriptors
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

'''
 Now we set a condition that at least 10 matches (defined by MIN_MATCH_COUNT) will be there to find the object.
   Otherwise, just display a message stating that there are not enough matches.
 If enough matches are found, we will extract the positions of the matching key points in the two images.
 They look for this transformation. Once we get this 3x3 transformation matrix,
 We use it to convert the corner of queryImage to the corresponding point in trainImage. Then we draw it.
'''
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h, w = img2.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    img1 = cv2.polylines(img1, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

else:
    print("Not enough matches are found", (len(good), MIN_MATCH_COUNT))
    matchesMask = None

# Finally draw the inner point (if the object is successfully found) or match the key point (if it fails)

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=None,
                   matchesMask=matchesMask,
                   flags=2)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

plt.imshow(img3, 'gray'), plt.show()