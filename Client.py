import sys
import socket
from select import select


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

    while True:
        read_list = [sys.stdin, sockfd]
        write_list = []
        error_list = [sys.stdin, sockfd]

        ready_to_read, ready_to_write, in_error = select(read_list, write_list, error_list)

        for it in ready_to_read:
            if it is sockfd:
                data = it.recv(4096)
                if not data:
                    print('Disconnect from server')
                    sys.exit(3)
                sys.stdout.write(data.decode('UTF-8'))
                sys.stdout.flush()
            if it is sys.stdin:
                data = sys.stdin.readline()
                sockfd.sendall(bytes(data, 'UTF-8'))

    sockfd.close()


if __name__ == '__main__':
    client(sys.argv)