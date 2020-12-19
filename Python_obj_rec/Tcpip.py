import socket

# define socket category and socket type in our case using TCP/IP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create a socket with IP address 192.168.12.248 port number 1025

Tcp_IP = '192.168.12.248'
Tcp_Port = 1025

# Open the socket and listen

serversocket.bind(Tcp_IP,Tcp_Port)
serversocket.listen()


