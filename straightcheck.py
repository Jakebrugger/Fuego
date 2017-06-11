import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('C:/Users/Jale Brunger/Downloads/shapcircle5', cv2.IMREAD_GRAYSCALE)


def StraightCheck(pic, theta_eps, thresh):
    
    x_diff_vert = np.diff(img, axis = 0)
    x_diff_v_shape = x_diff_vert.shape
    x_diff_hori = np.diff(img, axis = 1)
    x_diff_h_shape = x_diff_hori.shape
    img_diff = x_diff_vert[0:x_diff_v_shape[0],0:x_diff_h_shape[1]] + x_diff_hori[0:x_diff_v_shape[0],0:x_diff_h_shape[1]]
    
    outer_y = []        
    outer_x = []  
    bot_outer_y = []        
    bot_outer_x = []  
    
    for x in range(0, img_diff.shape[1]):
        edgeheight=[]

        for y in range(0, img_diff.shape[0]):
            if img_diff[y,x]>100:
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
        
    img_diag = np.sqrt( (img_diff.shape[0])**2 + (img_diff.shape[1])**2 )
    hough =  np.zeros( ( int(img_diag), int(np.pi*(1/theta_eps)) ) )
    
    for xy in range(0, len(outer_x)-1 ):
        for i in range(hough.shape[1]):
            x= outer_x[xy]
            y= outer_y[xy]
            thet = i * theta_eps
            r = int(x*np.cos(thet) + y*np.sin(thet))
            hough[r , i] = hough[r , i] + 1
                 
    R = []
    Thet = []

    for thet in range(0, hough.shape[1]):
        for r in range(0, hough.shape[0]):
            if hough[r, thet]> thresh:
                R.append(r)
                Thet.append(thet)
            else:
                continue
    newR = []
    newThet = []
    
###################################################   unfinished block to filter out simlar lines in the returned array of radii and angles, and therefore detect locations of distinct lines/ angles to identify quadralaterals
    for j in range(0, len(R)-1):
        
        if len(newR)==0:
            newR.append(R[j])
            newThet.append(Thet[j])
            continue
        
        elif len(newR)==1:
            check=0
            if abs(R[j]-newR[0])<15 and abs(Thet[j]-newThet[0])<15 :
                check = check + 1
                
            if check==0:
                newR.append(R[j])
                newThet.append(Thet[j])
###################################################                
    return(R, Thet)


thetaeps= .001
thresh = 50
straight = (StraightCheck(img, thetaeps, thresh))

if len(straight[0])==0:
    print('no straight lines > ', thresh,' pixels detected')
elif len(straight[0])>0:
    print('straight lines > ', thresh, ' pixels detected' )
    
    
    
print(len(straight[0]))
print(straight)
#
x_diff_vert = np.diff(img)
x_diff_v_shape = x_diff_vert.shape
x_diff_hori = np.diff(img, axis = 1)
x_diff_h_shape = x_diff_hori.shape
img_diff = x_diff_vert[0:x_diff_v_shape[0],0:x_diff_h_shape[1]] + x_diff_hori[0:x_diff_v_shape[0],0:x_diff_h_shape[1]]
#

cv2.imshow('Circle', img_diff)
cv2.waitKey(0)
cv2.destroyAllWindows

x_val=img.shape[1]

        
