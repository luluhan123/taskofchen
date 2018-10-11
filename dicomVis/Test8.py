import pydicom
import vtk

class StatusMessage():
    def Format(self, slice, maxslice):
        temp = "Slice Number :" + slice + 1+"/"+ maxslice + 1
        return temp

class myVtkInteractorStyleImage(vtk.vtkInteractorStyleImage):
    def __init__(self):
        pass

    def SetImageViewer(self, imageViewer):
        self._ImageViewer = imageViewer
        self._MinSlice = imageViewer.GetSliceMin()
        self._MaxSlice = imageViewer.GetSliceMax()
        self._Slice = self._MinSlice
        print("Slicer: Min = ",self._MinSlice,", Max = ",self._MaxSlice)

    def SetStatusMapper(self,statusMapper):
        self._StatusMapper = statusMapper

    def MoveSliceForward(self):
        if self._Slice < self._MaxSlice:
            self._Slice += 1;
            print("MoveSliceForward::Slice = ", self._Slice)
            self._ImageViewer.SetSlice(self._Slice)

            msg = StatusMessage.Format(self._Slice, self._MaxSlice)
            self._StatusMapper.SetInput(msg)
            self._ImageViewer.Render()

    def MoveSliceBackward(self):
        if self._Slice > self._MinSlice:
            self._Slice -= 1
            print("MoveSliceBackward::Slice = ",self._Slice)
            self._ImageViewer.SetSlice(self._Slice)
            msg = StatusMessage.Format(self._Slice, self._MaxSlice)
            self._StatusMapper.SetInput(msg)
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
    print("Before Event")


def DummyFunc2(obj, ev):
    print("After Event")

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName('P01dicom')
reader.Update()

# imageViewer = vtk.vtkImageViewer2()
# imageViewer.SetInputConnection(reader.GetOutputPort())

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(actor)

renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
renderWindowInteractor.SetRenderWindow(renwin)

renderWindowInteractor.RemoveObservers('MouseWheelForwardEvent')
renderWindowInteractor.RemoveObservers('MouseWheelBackwardEvent')
renderWindowInteractor.AddObserver('MouseWheelForwardEvent', DummyFunc1, 1.0)
renderWindowInteractor.AddObserver('MouseWheelBackwardEvent', DummyFunc2, -1.0)
renderWindowInteractor.Initialize()


# imageViewer.Render()
# imageViewer.GetRenderer().ResetCamera()
# imageViewer.Render()
renderWindowInteractor.Start()