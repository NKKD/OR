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
    detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)

    keypoints1, descriptors1 = detector.detectAndCompute(target_image, None)
    keypoints2, descriptors2 = detector.detectAndCompute(scene_image, None)

    # apply SURF descriptor
    kp1,des1 = detector.detectAndCompute(target_image,None)
    kp2,des2 = detector.detectAndCompute(scene_image,None)



    keyDown = cv2.waitKey(1)
    if keyDown == ord('q'):
        print('Quitting')
        break

cap.release()
cv2.destroyAllWindows()

