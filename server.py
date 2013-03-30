# Simple server for a chat program
import socket
from select import select

PORT = int(input("Use what port:"))

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setblocking(False)
serverSocket.bind( (socket.gethostname(), PORT) )
serverSocket.listen(5)
killServer = False
clientSockets = []
print("Server is", serverSocket, "at",socket.gethostname(), "at", serverSocket.getsockname())

while not killServer:
	socketsToRead, clientsToWrite, errord = select(clientSockets + [serverSocket], clientSockets,clientSockets)
	for socketToRead in socketsToRead:
		if socketToRead == serverSocket:
			newClient, newClientAdress = serverSocket.accept()
			print("New client", newClientAdress, "accepted")
			clientSockets.append(newClient)
		else:
			try:
				data = socketToRead.recv(1024)
			except socket.error:
				print("Client", socketToRead, "disconnected without recieving final data")
				socketToRead.close()
				clientSockets.remove(socketToRead)
				if socketToRead in clientsToWrite: clientsToWrite.remove(socketToRead)
				continue
			#if client disconnected
			if data == b'':
				print("Client", socketToRead, "disconnected!")
				socketToRead.close()
				clientSockets.remove(socketToRead)
			else:
				message = data.decode("utf-8")
				print("server recieved", message, "from", socketToRead.getpeername())
				if message == "killserver": killServer = True
				for socketToWrite in clientsToWrite:
					socketToWrite.sendall(data)

#shutdown stuff
print("Shutting down")
for clientSocket in clientSockets:
	clientSocket.close()
serverSocket.close()
