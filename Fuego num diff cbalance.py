from cv2 import imread
import numpy as np
import matplotlib.pyplot as plt

img=imread('C:\Users\Jale Brunger\Desktop\Lab projects\colorbalance\cbalance5.jpg')
txt=open('C:\Users\Jale Brunger\Desktop\Lab projects\colorbalance\cbalance5.txt', 'w')
x=np.array([291,1842,1053,1374,2250,2496,2163,2085])
y=np.array([855,984,1926,2445,1743,1383,2475,3261])
width=np.array([1548,408,1440,858,477,933,321,516])
height=np.array([486,114,381,663,885,771,816,204])
xres=3715
yres=4007


for u in range(len(x)):       #iterate through cells
    pxly= []      #create array of y values of pixel
    pxlx= []      #create array of x values of pixel     
    for w in range(0,width[u]):       #iterate through x values in cell
        blues = []               #create lists for rgb values of each vertical column         
        reds = []                ####
        greens = []               ####
        for h in range(0, height[u]):        #iterate through y values in cell
            pxly.append(y[u]+h)              #set y value of iterated pixel
            pxlx.append(x[u]+w)              #set x value of iterated pixel
            blues.append(img[pxly[h],pxlx[h],0])
            greens.append(img[pxly[h],pxlx[h],1])
            reds.append(img[pxly[h],pxlx[h],2])
        bluemax=max(abs(np.diff(np.asarray(blues, dtype= int))))
        redmax=max(abs(np.diff(np.asarray(reds, dtype=int))))
        greenmax=max(abs(np.diff(np.asarray(greens, dtype=int))))
        txt.write(str(bluemax)+'\n')
        txt.write(str(redmax)+ '\n')
        txt.write(str(greenmax)+ '\n')
        txt.write(''+ '\n')
        txt.write(''+ '\n')
    del(pxly)
    del(pxlx)

plt.figure(1)
plt.ylim([0, yres])
plt.xlim([0, xres])
 
txt.close


print('done')            
        
        
         
        

#pxl=img[y,x]
#blue=pxl[0]
#green=pxl[1]
#red=pxl[2]
#xyhw=[402,301,16,38,397,265,12,33,392,320,28,88,387,409,11,94]
#center_list_names=['smoke1','smoke2','smoke3','smoke4']  
#loop=0
#while loop<2:
#    for i in range(0,(len(xyhw)/4)):
#        centerx=xyhw[4*i] 
#        centery=xyhw[4*i+1]
#        width=xyhw[4*i+2]
#        height=xyhw[4*i+3]
#        red=0
#        blue=0
#        green=0
#        for x in range(centerx,centerx+width):
#            if x>1920:
#                break
#            for y in range(centery,centery+height):
#                if y>1080:
#                    break
#                pxl=img[y,x]
#                blue=blue+pxl[0]
#                green=green+pxl[1]
#                red=red+pxl[2]
#        red=float(red/(width*height))
#        green=float(green/(width*height))
#        blue=float(blue/(width*height))
#        blue_percent=float(((blue)/(blue+red+green))*100)
#        red_percent=float((red)/(red+blue+green)*100)
#        green_percent=float((green)/(red+blue+green)*100)
#        luminance=blue
#        if loop==0:
#            print str(center_list_names[i])+'('+str(centerx)+','+str(centery)+') '+' (A: '+str(width*height)+'), '
#        if loop==1:
#            print 'red= '+str(red_percent)+' blue= '+str(blue_percent)+' green= '+str(green_percent)
#        if loop==2:
#            print 
#    loop=loop+1
#    print ' '  