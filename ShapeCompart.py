import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread(r'C:\Users\Jale Brunger\Desktop\Physics77project\diamond.jpg', 0)


### marked for deletion from project itinerary #########################


def ShapeCompart(pic):
    
    xmins=[]
    ymins=[]
    xmaxs=[]
    ymaxs=[]
    
    x_diff=np.diff(pic)
    for y in range(0, len(x_diff.shape(1)-1)):
        a=0
        while a<6:
           edge_xs=[] 
           for x in range(0, len(x_diff.shape[0]-1)):
               if x_diff[x,y]>50:
                    edge_xs.append(x)
                    a=1
               else:
                   continue
           if len(edge_xs)==0 and a==1:
               a=+1
       xmins.append(min(edge_xs))
       xmaxs.append(max(edge_xs))
       
    y_diff=np.diff(pic, axis=0)
    for x in range(0, len(x_diff.shape[0]-1)):
        edge_ys=[]
        for y in range(0, len(x_diff.shape(1)-1)):
            if y_diff[x,y]>50:
                edge_ys.append(y)
        ymins.append(min(edge_ys))
        ymaxs.append(max(edge_ys))
       
    
    truexmin=min(xmins)
    trueymin=min(ymins)
    truexmax=max(xmaxs)
    trueymax=max(ymaxs)