import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter as gaussian
from skimage.morphology import local_maxima
# from skimage.measure import label
from scipy.ndimage import label
import time
from skimage.feature import peak_local_max
from skimage.measure import regionprops


img = np.load(r"..\0001\01.npy")
img = img.transpose((1,2,0))
img = img[50:-50,50:-50,:]
img = gaussian(img,1)


# img = img[300:600,500:800,:]




img = (img - np.min(img))/(np.max(img) - np.min(img))
img = np.round((img*255)).astype(np.uint8)


plt.figure(figsize=(15,15))
plt.imshow(img[:,:,25])
plt.show()




min_dist = 5
min_value = 50
loc_max = peak_local_max(img,min_distance=min_dist,threshold_abs=min_value)





min_area = 100
max_area = 2000
delta = 2




loc_max_bin = np.zeros(img.shape,dtype=bool)

num_of_max = loc_max.shape[0]
loc_max_bin[loc_max[:,0],loc_max[:,1],loc_max[:,2]] = np.arange(1,num_of_max+1)


loc_max_l, num_of_max = label(loc_max_bin)

ts = np.arange(255,0,-delta)
sizes =  np.zeros((num_of_max,len(ts)),dtype = np.int32)


for t_num,t in enumerate(ts):

    print(t_num)

    L,drop = label(img > t)
    props = regionprops(L)
    object_nums = L[loc_max[:,0],loc_max[:,1],loc_max[:,2]]
    
    
    for l_num in range(num_of_max):
        
        
        object_num = object_nums[l_num]
        
        
        if object_num!=0:

            
            sizes[l_num,t_num] = props[object_num-1].area
        
        
        
        
        
        
  
step = 1
max_rel_instability = 1.0
diffs = sizes - np.roll(sizes, step, axis=1)
    
diffs[:,:step] = np.Inf 
diffs[:,-step:] = np.Inf 
diffs[sizes<min_area] = np.Inf 
diffs[sizes>max_area] = np.Inf 


    

sizes[sizes == 0] = 0.0001
diffs = diffs/sizes

result = np.zeros(img.shape)
region_id = 0
for row_num in range(diffs.shape[0]): 

    diffs_row = diffs[row_num,:]
    
    min_pos = diffs_row.argmin()
    min_val = diffs_row.min()
    

    if min_val > max_rel_instability:
        continue
        
    
    
    t = ts[min_pos]
    
    L,drop = label(img>t)
    
    stable_reg = L == L[loc_max[row_num,0],loc_max[row_num,1],loc_max[row_num,2]]
    
    
    
    plt.figure(figsize=(15,15))
    plt.imshow(np.max(stable_reg,axis=2))
    plt.show()
    
    
    result[stable_reg] = region_id
    region_id = region_id +1
    
    
    

plt.figure(figsize=(15,15))
plt.imshow(result[:,:,25])
plt.show()





