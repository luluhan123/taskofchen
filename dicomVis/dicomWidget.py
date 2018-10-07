import SimpleITK as sitk
import vtk
import pydicom
import sys
from PyQt5.QtWidgets import QApplication
from scipy.stats.mstats import mquantiles

from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vtk.util.vtkConstants import *

class dicomWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        # self.renWin = vtk.vtkRenderWindow()
        # self.renWin.AddRenderer(self.ren)
        # self.renWin.SetSize(600, 600)
        self.renWin = self.vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.renWin.SetSize(600, 600)
        # self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.renWin.GetInteractor()

        self.reader = sitk.ImageSeriesReader()
        self.dicom_names = self.reader.GetGDCMSeriesFileNames('P01dicom')
        self.reader.SetFileNames(self.dicom_names)
        self.image = self.reader.Execute()
        self.information = self.getInformation()

        self.data = sitk.GetArrayFromImage(self.image)  # z, y, x

        q = mquantiles(self.data.flatten(), [0.7, 0.98])
        q[0] = max(q[0], 1)
        q[1] = max(q[1], 1)
        tf = [[0, 0, 0, 0, 0], [q[0], 0, 0, 0, 0], [q[1], 1, 1, 1, 0.5], [self.data.max(), 1, 1, 1, 1]]

        actor_list = self.volumeRender(self.data, tf, self.image.GetSpacing())

        for a in actor_list:
            # assign actor to the renderer
            self.ren.AddActor(a)

        self.renWin.Render()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()


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

    def numpy2VTK(self, img, spacing=[1.0, 1.0, 1.0]):
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

    def volumeRender(self, img, tf=[], spacing=[1.0, 1.0, 1.0]):
        importer = self.numpy2VTK(img, spacing)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = dicomWidget()

    sys.exit(app.exec_())