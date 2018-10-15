import vtk
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class myVtkInteractorStyleImage(vtk.vtkInteractorStyleImage):
    def __init__(self):
        pass

    def SetImageViewer(self, imageViewer):
        self._ImageViewer = imageViewer
        self._MinSlice = imageViewer.GetSliceMin()
        self._MaxSlice = imageViewer.GetSliceMax()
        self._Slice = self._MinSlice
        print("Slicer: Min = ",self._MinSlice,", Max = ",self._MaxSlice)

    def MoveSliceForward(self):
        if self._Slice < self._MaxSlice:
            self._Slice += 1;
            print("MoveSliceForward::Slice = ", self._Slice)
            self._ImageViewer.SetSlice(self._Slice)

            msg = "Slice Number :" + str(self._Slice + 1)+"/"+  str(self._MaxSlice+1)
            self._ImageViewer.Render()

    def MoveSliceBackward(self):
        if self._Slice > self._MinSlice:
            self._Slice -= 1
            print("MoveSliceBackward::Slice = ",self._Slice)
            self._ImageViewer.SetSlice(self._Slice)
            msg = "Slice Number :" + str(self._Slice + 1)+"/"+ str(self._MaxSlice + 1)
            self._ImageViewer.Render()

    def OnKeyDown(self):
        print(self.GetInteractor())
        key = self.GetInteraction().GetKeySym()
        if key.compare("Up") == 0:
            self.MoveSliceForward()
        elif key.compare("Down") == 0:
            self.MoveSliceBackward()
        super.OnkeyDown()

    def OnMouseWheelForward(self):
        self.MoveSliceForward()

    def OnMouseWheelBackward(self):
        if self._Slice > self._MinSlice:
            self.MoveSliceBackward()

def DummyFunc1(obj, ev):
    obj.GetInteractorStyle().MoveSliceBackward()
    print("Before Event")

def DummyFunc2(obj, ev):
    obj.GetInteractorStyle().MoveSliceForward()
    print("After Event")

class ProjectMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent= None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.reader = vtk.vtkDICOMImageReader()
        self.reader.SetDirectoryName('P01dicom')
        self.reader.Update()

        self.imageViewer = vtk.vtkImageViewer2()
        self.imageViewer.SetInputConnection(self.reader.GetOutputPort())

        self.renderder = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderder)
        self.imageViewer.SetRenderWindow(self.vtkWidget.GetRenderWindow())
        self.imageViewer.SetRenderer(self.renderder)
        self.myInteractorStyle = myVtkInteractorStyleImage()
        self.myInteractorStyle.SetImageViewer(self.imageViewer)
        self.renderWindowInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.imageViewer.SetupInteractor(self.renderWindowInteractor)

        self.myInteractorStyle = myVtkInteractorStyleImage()
        self.myInteractorStyle.SetImageViewer(self.imageViewer)

        self.renderWindowInteractor.SetInteractorStyle(self.myInteractorStyle)
        self.renderWindowInteractor.RemoveObservers('MouseWheelForwardEvent')
        self.renderWindowInteractor.RemoveObservers('MouseWheelBackwardEvent')
        self.renderWindowInteractor.AddObserver('MouseWheelForwardEvent', DummyFunc1, 1.0)
        self.renderWindowInteractor.AddObserver('MouseWheelBackwardEvent', DummyFunc2, 1.0)

        self.imageViewer.Render()
        self.imageViewer.GetRenderer().ResetCamera()
        self.imageViewer.Render()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.renderWindowInteractor.Initialize()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ProjectMainWindow()

    sys.exit(app.exec_())
