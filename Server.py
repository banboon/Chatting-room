import sys, socket, time, select


# predefine the buffer size
RECV_BUFFER = 4096


def Init(host, port):
    '''
    Setup the server socket and listen on that socket
    '''
    listenSock = None
    # get the address of the chat server
    res = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    
    for one in res:
        af, socktype, proto, canonname, sa = one
        try:
            listenSock = socket.socket(af, socktype, proto)
        except OSError as msg:
            listenSock = None
            continue
        try:
            # bind the address and port with the listen socket
            listenSock.bind(sa)
            # listen on that socket
            listenSock.listen(5)
        except OSError as msg:
            listenSock.close()
            listenSock = None
            continue
        break

    if listenSock is None:
        print('could not open socket')
        sys.exit(1)

    return listenSock


def Multicast(sockets, srcSockfd, data):
    '''
    Server forward data to all the other clients.
    '''
    for sock in sockets:
        if sock is not srcSockfd:
            try:
                sock.sendall(data.encode())
            except:
                sock.close()
                # sockets is shallow copy, so should be modified also in Server()
                sockets.remove(sock)


def Server(argv): 
    '''
    Main function
    '''    
    HOST = None     
    PORT = 9876

    if len(argv) > 1:
        PORT = argv[1]

    # initiate the server socket
    listenSock = Init(HOST, PORT)

    client_sockets = []

    while True:
        read_list = [listenSock] + client_sockets
        write_list = []
        error_list = []
        timeout = 1

        ready_to_read, ready_to_write, in_error = select.select(read_list, write_list, error_list, timeout)

        for sock in ready_to_read:
            if sock == listenSock:
                client_sock, client_addr = listenSock.accept()
                client_sockets.append(client_sock)
                print("Client (%s, %s) connected" % client_addr)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        Multicast(client_sockets, sock, data.decode())
                    else:
                        sock.close()
                        client_sockets.remove(sock)
                except:
                    sock.close()
                    continue

    listenSock.close()


if __name__ == '__main__':
    Server(sys.argv)