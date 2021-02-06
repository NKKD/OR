import cv2
import numpy as np
import matplotlib.pyplot as plt


while(True):

    # load the target image
    target_image = cv2.imread("target.jpg")

    # show the target image
    cv2.imshow('target image',target_image)

    # load the scene image
    scene_image = cv2.imread("scene.jpg")

    # show the scene image
    cv2.imshow('scene image', scene_image)

    # -- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
    minHessian = 400

    detector = cv2.xfeatures2d.SURF_create(hessianThreshold=minHessian)

    keypoints1, descriptors1 = detector.detectAndCompute(target_image, None)
    keypoints2, descriptors2 = detector.detectAndCompute(scene_image, None)

    # apply SURF descriptor
    kp1,des1 = detector.detectAndCompute(target_image,None)
    kp2,des2 = detector.detectAndCompute(scene_image,None)

    # -- Step 2: Matching descriptor vectors with a FLANN based matcher
    # Since SURF is a floating-point descriptor NORM_L2 is used
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
    # -- Filter matches using the Lowe's ratio test
    ratio_thresh = 0.7
    good_matches = []
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)
    # -- Draw matches
    img_matches = np.empty((max(target_image.shape[0], scene_image.shape[0]), target_image.shape[1] + scene_image.shape[1], 3),
                           dtype=np.uint8)
    cv2.drawMatches(target_image, keypoints1, scene_image, keypoints2, good_matches, img_matches,
                   flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # -- Show detected matches
    cv2.imshow('Good Matches', img_matches)



    keyDown = cv2.waitKey(1)
    if keyDown == ord('q'):
        print('Quitting')
        break

cv2.destroyAllWindows()

