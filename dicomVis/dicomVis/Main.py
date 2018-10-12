from __future__ import print_function
import os
import vtk
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QHBoxLayout, QAction, QFileDialog, QMessageBox
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5 import uic
import dicomWidget
import dicomView

class GlyphViewerApp(QMainWindow):
    def __init__(self):
        # Parent constructor
        super(GlyphViewerApp, self).__init__()
        self.vtk_widget = None
        self.ui = None
        self.setup()

    def setup(self):
        exitAction = QAction('&File', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Open dicom directory')
        exitAction.triggered.connect(self.changeDir)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        self.vtk_widget = dicomWidget.dicomWidget()
        self.Dicomshow()

    def Dicomshow(self):
        self.information = self.vtk_widget.getInformation()
        self.ui = dicomView.Ui_MainWindow()
        self.ui.setupUi(self, self.information)
        self.ui.vtk_layout = QHBoxLayout()
        self.ui.vtk_layout.addWidget(self.vtk_widget)
        self.ui.vtk_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.vtk_panel.setLayout(self.ui.vtk_layout)

    def initialize(self):
        self.vtk_widget.start()

    def changeDir(self):
        directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        flag = True
        for dirName,subdirList,fileList in os.walk(directory1):
            for filename in fileList:
                if ".dcm" not in filename.lower():
                    flag = False
        if flag:
            self.vtk_widget.setPath(directory1)
            self.vtk_widget.ReadandShow()
            self.Dicomshow()
        else:
            reply = QMessageBox.question(self, 'Message', '该目录下没有dicom序列',
                                         QMessageBox.Yes)



if __name__ == "__main__":
    app = QApplication([])
    main_window = GlyphViewerApp()
    main_window.show()
    main_window.initialize()
    app.exec_()