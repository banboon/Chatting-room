import sys
import socket
import time
from select import select


RECV_BUFFER = 4096


# create a socket project
def server(argv):     
    HOST = None     
    PORT = 9876

    if len(argv) > 1:
        PORT = argv[1]

    listenSock = None
    res = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)

    for one in res:
        af, socktype, proto, canonname, sa = one
        try:
            listenSock = socket.socket(af, socktype, proto)
        except OSError as msg:
            listenSock = None
            continue
        try:
            listenSock.bind(sa)
            listenSock.listen(5)
        except OSError as msg:
            listenSock.close()
            listenSock = None
            continue
        break

    if listenSock is None:
        print('could not open socket')
        sys.exit(1)

    clientSockets = []

    while True:
        read_list = [listenSock] + clientSockets
        write_list = []
        error_list = []
        timeout = 1

        readable, writable, e = select(read_list, write_list, error_list, timeout)

        for sock in readable:
            if sock == listenSock:
                clientSock, addr = listenSock.accept()
                clientSockets.append(clientSock)

        for it in clientSockets:
            if it in read_list or it in error_list:
                data = it.recv(RECV_BUFFER)
                print(data)
                if not data:
                    it.close()
                    clientSockets.remove(it)
                else:
                    for sock in clientSockets:
                        if it != sock:
                            try:
                                sock.sendall(data)
                            except:
                                sock.close()
                                clientSockets.remove(sock)

    listenSock.close()


if __name__ == '__main__':
    server(sys.argv)