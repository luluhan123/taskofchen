from pyevtk.hl import imageToVTK
import numpy as np
import dicom
import glob as gb
import os
from scipy.misc import imresize
from scipy.ndimage import zoom
import tifffile
import matplotlib.pyplot as pp
import subprocess

CWDst = os.getcwd()

def GenVTK():
    Names=sorted(gb.glob('IM*'))
    XScale, YScale, ZScale =100,100, 25 #%
    Zsize=150#len(Names)
    Idx = 0
    if Zsize==0:
        Zsize=len(Names)
    for kat in Names[0:Zsize]:
        DI = dicom.read_file(kat)
        Pix = DI.pixel_array
        Pix=zoom(Pix, ZScale*0.01)
        Pix2 = Pix
        Xsize, Ysize = Pix2.shape
        XPart, YPart = Pix.shape[0]*XScale/100, Pix.shape[1]*YScale/100
        #patata
        if kat == Names[0]:
            ###allocate Volume
            Vol=np.zeros([XPart-1, YPart-1, Zsize])
        Vol[:,:,Idx]=Pix2[1:XPart,1:YPart]
        Idx+=1
    #patata
    imageToVTK("./VTKimage", cellData = {"Scattering" : Vol} )

Folders=subprocess.check_output(["find","-name","*_OCT"]).split('\n')
pp.ion()
for katF in Folders:
    os.chdir(katF)
    GenVTK()
    os.chdir(CWDst)