from vtk import *

class myVtkInteractorStyleImage(vtkInteractorStyleImage):
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

def DummyFunc3(obj, ev):
    obj.GetInteractorStyle().OnKeyDown()
    print(ev)
    print("KeyPress")

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName('P01dicom')
reader.Update()

actor = vtkImageActor()
actor.SetInputData(reader.GetOutput())
print(actor)

render = vtkRenderer()
render.AddActor(actor)
render.ResetCamera()
render.SetBackground(1,1,1)

window = vtkRenderWindow()
window.AddRenderer(render)
# window.SetSize(640,480)
window.SetWindowName("ImageViewer3D")
window.Render()

rwi = vtkRenderWindowInteractor()
style = myVtkInteractorStyleImage()
rwi.SetInteractorStyle(style)

rwi.RemoveObservers('MouseWheelForwardEvent')
rwi.RemoveObservers('MouseWheelBackwardEvent')
rwi.RemoveObservers('KeyPressEvent')
rwi.AddObserver('MouseWheelForwardEvent', DummyFunc1, 1.0)
rwi.AddObserver('MouseWheelBackwardEvent', DummyFunc2, 1.0)
rwi.AddObserver('KeyPressEvent', DummyFunc3, 1.0)

rwi.SetRenderWindow(window)
rwi.Initialize()
rwi.Start()