import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp
from PyQt5.QtGui import QIcon

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        exitAction = QAction(QIcon('F:\Python\PyQt5\MenusAndToolbar\images\exit.png'), '&退出', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出应用程序')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&文件')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('菜单栏')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
