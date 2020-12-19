import cv2
import socket
import sys
import numpy
import time


state = 1
flag = 0
flag1 = 0
flag2 = 0
cap = cv2.VideoCapture(0)
statename = "null"

cap.set(3,640) # Width
cap.set(4,480) # Height
# When changing resolution, you may need to remap window locations in the movewindow() functions furthur below.

while (True):

    ret, frame = cap.read() # Reads next frame
    output = frame.copy() # Creates output frame
    t = time.time() #Stores system time at start of program exacution loop (used for calculating loop time on your state later)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # STATE 1
    if (state == 1):
        statename = "No Image Processing"
        if (flag == 0):
            print("State 1: ", statename)
            flag = 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # STATE 2
    if (state == 2):
        statename = "BGR to Grayscale"
        if (flag == 0):
            print("State 2: ", statename)
            flag = 1
        output = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # STATE 3:
    if (state == 3):
        statename = "Edge Detection"
        if (flag == 0):
            print("State 3: ", statename)
            flag = 1
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        output = cv2.Canny(gray,100,200)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # STATE 4
    if (state == 4):
        statename = "Detect Orange Area"
        if (flag == 0):
            print("State 4: ", statename)
            flag = 1
        cv2.putText(output, 'Looking for orange objects',(200, 450), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0,100,150), (50,255,255)) # Looking for hues in the orange range
        # Identify controur
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if(len(contours) > 0):
            max_area = 0
            ci = ""
            # Check each Contour
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci = cnt
            if(ci != ""):
                #Calculate Moments
                moments = cv2.moments(ci)
                if(moments['m00'] != 0):
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
                    cv2.circle(output,(cx,cy),5,(0,0,255),-1)
                    #print("Coordinates", cx, cy)
                #Draw Contours
                cv2.drawContours(output,[ci],0,(255,0,0),2)



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #STATE 5
    if (state == 5):
        statename = "EMPTY FUNCTION"
        if (flag == 0):
            print("State 5: ", statename)
            flag = 1
        # You may put your own OpenCV here
        #
        #
        #
        #
        #


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #STATE 6
    if (state == 6):
        statename = "EMPTY FUNCTION"
        if (flag == 0):
            print("State 6: ", statename)
            flag = 1
        # You may put your own OpenCV here
        #
        #
        #
        #
        #

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #STATE 7
    if (state == 7):
        statename = "EMPTY FUNCTION"
        if (flag == 0):
            print("State 7: ", statename)
            flag = 1
        # You may put your own OpenCV here
        #
        #
        #
        #
        #

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #STATE 8
    if (state == 8):
        statename = "EMPTY FUNCTION"
        if (flag == 0):
            print("State 8: ", statename)
            flag = 1
        # You may put your own OpenCV here
        #
        #
        #
        #
        #

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #STATE 9
    if (state == 9):
        statename = "EMPTY FUNCTION"
        if (flag == 0):
            print("State 9: ", statename)
            flag = 1
        # You may put your own OpenCV here
        #
        #
        #
        #
        #

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #STATE 0
    if (state == 0):
        statename = "EMPTY FUNCTION"
        if (flag == 0):
            print("State 0: ", statename)
            flag = 1
        # You may put your own OpenCV here
        #
        #
        #
        #
        #



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    dt = time.time() - t #Calculates the time taken to cycle your CV state
    cv2.putText(frame, 'CycleSpeed: %.9f sec' % (dt),(350, 20), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1) #outputs latency
    #print(dt) #Debugging latency time

    cv2.putText(frame, '1: %s' % (statename),(30, 20), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '2: %s' % (statename),(30, 60), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '3: %s' % (statename),(30, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '4: %s' % (statename),(30, 140), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '5: %s' % (statename),(30, 180), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '6: %s' % (statename),(30, 220), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '7: %s' % (statename),(30, 260), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '8: %s' % (statename),(30, 300), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '9: %s' % (statename),(30, 340), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    cv2.putText(frame, '0: %s' % (statename),(30, 380), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
    # ONLY send TCP/IP coordinates if you are in a state that defines the camera x and y variables ('cx' and 'cy')
    cv2.putText(frame, 'S: Send TCP/IP coords',(30, 420), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
    cv2.putText(frame, 'Q: Exit',(30, 438), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
    cv2.putText(frame, 'State: %s' % (statename),(400, 438), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)

    cv2.imshow('Output',output)
    cv2.imshow('Input',frame)
    if (flag2 == 0):
        cv2.moveWindow("Output", 700,20)
        cv2.moveWindow("Input", 20,20)
        flag = 1

    # State change keypress LISTENERS (Do not change unless you know what ur doing)
    keyDown = cv2.waitKey(1)
    if keyDown == ord('1'):
            state = 1
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('2'):
            state = 2
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('3'):
            state = 3
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('4'):
            state = 4
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('5'):
            state = 5
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('6'):
            state = 6
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('7'):
            state = 7
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('8'):
            state = 8
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('9'):
            state = 9
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('0'):
            state = 0
            flag = 0
            cv2.destroyAllWindows()

    if keyDown == ord('s'): # Send TCPIP coordinates.
            flag1 = 1 # TCPIP flag
            if (state >= 4):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connecting socket to the port
                server_address = ('192.168.0.20', 1025)
                sock.connect(server_address)
                print('connected to %s port %s!' % server_address)

                # Wait for server to send Execute command
                while (True):
                    data = sock.recv(7)
                    amount_received = 7
                    print("Waiting for response")
                    if data == b'Execute':
                        print('received "%s"' % data)
                        break

                # Debug text for console
                print('Local x-coordinate "%s"' % cx)
                print('Local y-coordinate "%s"' % cy)

                # Geometrical transform for 2019 project. This will only work for objects
                # with an elevation of ~1122.5mm high in the z-axis in the robot base frame.
                # You may replace this function with our own transform if applicable.
                Xs = (cy / 480) * 344.4 + 1167.9
                Ys = (cx / 640) * 440.6 - 243
                # Geometric function ends.

                # Send data
                message = bytes(str(Xs), 'ascii')
                print('sending X coordinate "%s"' % message)
                sock.sendall(message)

                message = bytes(str(Ys), 'ascii')
                print('sending Y coordinate "%s"' % message)
                sock.sendall(message)



    # QUIT PROGRAM
    if keyDown == ord('q'):
        print('Quitting')
        break


# Closing Program
cap.release()
cv2.destroyAllWindows()
if flag1 == 1:
    print(sys.stderr, 'closing socket')
    sock.close()
