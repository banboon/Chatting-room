import sys
import socket


def client(argv):
    if len(argv) < 2:
        print("Usage: chat hostname")
        sys.exit(1)

    HOST = argv[1]
    PORT = 9876

    if len(argv) > 2: 
        PORT = argv[2]  

    sockfd = None
    res = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM)

    for one in res:
        af, socktype, proto, canonname, sa = one
        try:
            sockfd = socket.socket(af, socktype, proto)
        except OSError as msg:
            sockfd = None
            continue
        try:
            sockfd.connect(sa)
        except OSError as msg:
            sockfd.close()
            sockfd = None
            continue
        break

    if sockfd is None:
        print('could not open socket')
        sys.exit(2)

    sockfd.sendall(b'Hello world')
    data = sockfd.recv(1024)

    sockfd.close()

    print('Received', repr(data))


if __name__ == '__main__':
    client(sys.argv)