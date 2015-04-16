import sys
import socket
import time

# create a socket project
def server(argv):     
    HOST = None     
    PORT = 9876

    if len(argv) > 1:
        PORT = argv[1]

    sockfd = None
    res = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)

    for one in res:
        af, socktype, proto, canonname, sa = one
        try:
            sockfd = socket.socket(af, socktype, proto)
        except OSError as msg:
            sockfd = None
            continue
        try:
            sockfd.bind(sa)
            sockfd.listen(5)
        except OSError as msg:
            sockfd.close()
            sockfd = None
            continue
        break

    if sockfd is None:
        print('could not open socket')
        sys.exit(1)

    conn, addr = sockfd.accept()
    print('Connected by ', addr)

    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)

    sockfd.close()


if __name__ == '__main__':
    server(sys.argv)