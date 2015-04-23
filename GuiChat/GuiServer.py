import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtNetwork import *


class ServerWindow(QWidget):
    def __init__(self):
        super(ServerWindow, self).__init__()
        self.setupUi()

        # Create a TCP server for chat room
        self.server = QTcpServer(self)

        # list to store connected client sockets
        self.client_sockets = []
        self.server.newConnection.connect(self.newConnection)


    def setupUi(self):
        self.setWindowTitle('Chat Server')
        self.layout = QVBoxLayout()

        self.hlayout_1 = QHBoxLayout()

        self.port_lbl = QLabel('Port: ', self)
        self.hlayout_1.addWidget(self.port_lbl)

        self.port_input = QLineEdit()
        self.port_input.setMaxLength(5)
        self.hlayout_1.addWidget(self.port_input)

        self.hlayout_1.addStretch(1)
        self.layout.addLayout(self.hlayout_1)

        self.connect_log = QTextEdit(self)
        self.connect_log.setReadOnly(True)
        self.layout.addWidget(self.connect_log)

        self.hlayout_2 = QHBoxLayout()

        self.start_btn = QPushButton('Start Server', self)
        self.start_btn.clicked.connect(self.start)
        self.hlayout_2.addWidget(self.start_btn)

        self.close_btn = QPushButton('Close Server', self)
        self.close_btn.clicked.connect(self.close)
        self.hlayout_2.addWidget(self.close_btn)

        self.layout.addLayout(self.hlayout_2)
        
        self.setLayout(self.layout)


    @Slot()    
    def start(self):
        '''
        When start button clicked, start listening on port.
        '''
        if self.port_input.text():
            self.server.listen(QHostAddress('0.0.0.0'), int(self.port_input.text()))
            text = "Start listening on port %s." % self.port_input.text()
            self.connect_log.append(text)


    def closeEvent(self, event):
        for it in self.client_sockets:
            if it.state() is not QAbstractSocket.ClosingState:
                it.close()
        self.close()
        event.accept()


    @Slot()
    def newConnection(self):
        '''
        When there is a new client connection, add the client socket into list.
        '''
        client_sock = self.server.nextPendingConnection()
        client_sock.readyRead.connect(self.readyRead)
        client_sock.disconnected.connect(self.clientDisconnect)
        self.client_sockets.append(client_sock)

        # send to all the clients the current user list
        userList = 'User: \n'
        for sock in self.client_sockets:
            userList += '(%s, %s)\n' % (sock.peerAddress().toString(), str(sock.peerPort()))
        for sock in self.client_sockets:
            sock.write(userList.encode())
        
        # Multicast to notify other clients the coming of the new user
        message = 'Client (%s, %s) entered our chat room.\n' % (client_sock.peerAddress().toString(), str(client_sock.peerPort()))
        self.multicast(client_sock, message)
        
        # Update the connection log
        text = 'Client (%s, %s) connected.' % (client_sock.peerAddress().toString(), str(client_sock.peerPort()))
        self.connect_log.append(text)


    @Slot()
    def readyRead(self):
        '''
        When there is incoming data, read in the data and forward to other clients.
        '''
        sock = self.sender()

        if sock.isValid():            
            message = ''
            # while sock.canReadLine():
            #     message = message + str(sock.readLine())
            if sock.isReadable():
                message = str(sock.readAll())

            self.multicast(sock, message)
        else:
            sock.close()
            self.client_sockets.remove(sock)


    def run(self):
        self.show()
        #self.port_input.setFocus()


    def multicast(self, sourceSock, message):
        for sock in self.client_sockets:
            if sock is not sourceSock:
                sock.write(message.encode())


    @Slot()
    def clientDisconnect(self):
        sender = self.sender()

        # Update the connection log
        text = 'Client (%s, %s) disconnected.' % (sender.peerAddress().toString(), str(sender.peerPort()))
        self.connect_log.append(text)

        # send to all the clients the current user list
        userList = 'User: \n'
        for sock in self.client_sockets:
            if sock is not sender:
                userList += '(%s, %s)\n' % (sock.peerAddress().toString(), str(sock.peerPort()))
        for sock in self.client_sockets:
            sock.write(userList.encode())

        message = 'Client (%s, %s) left our chat room.' % (sender.peerAddress().toString(), str(sender.peerPort()))
        self.multicast(sender, message)

        sender.close()
        self.client_sockets.remove(sender)


def main(argv):
    app = QApplication(argv)
    chat_server = ServerWindow()
    chat_server.run()
    chat_server.move(0, 0)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
