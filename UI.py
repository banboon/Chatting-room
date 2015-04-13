import sys
from PySide.QtCore import *
from PySide.QtGui import *

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

        self._chatting_text = QTextEdit(self)
        self._chatting_text.setMinimumHeight(80)
        self._chatting_text.setStyleSheet('QTextEdit { font: 18px; } QTextEdit[class=invalid] { background-color: #FFCDCD; };')

        self._layout.addWidget(self._chatting_text)

        enter_label = QLabel('Please enter: ')
        self._layout.addWidget(enter_label)

        hlayout = QHBoxLayout()

        self._enter_text = QLineEdit(self)
        self._enter_text.setMinimumWidth(400)

        hlayout.addWidget(self._enter_text)
        hlayout.addStretch(1)

        self.enter_button = QPushButton('Enter', self)
        self.enter_button.clicked.connect(self.execute)
        hlayout.addWidget(self.enter_button)

        self._layout.addLayout(hlayout)

        self.setLayout(self._layout)

    def run(self):
        self.show()

    def execute(self):
    	self.chatting_log = self._enter_text.text() if self.chatting_log is '' else self.chatting_log + '\n' + self._enter_text.text()
    	self._chatting_text.setText(self.chatting_log)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()