import SimpleITK as sitk
import vtk
import numpy as np

from vtk.util.vtkConstants import *


def numpy2VTK(img, spacing=[1.0, 1.0, 1.0]):
    importer = vtk.vtkImageImport()

    img_data = img.astype('uint8')
    img_string = img_data.tostring()  # type short
    dim = img.shape

    importer.CopyImportVoidPointer(img_string, len(img_string))
    importer.SetDataScalarType(VTK_UNSIGNED_CHAR)
    importer.SetNumberOfScalarComponents(1)

    extent = importer.GetDataExtent()
    importer.SetDataExtent(extent[0], extent[0] + dim[2] - 1,
                           extent[2], extent[2] + dim[1] - 1,
                           extent[4], extent[4] + dim[0] - 1)
    importer.SetWholeExtent(extent[0], extent[0] + dim[2] - 1,
                            extent[2], extent[2] + dim[1] - 1,
                            extent[4], extent[4] + dim[0] - 1)

    importer.SetDataSpacing(spacing[0], spacing[1], spacing[2])
    importer.SetDataOrigin(0, 0, 0)

    return importer


def volumeRender(img, tf=[], spacing=[1.0, 1.0, 1.0]):
    importer = numpy2VTK(img, spacing)

    # Transfer Functions
    opacity_tf = vtk.vtkPiecewiseFunction()
    color_tf = vtk.vtkColorTransferFunction()

    if len(tf) == 0:
        tf.append([img.min(), 0, 0, 0, 0])
        tf.append([img.max(), 1, 1, 1, 1])

    for p in tf:
        color_tf.AddRGBPoint(p[0], p[1], p[2], p[3])
        opacity_tf.AddPoint(p[0], p[4])

    # working on the GPU
    volMapper = vtk.vtkGPUVolumeRayCastMapper()
    volMapper.SetInputConnection(importer.GetOutputPort())

    # The property describes how the data will look
    volProperty =  vtk.vtkVolumeProperty()
    volProperty.SetColor(color_tf)
    volProperty.SetScalarOpacity(opacity_tf)
    volProperty.ShadeOn()
    volProperty.SetInterpolationTypeToLinear()


    vol = vtk.vtkVolume()
    vol.SetMapper(volMapper)
    vol.SetProperty(volProperty)

    return [vol]


def vtk_basic(actors):
    # create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(600, 600)
    # ren.SetBackground( 1, 1, 1)

    # create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    for a in actors:
        # assign actor to the renderer
        ren.AddActor(a)

    # render
    renWin.Render()

    # enable user interface interactor
    iren.Initialize()
    iren.Start()


#####

reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames('P01dicom')
reader.SetFileNames(dicom_names)
image = reader.Execute()

data = sitk.GetArrayFromImage(image) # z, y, x

from scipy.stats.mstats import mquantiles

q = mquantiles(data.flatten(), [0.7, 0.98])
q[0] = max(q[0], 1)
q[1] = max(q[1], 1)
tf = [[0, 0, 0, 0, 0], [q[0], 0, 0, 0, 0], [q[1], 1, 1, 1, 0.5], [data.max(), 1, 1, 1, 1]]

actor_list = volumeRender(data, tf=tf, spacing=image.GetSpacing())

vtk_basic(actor_list)
