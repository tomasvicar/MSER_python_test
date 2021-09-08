

import numpy as np
from skimage.segmentation import watershed
from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.filters import gaussian
from scipy.signal import convolve2d

from scipy.ndimage.morphology import grey_dilation
from skimage.morphology import h_maxima
from skimage.measure import regionprops
from skimage.measure import label
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.morphology import remove_small_objects





img = imread('00002_PC3_img.tif')


img = gaussian(img,2)



objects = watershed(-img,watershed_line=True)
lines = objects==0


positions = [[0,0],[0,2],[2,0],[2,2]]
pos_imgs = np.zeros([lines.shape[0],lines.shape[1],len(positions)],dtype=np.int32)
for pos_ind,pos in enumerate(positions):
    
    mask = np.zeros((3,3),dtype=np.int32)
    mask[pos[0],pos[1]] = 1
    
    pos_imgs = convolve2d(objects,mask,'same')
    
    


# for k in range(500):
    
values =  img[lines]
inds = np.argwhere(lines)


max_pos = values.argmax()


    
    
    










