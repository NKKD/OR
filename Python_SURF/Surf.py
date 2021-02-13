import cv2
import numpy as np
import matplotlib.pyplot as plt
import math



cap = cv2.VideoCapture(0)

ret, frame = cap.read()

MIN_MATCH_COUNT = 10

img1 = cv2.imread('arduino.jpg', 0)  # Target Object

img2 = frame  # Scene Image

# Initiate Surf detector
plt.imshow(img3), plt.show()
