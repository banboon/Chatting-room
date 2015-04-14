import sys
import socket
from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Chatting room')
        self.setMinimumWidth(550)

        self.chatting_log = ''

        self.setupWidget()


    def setupWidget(self):
        self._layout = QVBoxLayout()
        #self._layout.setSpacing(10)

        # Setup window for chatting history
        self._chatting_text = QTextEdit(self)
        self._chatting_text.setMinimumHeight(80)
        self._chatting_text.setStyleSheet('QTextEdit { font: 18px; } QTextEdit[class=invalid] { background-color: #FFCDCD; };')

        self._layout.addWidget(self._chatting_text)

        enter_label = QLabel('Please enter: ')
        self._layout.addWidget(enter_label)

        hlayout = QHBoxLayout()

        # Setup text line for entering text to be sent
        self._enter_text = QLineEdit(self)
        self._enter_text.setMinimumWidth(400)

        hlayout.addWidget(self._enter_text)
        hlayout.addStretch(1)

        # Setup 'enter' button
        self.enter_button = QPushButton('Enter', self)
        self.enter_button.clicked.connect(self.execute)
        hlayout.addWidget(self.enter_button)

        # Enable keyboard 'return' hit function
        self._enter_text.returnPressed.connect(self.enter_button.clicked)

        self._layout.addLayout(hlayout)

        self.setLayout(self._layout)


    def run(self):
        self.show()


    def execute(self):
        curText = socket.gethostname() + ' ' + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') + ' :' + '\n' + self._enter_text.text()
        self.chatting_log = curText + '\n' if self.chatting_log is '' else self.chatting_log + '\n' + curText + '\n'
        self._chatting_text.setText(self.chatting_log)
        self._enter_text.setText('')
        

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()