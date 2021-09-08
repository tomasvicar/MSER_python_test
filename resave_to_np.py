import numpy as np
import imagej
ij = imagej.init()





img_imagej = ij.io().open(r"C:\Users\tomas\Desktop\test_mser\0001\01.ics")

img_xarray = ij.py.from_java(img_imagej)

img_numpy = img_xarray.data


np.save(r"C:\Users\tomas\Desktop\test_mser\0001\01.npy",img_numpy)



