


import cv2

import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.filters import gaussian




img = imread('00002_PC3_img.tif')

img = gaussian(img,2)
img = (img - np.max(img))/(np.max(img) - np.min(img))
img = (img*255).astype(np.uint8)


vis = img.copy()


mser = cv2.MSER()
regions = mser.detect(img,None)

hulls = [cv2.convexHull(np.array(p.pt).reshape(-1, 1, 2)).astype(np.float32) for p in regions]

cv2.polylines(vis, hulls, 1, (0, 255, 0))
cv2.imshow('img', vis)


plt.imshow(vis)


