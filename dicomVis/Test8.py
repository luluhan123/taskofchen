import vtk

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

def DummyFunc3(obj, ev):
    obj.GetInteractorStyle().OnKeyDown()
    print("KeyPress")

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName('P01dicom')
reader.Update()

imageViewer = vtk.vtkImageViewer2()
imageViewer.SetInputConnection(reader.GetOutputPort())

# sliceTextProp = vtk.vtkTextProperty()
# sliceTextProp.SetFontFamilyToCourier()
# sliceTextProp.SetFontSize(20)
# sliceTextProp.SetVerticalJustificationToBottom()
# sliceTextProp.SetJustificationToLeft()
#
# sliceTextMapper = vtk.vtkTextMapper()
# msg = "Slice Number :" + str(imageViewer.GetSliceMin())+"/"+ str(imageViewer.GetSliceMax())
# sliceTextMapper.SetInput(msg)
# sliceTextMapper.SetTextProperty(sliceTextProp)
#
# sliceTextActor = vtk.vtkActor2D()
# sliceTextActor.SetMapper(sliceTextMapper)
# sliceTextActor.SetPosition(15,10)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
myInteractorStyle = myVtkInteractorStyleImage()
myInteractorStyle.SetImageViewer(imageViewer)


imageViewer.SetupInteractor(renderWindowInteractor)
renderWindowInteractor.SetInteractorStyle(myInteractorStyle)
renderWindowInteractor.RemoveObservers('MouseWheelForwardEvent')
renderWindowInteractor.RemoveObservers('MouseWheelBackwardEvent')
#renderWindowInteractor.RemoveObservers('KeyPressEvent')
renderWindowInteractor.AddObserver('MouseWheelForwardEvent', DummyFunc1, 1.0)
renderWindowInteractor.AddObserver('MouseWheelBackwardEvent', DummyFunc2, 1.0)
#renderWindowInteractor.AddObserver('KeyPressEvent', DummyFunc3, 1.0)

imageViewer.Render()
imageViewer.GetRenderer().ResetCamera()
imageViewer.Render()
renderWindowInteractor.Start()
