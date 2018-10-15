from vtk import *

def DummyFunc1(obj, ev):
    print(obj)
    print("Before Event")


def DummyFunc2(obj, ev):
    print("After Event")

# reader the dicom file
reader = vtkDICOMImageReader()
reader.SetDataByteOrderToLittleEndian()
reader.SetDirectoryName('P01dicom')
reader.Update()

# show the dicom flie
imageViewer = vtkImageViewer2()
imageViewer.SetInputConnection(reader.GetOutputPort())
renderWindowInteractor = vtkRenderWindowInteractor()
imageViewer.SetupInteractor(renderWindowInteractor)
print(renderWindowInteractor)

renderWindowInteractor.RemoveObservers('MouseWheelForwardEvent')
renderWindowInteractor.RemoveObservers('MouseWheelBackwardEvent')
renderWindowInteractor.AddObserver('MouseWheelForwardEvent', DummyFunc1, 1.0)
renderWindowInteractor.AddObserver('MouseWheelBackwardEvent', DummyFunc2, -1.0)

imageViewer.Render()
imageViewer.GetRenderer().ResetCamera()
imageViewer.Render()
renderWindowInteractor.Start()
