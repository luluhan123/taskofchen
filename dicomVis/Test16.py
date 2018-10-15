import sys
from vtk import *
from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class myMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.renWin = self.vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.renWin.SetSize(600, 600)
        self.iren = self.renWin.GetInteractor()

        # reader the dicom file
        self.reader = vtkDICOMImageReader()
        self.reader.SetDataByteOrderToLittleEndian()
        self.reader.SetDirectoryName('P01dicom')
        self.reader.Update()

        # show the dicom flie
        self.imageViewer = vtkImageViewer2()
        self.imageViewer.SetInputConnection(self.reader.GetOutputPort())
        self.renderWindowInteractor = vtkRenderWindowInteractor()
        self.imageViewer.SetupInteractor(self.renderWindowInteractor)
        self.imageViewer.SetRenderWindow(self.vtkWidget.GetRenderWindow())

        self.renderWindowInteractor.RemoveObservers('MouseWheelForwardEvent')
        self.renderWindowInteractor.RemoveObservers('MouseWheelBackwardEvent')
        self.renderWindowInteractor.AddObserver('MouseWheelForwardEvent', self.DummyFunc1, 1.0)
        self.renderWindowInteractor.AddObserver('MouseWheelBackwardEvent', self.DummyFunc2, -1.0)

        self.renderWindowInteractor.Render()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()

    def DummyFunc1(self, obj, ev):
        print("forward")

    def DummyFunc2(self, obj, ev):
        print("backward")


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = myMainWindow()

    sys.exit(app.exec_())