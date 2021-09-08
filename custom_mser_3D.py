import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter as gaussian
from skimage.morphology import local_maxima
from skimage.measure import label
import time

img = np.load(r"C:\Users\tomas\Desktop\test_mser\0001\01.npy")
img = img.transpose((1,2,0))
img = img[50:-50,50:-50,:]
img = gaussian(img,2)


p95= np.percentile(img, 95)
img[img < p95] = p95

img = (img - np.min(img))/(np.max(img) - np.min(img))
img = np.round((img*255)).astype(np.uint8)


plt.figure(figsize=(15,15))
plt.imshow(img[:,:,25])
plt.show()




min_area = 200
max_area = 5000
step = 2
max_rel_instability = 0.5

loc_max_binar = local_maxima(img)




loc_max_l = label(loc_max_binar)


ts = np.arange(255,0,-1)
sizes =  np.zeros((np.max(loc_max_l)+1,len(ts)),dtype = np.int32)


plt.figure(figsize=(15,15))
plt.imshow(loc_max_l[:,:,25])
plt.show()



start = time.time()

for t_num,t in enumerate(ts):

    print(t_num)

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



