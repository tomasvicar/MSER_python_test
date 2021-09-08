

# conda create -n pyimagej -c conda-forge pyimagej openjdk=8
# conda activate pyimagej



import imagej
ij = imagej.init()





img_imagej = ij.io().open(r"C:\Users\tomas\Desktop\test_mser\0001\01.ics")

img_xarray = ij.py.from_java(img_imagej)

img_numpy = img_xarray.data











