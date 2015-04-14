import socket

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9876

s.connect((host,port))

tm = s.recv(1024)

s.close()

print('Time: %s' % tm.decode('ascii'))

