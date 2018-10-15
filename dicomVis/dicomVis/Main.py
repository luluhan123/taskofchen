from __future__ import print_function
import os
import vtk
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QHBoxLayout, QAction, QFileDialog, QMessageBox, \
    QInputDialog
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
        self.Model3D = True
        self.setup()

    def setup(self):
        exitAction = QAction('&File', self)
        exitAction.setShortcut('Ctrl+O')
        exitAction.setStatusTip('Open dicom directory')
        exitAction.triggered.connect(self.changeDir)

        modelChangeAction = QAction('&Change', self)
        modelChangeAction.setShortcut('Ctrl+C')
        modelChangeAction.setStatusTip('Open dicom model')
        modelChangeAction.triggered.connect(self.changeModel)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        change3D2DMenu = menubar.addMenu('&Change')
        change3D2DMenu.addAction(modelChangeAction)

        toolbar = self.addToolBar('Menu')
        toolbar.addAction(exitAction)
        toolbar.addAction(modelChangeAction)
        if self.Model3D:
            self.vtk_widget = dicomWidget.dicomWidget()
            self.Dicomshow()
        else:
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
        if directory1.strip()=="":
            flag = False
        else:
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

    def changeModel(self):
        oldModel = self.Model3D
        items = ["2D", "3D"]
        value, ok = QInputDialog.getItem(self,"模型类型", "请选择模型类型:", items, 1, True)
        if value == "2D":
            self.Model3D = False
        else:
            self.Model3D = True
        if oldModel != self.Model3D:
            print("changed!")
            if self.Model3D == True:
                print("3D")
            else:
                print("2D")
        print(self.Model3D)

if __name__ == "__main__":
    app = QApplication([])
    main_window = GlyphViewerApp()
    main_window.show()
    main_window.initialize()
    app.exec_()