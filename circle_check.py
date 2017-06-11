import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread(r'C:\Users\Jale Brunger\Desktop\Physics77project\diamond.jpg', cv2.IMREAD_GRAYSCALE)




def CenterMass(pic):
    x_diff=np.diff(pic)
   
    outer_y = []        
    outer_x = []  
    bot_outer_y = []        
    bot_outer_x = []  
     
    
    for x in range(0, x_diff.shape[1]):
        
        edgeheight=[]
        for y in range(0, x_diff.shape[0]):
            if x_diff[y,x]>100:
                edgeheight.append(y)
        if len(edgeheight)==0:
            continue
        elif len(edgeheight)==1:
            outer_y.append(edgeheight[0])
            outer_x.append(x)
        else:
            outer_y.append(edgeheight[0])
            bot_outer_y.append(edgeheight[len(edgeheight)-1])
            outer_x.append(x)
            bot_outer_x.append(x)
    for i in (bot_outer_y[::-1]):
        outer_y.append(i)
        
    for i in (bot_outer_x[::-1]):
        outer_x.append(i)  
    
    centerx= sum(outer_x)/len(outer_x)
    centery=sum(outer_y)/len(outer_y)
    return np.array([centery, centerx])
    
    
    
    
def CircleCheck(pic):      # returns the standard deviation of all radii from a center point on the shape in 'img'
    
    x_diff=np.diff(pic)    # add param 'axis=0' for differentiating y instead of x
                        
                        
    outer_y = []        #  Lists to hold x and y positions of outer edges
    outer_x = []        #
    
    for x in range(0, x_diff.shape[0]-1):
        edgeheight=[]
        
        for y in range(0, x_diff.shape[1]-1):
            if x_diff[x,y]>50:
                edgeheight.append(y)
        if len(edgeheight)==0:
            continue
        elif len(edgeheight)==1:
            outer_y.append(edgeheight[0])
            outer_x.append(x)
        else:
            outer_y.append(edgeheight[0])
            outer_y.append(edgeheight[len(edgeheight)-1])
            outer_x.append(x)
            outer_x.append(x)

    central_x_coord = CenterMass(img)[0]
    central_y_coord = CenterMass(img)[1]
    
    distances = []
    for i in range(len(outer_x)):
        delta_x = outer_x[i] - central_x_coord
        delta_y = outer_y[i] - central_y_coord
        radius = (delta_x**2+delta_y**2)**0.5
        distances.append(radius)

    array_dist = np.array(distances)
    
    stand = np.std(array_dist)
    return(stand)

print('standard deviation of radii:', CircleCheck(img), 'pixels')
print('CM:', CenterMass(img) )
print(img.shape)
cv2.imshow('circle', cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5))
cv2.waitKey(0)
cv2.destroyAllWindows