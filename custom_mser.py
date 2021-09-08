

import numpy as np
from skimage.segmentation import watershed
from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.filters import gaussian


from scipy.ndimage.morphology import grey_dilation
from skimage.morphology import h_maxima
from skimage.measure import regionprops
from skimage.measure import label
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.morphology import remove_small_objects





img = imread('00002_PC3_img.tif')


img = gaussian(img,2)



min_dist= 5
min_value = 0.2
min_h = 0.05
min_size = 5



img_pos = img


p1=peak_local_max(img_pos,min_distance=min_dist,threshold_abs=min_value)
p2=h_maxima(img_pos,min_h)
final=np.zeros(img_pos.shape)
for p in p1:
    final[int(p[0]),int(p[1])]=p2[int(p[0]),int(p[1])]





seeds=label(final>0,connectivity=1)



img = (img - np.max(img))/(np.max(img) - np.min(img))


img = (img*255).astype(np.uint8)


min_area = 15
step = 2

objects = watershed(-img,markers=seeds,mask=img>np.median(img),watershed_line=True)>0

objects= remove_small_objects(objects,min_area)


seeds = objects*seeds


seeds_L = label(seeds)
nums_obj = np.max(seeds_L)


for obj_num in range(1,nums_obj+1):
    
    object_bin = objects == obj_num
    object_vals = img[object_bin]

        
    object_hist = 
    




plt.figure(figsize=(20,20))
plt.imshow(img)
plt.show()

plt.figure(figsize=(20,20))
plt.imshow(seeds)
plt.show()












