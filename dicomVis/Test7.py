import SimpleITK as sitk
from PIL import Image
import pydicom
import numpy as np
import cv2

filename = 'sample'

def loadFile(filename):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames('P01dicom')
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    image_array = sitk.GetArrayFromImage(image)
    frame_num, width, height = image_array.shape
    return image_array, frame_num, width, height

def loadFileInformation(filename):
    information = {}
    ds = pydicom.read_file(filename)
    information['PatientID'] = ds.PatientID
    information['PatientName'] = ds.PatientName
    information['PatientBirthDate'] = ds.PatientBirthDate
    information['PatientSex'] = ds.PatientSex
    information['StudyID'] = ds.StudyID
    information['StudyDate'] = ds.StudyDate
    information['StudyTime'] = ds.StudyTime
    information['InstitutionName'] = ds.InstitutionName
    information['Manufacturer'] = ds.Manufacturer
    information['NumberOfFrames'] = ds.NumberOfFrames
    return information

def showImage(img_array, frame_num = 0):
    img_bitmap = Image.fromarray(img_array[frame_num])
    return img_bitmap

def limitedEqualize(img_array, limit = 4.0):
   img_array_list = []
   for img in img_array:
       clahe = cv2.createCLAHE(clipLimit = limit, tileGridSize = (8,8))
       img_array_list.append(clahe.apply(img))
   img_array_limited_equalized = np.array(img_array_list)
   return img_array_limited_equalized


def writeVideo(img_array):
    frame_num, width, height = img_array.shape
    filename_output = filename.split('.')[0] + '.avi'
    video = cv2.VideoWriter(filename_output, -1, 16, (width, height))
    for img in img_array:
        video.write(img)
    video.release()

image_array, frame_num, width, height = loadFile(filename)
print(image_array)
print(frame_num)
writeVideo(image_array)