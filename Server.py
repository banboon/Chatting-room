import socket
import time

# create a socket project

serversocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9876

serversocket.bind((host, port))

serversocket.listen(5)

while True:

	clientSocket,addr = serversocket.accept()

	print('A connect from :%s' % str(addr))
	currentTime = time.ctime(time.time())+"\r\n"
	clientSocket.send(currentTime.encode('ascii'))
	clientSocket.close()
