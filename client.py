# Simple client for chat program
import socket
from select import select

HOST = 'localhost'
PORT = int(input("Use what port:"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect( (HOST, PORT) )
s.setblocking(False)

userInput = input("Enter what to send:")
while userInput != "q":
	socketsToRead, socketsToWrite, erred = select([s],[s],[])
	if s in socketsToWrite:
		s.sendall(userInput.encode("utf-8"))
	if s in socketsToRead:
		data = s.recv(1024)
		print('Received', data.decode('utf-8'))
	userInput = input("Enter what to send:")
s.close()
