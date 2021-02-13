def recognition():
    print("object recognition start")

    import cv2

    cap = cv2.VideoCapture(1)

    # set the camera resolution to 1080p

    cap.set(3, 1920)  # Width
    cap.set(4, 1080)  # Height
    cx = 0
    cy = 0
    rx = 0
    ry = 0

    while (True):

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

        cv2.imshow('Input', frame)

        if cx and cy is not None:
            print(cx)
            print(cy)

        # transfter coordinates into robot system

        rx = (-(cy - 540)) * (217 / 1080) + 650  # mm
        ry = (-(cx - 960)) * (388.6 / 1920) - 127

        print("rx is :", rx)
        print("ry is :", ry)

        keyDown = cv2.waitKey(1)

        if keyDown == ord('q'):
            print('Quitting')
            break

    cap.release()
    cv2.destroyAllWindows()

    return rx, ry


if __name__ == '__main__':

    import socket

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

        data = conn.recv(1024)
        print("recive data: ")
        print(data)

        if not data:
            break
            print("Connection lost")

        if data == b'1':
            print("Connection esitablished")

            x, y = recognition()

            print("returned x and y is:", x, y)

            print("color recogition finished")

        z = 0.2

        a = -2.18148
        b = 2.2607
        c = -0

        coordinate = x/1000, y/1000, z, a, b, c

        # Send data
        message = bytes(str(coordinate), 'ascii')
        print('sending X coordinate "%s"' % message)
        conn.send(message)

        conn.close()

        break
