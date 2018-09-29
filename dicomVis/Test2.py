from vtk import *


ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

Reader = vtkDICOMImageReader()
Reader.SetDirectoryName('sample')
Reader.SetDataByteOrderToLittleEndian()
Reader.Update()
print("读取数据完成")
print(Reader)

marchingCube = vtkMarchingCubes()
marchingCube.SetInputConnection(Reader.GetOutputPort())
marchingCube.SetValue(0,140)

Stripper = vtkStripper()
Stripper.SetInputConnection(marchingCube.GetOutputPort())

Mapper = vtkPolyDataMapper()
Mapper.SetInputConnection(Stripper.GetOutputPort())
Mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(Mapper)
actor.GetProperty().SetDiffuseColor(1, .49, .25)
actor.GetProperty().SetSpecular(0.3)
actor.GetProperty().SetSpecularPower(20)
actor.GetProperty().SetOpacity(1.0)
actor.GetProperty().SetColor(1,0,0)
actor.GetProperty().SetRepresentationToWireframe()

aCamera=vtkCamera()
aCamera.SetViewUp ( 0, 0, -1 )
aCamera.SetPosition ( 0, 1, 0 )
aCamera.SetFocalPoint( 0, 0, 0 )
aCamera.ComputeViewPlaneNormal()

outlinefilter=vtkOutlineFilter()
outlinefilter.SetInputConnection(Reader.GetOutputPort())

outlineMapper=vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlinefilter.GetOutputPort())

OutlineActor=vtkActor()
OutlineActor.SetMapper(outlineMapper)
OutlineActor.GetProperty().SetColor(0,0,0)

ren.AddActor(actor)
ren.AddActor(OutlineActor)

ren.SetActiveCamera(aCamera)
ren.ResetCamera()
aCamera.Dolly(1.5)
ren.SetBackground(1,1,1)

renWin.SetSize(1000, 600)
renWin.Render()
iren.Initialize()
iren.Start()
porter=vtkOBJExporter()
porter.SetFilePrefix("E:\\PolyDataWriter.obj")
porter.SetInput(renWin)
porter.Write()
