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
from skimage.morphology import extrema
import time



min_area = 15
step = 2


img = imread('00002_PC3_img.tif')


img = gaussian(img,2)


img = (img - np.min(img))/(np.max(img) - np.min(img))
img = np.round((img*255)).astype(np.uint8)



loc_max_binar = extrema.local_maxima(img)


loc_max_l = label(loc_max_binar)


ts = np.arange(255,0,-1)
sizes =  np.zeros((np.max(loc_max_l)+1,len(ts)),dtype = np.int32)


start = time.time()

for t_num,t in enumerate(ts):


    L = label(img > t)
    for l_num in range(1,np.max(L)+1):
        
        bin_ = L == l_num
        
        u = np.unique(loc_max_l[bin_])
        u = u[u>0]
        
        size = np.sum(bin_)
        
        for uu in u:
            sizes[u,t_num] = size
        
        
        
end = time.time()
print(end - start)     
        
      
        
      
sizes = sizes[1:]       
       

min_area = 50
max_area = 500
step = 1
max_rel_instability = 0.5



start = time.time()

diffs = sizes - np.roll(sizes, step, axis=1)
    
diffs[:,:step] = 9999999 
diffs[:,-step:] = 9999999
diffs[sizes<min_area] = 9999999
diffs[sizes>max_area] = 9999999



sizes[sizes == 0] = 0.0001
diffs = diffs/sizes

result = np.zeros(img.shape)
for row_num in range(diffs.shape[0]): 

    diffs_row = diffs[row_num,:]
    
    min_pos = diffs_row.argmin()
    min_val = diffs_row.min()
    

    if min_val > max_rel_instability:
        continue
        
    
    
    t = ts[min_pos]
    
    L = label(img>t)
    
    stable_reg = L == L[loc_max_l==row_num+1][0]
    
    # plt.figure(figsize=(15,15))
    # plt.imshow(stable_reg)
    # plt.show()
    
    
    result = result + stable_reg
    
    
    
    
    
end = time.time()
print(end - start)     
        




        
plt.figure(figsize=(15,15))
plt.imshow(result)
plt.show()




