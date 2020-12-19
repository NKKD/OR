import cv2
import sys
import numpy


cap = cv2.VideoCapture(0)

#set the camera resolution to 1080p

cap.set(3,1920) # Width
cap.set(4,1080) # Height

while(True):

    ret, frame = cap.read()  # Reads next frame
    cv2.putText(frame, 'Looking for orange objects', (200, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 100, 150), (50, 255, 255))  # Looking for hues in the orange range

    # Identify controur
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        max_area = 0
        ci = ""
        # Check each Contour
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if (area > max_area):
                max_area = area
                ci = cnt
        if (ci != ""):
            # Calculate Moments
            moments = cv2.moments(ci)
            if (moments['m00'] != 0):
                cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
                cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                # print("Coordinates", cx, cy)
            # Draw Contours
            cv2.drawContours(frame, [ci], 0, (255, 0, 0), 2)



    cv2.imshow('Input',frame)

    # print('Local x-coordinate' , cx)
    # print('Local y-coordinate' , cy)

    keyDown = cv2.waitKey(1)

    if keyDown == ord('q'):
        print('Quitting')
        break


cap.release()
cv2.destroyAllWindows()