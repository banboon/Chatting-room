import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtNetwork import *


class Server(QPushButton):
    def __init__(self, parent = None):
        super(Server, self).__init__('&Close Server', parent)

        self.server = QTcpServer(self)

        self.client_sockets = []
        self.server.newConnection.connect(self.newConnection)
        self.clicked.connect(self.close)

        self.server.listen(QHostAddress('0.0.0.0'), 9876)


    def newConnection(self):
        client_sock = self.server.nextPendingConnection()
        client_sock.readyRead.connect(self.readyRead)
        self.client_sockets.append(client_sock)


    def readyRead(self):
        for sock in self.client_sockets:
            message = ''
            while sock.canReadLine():
                message = message + str(sock.readLine())

            for other in self.client_sockets:
                if other is not sock:
                    other.write(message.encode())


    def run(self):
        self.show()


def main(argv):
    app = QApplication(argv)
    chat_server = Server()
    chat_server.run()
    chat_server.move(0, 0)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
