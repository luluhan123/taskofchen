import SimpleITK as sitk
import vtk
import pydicom
import PyQt5
import numpy as np
from scipy.stats.mstats import mquantiles

from vtk.util.vtkConstants import *

class dicomShow():
    def __init__(self):
        self.reader = sitk.ImageSeriesReader()
        self.dicom_names = self.reader.GetGDCMSeriesFileNames('P01dicom')
        self.reader.SetFileNames(self.dicom_names)
        self.image = self.reader.Execute()
        self.information = self.getInformation()

        self.data = sitk.GetArrayFromImage(self.image)  # z, y, x

    def getInformation(self):
        information = {}
        for var in self.dicom_names:
            ds = pydicom.read_file(var)
            current_information = {}
            current_information['PatientID'] = ds.PatientID
            current_information['PatientName'] = ds.PatientName
            current_information['PatientBirthDate'] = ds.PatientBirthDate
            current_information['PatientSex'] = ds.PatientSex
            current_information['StudyID'] = ds.StudyID
            current_information['StudyDate'] = ds.StudyDate
            current_information['StudyTime'] = ds.StudyTime
            current_information['InstitutionName'] = ds.InstitutionName
            current_information['Manufacturer'] = ds.Manufacturer
            if(not information):
                information = current_information

            if(information != current_information):
                information = {}
                break
        return information

    def getdate(self):
        return self.information['StudyDate']

    def Show(self):
        q = mquantiles(self.data.flatten(), [0.7, 0.98])
        q[0] = max(q[0], 1)
        q[1] = max(q[1], 1)
        tf = [[0, 0, 0, 0, 0], [q[0], 0, 0, 0, 0], [q[1], 1, 1, 1, 0.5], [self.data.max(), 1, 1, 1, 1]]

        actor_list = self.volumeRender(self.data, tf, self.image.GetSpacing())

        self.vtk_basic(actor_list)

    def numpy2VTK(self, img, spacing=[1.0, 1.0, 1.0]):
        importer = vtk.vtkImageImport()
        img_data = self.astype('uint8')
        img_string = img_data.tostring()  # type short
        dim = self.shape

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

    def volumeRender(self, img, tf=[], spacing=[1.0, 1.0, 1.0]):
        importer = dicomShow.numpy2VTK(img, spacing)

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
        volProperty = vtk.vtkVolumeProperty()
        volProperty.SetColor(color_tf)
        volProperty.SetScalarOpacity(opacity_tf)
        volProperty.ShadeOn()
        volProperty.SetInterpolationTypeToLinear()

        vol = vtk.vtkVolume()
        vol.SetMapper(volMapper)
        vol.SetProperty(volProperty)

        return [vol]

    def vtk_basic(self, actors):
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


if __name__ == '__main__':
    dicomS = dicomShow()
    if(dicomS.information):
        print(dicomS.getdate())