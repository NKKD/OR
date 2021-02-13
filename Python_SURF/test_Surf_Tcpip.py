import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import socket

if __name__ == '__main__':

    # define socket category and socket type in our case using TCP/IP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # create a socket with IP address 192.168.12.248 port number 1025

    Tcp_IP = '192.168.12.253'
    Tcp_Port = 1025

    # Open the socket and listen

    s.bind((Tcp_IP, Tcp_Port))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)

    while True:

        cap = cv2.VideoCapture(1)

        cap.set(3, 1920)  # Width
        cap.set(4, 1080)  # Height

        ret, frame = cap.read()

        MIN_MATCH_COUNT = 50

        img1 = cv2.imread('arduino.jpg', 0)  # Target Object

        img2 = frame  # Scene Image

        data = conn.recv(1024)

        print("recieved data: ")
        print(data)

        if data != b'1\r\n':
            print("Connection lost")

            break

        if data == b'1\r\n':
            print("Connection established")

            # run the surf object detection program

            # Initiate Surf detector
            s = cv2.xfeatures2d.SURF_create()
            # find key points and descriptors with SURF
            kp1, des1 = s.detectAndCompute(img1, None)
            kp2, des2 = s.detectAndCompute(img2, None)
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(des1, des2, k=2)
            # store all the good matches as per Lowe's ratio test.
            good = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)

            if len(good) > MIN_MATCH_COUNT:
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                matchesMask = mask.ravel().tolist()
                h, w = img1.shape
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            else:
                print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
                matchesMask = None

            draw_params = dict(matchColor=(255, 255, 0),  # draw matches in green color
                               singlePointColor=None,
                               matchesMask=matchesMask,  # draw only inliers
                               flags=2)
            img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

            try:

                M is not None

                print('Transformation matrix M is:', '\n', M, '\n')
                print('Bounding box corners coordinates dst: ', '\n', dst, '\n')
                # print('centroid of the bounding box is', , '\n')

                R = M

                sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

                singular = sy < 1e-6

                if not singular:
                    ex = math.atan2(R[2, 1], R[2, 2])
                    ey = math.atan2(-R[2, 0], sy)
                    ez = math.atan2(R[1, 0], R[0, 0])
                else:
                    ex = math.atan2(-R[1, 2], R[1, 1])
                    ey = math.atan2(-R[2, 0], sy)
                    ez = 0

                print("The euler angle is ", ex, ey, ez, '\n')

                x0 = dst[0][0][0]
                y0 = dst[0][0][1]

                x1 = dst[1][0][0]
                y1 = dst[1][0][1]

                x2 = dst[2][0][0]
                y2 = dst[2][0][1]

                x3 = dst[3][0][0]
                y3 = dst[3][0][1]

                x = [x1, x2, x3, x0]
                y = [y0, y1, y2, y3]

                print("Max value of all x: ", max(x))
                print("Max value of all y: ", max(y))
                print("Min value of all x: ", min(x))
                print("Min value of all y: ", min(y))

                xcenter = 0.5 * (max(x) - min(x)) + min(x)
                ycenter = 0.5 * (max(y) - min(y)) + min(y)

                print("the center of the object is x y: ", xcenter, ycenter)

                plt.imshow(img3), plt.show()

                print("returned values are", xcenter, ycenter, ex, ey, ez)

                print("object detection program finished")

                z = 0.2

                a = -2.18148
                b = 2.2607
                c = -0 + ez

                coordinate = xcenter / 1000, ycenter / 1000, z, a, b, c

                # Send data
                message = bytes(str(coordinate), 'ascii')
                print('sending X coordinate "%s"' % message)
                conn.send(message)

                conn.close()
                cap.release()
                cv2.destroyAllWindows()

            except Exception as e:

                print("Object detection un-success")

                conn.close()
                cap.release()
                cv2.destroyAllWindows()
