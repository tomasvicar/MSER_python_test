import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.filters import gaussian





class Region():
    def __init__(self,level,pixel):
        self.level = level
        self.pixel = pixel
        self.area = 0
        self.childs = []
        self.parents = []
        
        
        
    def accumulate(self):
        self.area = self.area +1
        
    def merge(self,child):
        
        self.area += child.area
        
        
        self.childs.append(child)
        child.parents.append(self)
        
        
        
        
def processStack(newPixelGreyLevel, pixel, regionStack):
    	
    
    
#     // 1. Process component on the top of the stack. The next grey-level is the minimum of
# 	// newPixelGreyLevel and the grey-level for the second component on the stack.
    
    a = 5

    while 1:
        
        region_top = regionStack[-1]
        
        
        regionStack.pop(-1)
        
        if newPixelGreyLevel < regionStack[-1].level:
            
            regionStack.append(Region(newPixelGreyLevel, pixel))


            regionStack[-1].merge(region_top);
            
            
            break
        

        regionStack[-1].merge(region_top);

        if newPixelGreyLevel <= regionStack[-1].level:
            break
        
        





img = imread('00002_PC3_img.tif')
img = gaussian(img,2)
img = - img
img = (img - np.min(img))/(np.max(img) - np.min(img))
img = np.round((img*255)).astype(np.uint8)

img = img[:200,:200]




regionStack = []

delta = 2
minArea = 10
maxArea = 500
maxVariation = 0.3
minDiversity = 0.5

shape = img.shape

accessible = np.zeros((shape),dtype=bool)

priority = 256


boundaryPixels = [[] for i in range(256)]

curPixel = np.array([50,100])
curEdge = curPixel 
curLevel = img[curPixel[0],curPixel[1]]

neighbors_pos = [np.array([-1,0]),np.array([0,-1]),np.array([1,0]),np.array([0,1])]




regionStack.append(Region(99999, curPixel))





for k  in range(10000):
    
    go_again = 1
    
    while go_again:
    
        go_again = 0
        
        # // 3. Push an empty component with current level onto the component stack.
        

        regionStack.append(Region(curLevel, curPixel))
        
        # // 4. Explore the remaining edges to the neighbors of the current pixel, in order, as follows:
    	# // For each neighbor, check if the neighbor is already accessible. If it is not, mark it as
    	# // accessible and retrieve its grey-level. If the grey-level is not lower than the current one,
    	# // push it onto the heap of boundary pixels. If on the other hand the grey-level is lower than
    	# // the current one, enter the current pixel back into the queue of boundary pixels for later
    	# // processing (with the next edge number), consider the new pixel and its grey-level and go to 3.
        
        
        for neighbor_pos in neighbors_pos:
            
            neighborPixel = curPixel + neighbor_pos
            
            if neighborPixel[0]<0 or neighborPixel[0]>=shape[0] or neighborPixel[1]<0 or neighborPixel[1]>=shape[1]:
                continue
            
            
            if accessible[neighborPixel[0],neighborPixel[1]]:
                continue
                
            
            accessible[neighborPixel[0],neighborPixel[1]] = True
            
            neighborLevel = img[neighborPixel[0],neighborPixel[1]]
                
            if (neighborLevel >= curLevel):
                boundaryPixels[neighborLevel].append(neighborPixel)
                
        
                if (neighborLevel < priority):
                    priority = neighborLevel;
            
            else:
                
                boundaryPixels[curLevel].append(curPixel)
                
                if (curLevel < priority):
                    priority = curLevel
                
            
                curPixel = neighborPixel
                curEdge = 0
                curLevel = neighborLevel
                
                go_again = 1
                break
    
            
#     // 5. Accumulate the current pixel to the component at the top of the stack (water
# 		// saturates the current pixel).
    # regionStack.back()->accumulate(x, y);
    regionStack[-1].accumulate()
    
    
    
    
    
    
#       // 6. Pop the heap of boundary pixels. If the heap is empty, we are done. If the returned
# 		// pixel is at the same grey-level as the previous, go to 4.
# 		}


        
        
    
    curPixel = boundaryPixels[priority][-1]
    curEdge = boundaryPixels[priority][-1]
    boundaryPixels[priority].pop(-1)
    	
    while len(boundaryPixels[priority]) == 0  and (priority < 255):
        priority = priority + 1
    
    
    newPixelGreyLevel  = img[curPixel[0],curPixel[1]]
    
    if (newPixelGreyLevel != curLevel):
        
        curLevel = newPixelGreyLevel
        
        
        processStack(newPixelGreyLevel, curPixel, regionStack)
        
			
# 			// 7. The returned pixel is at a higher grey-level, so we must now process
# 			// all components on the component stack until we reach the higher
# 			// grey-level. This is done with the processStack sub-routine, see below.
# 			// Then go to 4.

# 		processStack(newPixelGreyLevel, curPixel, regionStack)

  

plt.imshow(accessible)

for region in regionStack:
    
    print(region.area)








