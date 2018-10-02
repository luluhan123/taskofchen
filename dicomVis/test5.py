import SimpleITK as sitk
import numpy as np
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames('P01dicom')
reader.SetFileNames(dicom_names)
image = reader.Execute()

image_array = sitk.GetArrayFromImage(image) # z, y, x
origin = image.GetOrigin() # x, y, z
spacing = image.GetSpacing() # x, y, z

# print(image)

print(image_array.shape)
