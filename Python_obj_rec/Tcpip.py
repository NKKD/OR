import socket

# define socket category and socket type in our case using TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create a socket with IP address 192.168.12.248 port number 1025

Tcp_IP = '192.168.12.248'
Tcp_Port = 1025

# Open the socket and listen

s.bind((Tcp_IP,Tcp_Port))
s.listen(1)

conn,addr = s.accept()
print ('Connection address:',addr)

while True:

    data = conn.recv(1024)
    print ("recive data: ")
    print(data)

    if not data:
        break
        print("Connection lost")

    if data == b'1':
        print("Connection esitablished")


    x = 0.57339
    y = -0.09126
    z = 0.2
    a = -2.18148
    b = 2.2607
    c = -0



    coordinate = x,y,z,a,b,c

    # Send data
    message = bytes(str(coordinate),'ascii')
    print('sending X coordinate "%s"' % message)
    conn.send(message)

    conn.close()

    break



