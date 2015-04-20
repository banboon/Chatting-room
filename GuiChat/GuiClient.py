import sys, socket
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *
from datetime import datetime


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.sock = QTcpSocket(self)

        self.sock.connected.connect(self.connected)
        self.sock.readyRead.connect(self.readyRead)


    def setupUi(self):
        self.setWindowTitle('Chatting room')
        self.setMinimumWidth(550)

        self.chatting_log = ''

        self.SetupWidget()


    def AddPushButton(self, name, layout, conn_func):
        '''
        Add push button for GUI.
        '''
        new_button = QPushButton(name, self)
        new_button.clicked.connect(conn_func)
        layout.addWidget(new_button)
        return new_button


    def AddLabel(self, name, layout):
        new_label = QLabel(name)
        layout.addWidget(new_label)


    def SetupWidget(self):
        '''
        '''
        self.layout = QVBoxLayout()
        #self._layout.setSpacing(10)

        self.hlayout_top = QHBoxLayout()
        # Add 'welcome' label
        self.AddLabel('Welcome to Banboon chat room!', self.hlayout_top)
        self.hlayout_top.addStretch(1)
        # setup 'login' button
        self.login_button = self.AddPushButton('Login', self.hlayout_top, self.on_loginButton_clicked)
        # setup 'exit' button
        self.exit_button = self.AddPushButton('Exit', self.hlayout_top, self.close)

        self.layout.addLayout(self.hlayout_top)

        # Setup window for chatting history
        self._chatting_text = QTextEdit(self)
        self._chatting_text.setMinimumHeight(80)
        self._chatting_text.setStyleSheet('QTextEdit { font: 13px; } QTextEdit[class=invalid] { background-color: #FFCDCD; };')

        self.layout.addWidget(self._chatting_text)

        self.enter_label = self.AddLabel('Please enter: ', self.layout)

        self.hlayout_bottom = QHBoxLayout()

        # Setup text line for entering text to be sent
        self.enter_text = QLineEdit(self)
        self.enter_text.setMinimumWidth(400)

        self.hlayout_bottom.addWidget(self.enter_text)
        self.hlayout_bottom.addStretch(1)

        # Setup 'enter' button
        self.enter_button = self.AddPushButton('Enter', self.hlayout_bottom, self.on_sayButton_clicked)

        # Enable keyboard 'return' hit function
        self.enter_text.returnPressed.connect(self.enter_button.clicked)

        self.layout.addLayout(self.hlayout_bottom)

        self.setLayout(self.layout)


    def Run(self):
        self.show()


    def on_sayButton_clicked(self):
        curText = socket.gethostname() + ' ' + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') + ' :' + '\n' + self.enter_text.text() + '\n\n'
        self.chatting_log = self.chatting_log + curText
        self._chatting_text.setText(self.chatting_log)

        if curText:
            self.sock.write(curText.encode())

        self.enter_text.clear()
        self.enter_text.setFocus()


    def on_loginButton_clicked(self):
        host = '127.0.0.1'
        port = 9876
        self.sock.connectToHost(host, port)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # close the socket
            if self.sock.state() is not QAbstractSocket.ClosingState:
                self.sock.close()
            event.accept()
        else:
            event.ignore()


    def connected(self):
        self.chatting_log = 'Connected to chat server. You can start sending messages.\n\n'
        self._chatting_text.setText(self.chatting_log)
        self.enter_text.setFocus()


    def readyRead(self):
        while self.sock.canReadLine():
            line = self.sock.readLine()
            self.chatting_log = self.chatting_log + str(line)
        self.chatting_log = self.chatting_log
        self._chatting_text.setText(self.chatting_log)


def main(argv):
    app = QApplication(argv)
    win = MainWindow()
    win.Run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)