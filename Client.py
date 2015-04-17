import sys, socket, select


def client(argv):
    if len(argv) < 2:
        print("Usage: chat hostname")
        sys.exit(1)

    HOST = argv[1]
    PORT = 9876

    if len(argv) > 2: 
        PORT = argv[2]  

    mySockfd = None
    # get the address of the remoter server
    res = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM)

    # try to connect to the remote server
    for one in res:
        af, socktype, proto, canonname, sa = one
        try:
            mySockfd = socket.socket(af, socktype, proto)
        except OSError as msg:
            mySockfd = None
            continue
        try:
            mySockfd.connect(sa)
        except OSError as msg:
            mySockfd.close()
            mySockfd = None
            continue
        break

    if mySockfd is None:
        print('Unable to connect')
        sys.exit(2)

    print('Connected to chat server. You can start sending messages.')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    # set up the select list used for select
    read_list = [sys.stdin, mySockfd]
    write_list = []
    error_list = [sys.stdin, mySockfd]

    while True:
        # Get the ready sockets or fileno
        ready_to_read, ready_to_write, in_error = select.select(read_list, write_list, error_list)

        for it in ready_to_read:
            if it is mySockfd:
                data = it.recv(4096)
                if not data:
                    print('Disconnect from the chat server')
                    sys.exit(3)
                else:
                    sys.stdout.write(data.decode())
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()
            if it is sys.stdin:
                data = sys.stdin.readline()
                mySockfd.sendall(data.encode())
                sys.stdout.write('[Me] ')
                sys.stdout.flush()

    mySockfd.close()


if __name__ == '__main__':
    client(sys.argv)