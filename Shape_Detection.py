import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('C:/Users/Jale Brunger/Downloads/shapeellipse5.jpg', cv2.IMREAD_GRAYSCALE)

#Distance function that will be used later, distance is found with distance formula

def Distance(x1,y1,x2,y2):
    D = ((x1-x2)**2+(y1-y2)**2)**0.5
    return D

#Center of Mass function to find the center of the shape being analyzed
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
    

#Now to check if shape is circle and/or ellipse


def StraightCheck(pic, theta_eps, thresh):
  # create a list of pixles on the edge of the shape          #############################################################
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
        
    ###################################################################################################################
        
    img_diag = np.sqrt( (img_diff.shape[0])**2 + (img_diff.shape[1])**2 )   ## maximum radius that any line in the image could be parametrized by is the length of the diagonnal of the image
    hough =  np.zeros( ( int(img_diag), int(np.pi*(1/theta_eps)) ) )         ## create an empty array where rows are radii and columns are angles each point is iterated through
    
    for xy in range(0, len(outer_x)-1 ):                                      ## iterate through each line going through each point determined by the desired accuracy for theta, "vote" up the (R,Theta) 
                                                                               ## coordinate through each possible line.  The lines that have enough "votes" beyond a threshold are appended to the final list to be returned by the function
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




def EllipseCheck(pic):
    
    #creating array of edges
    
    x_diff_vert = np.diff(img, axis = 0) #differentiating left to right
    x_diff_v_shape = x_diff_vert.shape
    x_diff_hori = np.diff(img, axis = 1) #differentiating top to bottom
    x_diff_h_shape = x_diff_hori.shape
    #add together to get total array of edges
    x_diff = x_diff_vert[0:x_diff_v_shape[0],0:x_diff_h_shape[1]] + x_diff_hori[0:x_diff_v_shape[0],0:x_diff_h_shape[1]]
                        
                        
    outer_y = []        #  Lists to hold x and y positions of outer edges
    outer_x = []
    
    #now iterate through every single pixel to see where there are significant edges and find the outermost edges for each column
    
    for x in range(0, x_diff.shape[1]): #for every column
        edgeheight=[]
        
        for y in range(0, x_diff.shape[0]): #for every row in the column we're iterating through
            if x_diff[y,x]>100: #if differentiation detects a value greater than 100, it's an edge
                edgeheight.append(y)
        if len(edgeheight)==0: #if list of edges is 0, move on
            continue
        elif len(edgeheight)==1: #if list of edges is 1, simply append that cooardinate to the list of outer edges
            outer_y.append(edgeheight[0])
            outer_x.append(x)
        else:
          
            #if list has more than 1 edge, find uppermost and lowermost edges and add them to list
            #of outer edges
            
            outer_y.append(edgeheight[0]) 
            outer_y.append(edgeheight[len(edgeheight)-1])
            outer_x.append(x)
            outer_x.append(x)

    central_x_coord = CenterMass(img)[0] #get coordinates for center of mass
    central_y_coord = CenterMass(img)[1]
    
    distances = []
    
    #for each outer edge coordinate
    
    for i in range(len(outer_x)):
        delta_y = outer_y[i] - central_y_coord #find y distance from center of mass to outer edge y component
        delta_x = outer_x[i] - central_x_coord #do the same for the x
        radius = (delta_x**2 + delta_y**2)**0.5 #Use Pythagorean theorem to get Distance
        distances.append(radius) #create list of Distances between outer edges and the center of mass

    maxim = max(distances) #find maximum and minimum distances
    minim = min(distances)
    
    max_index = distances.index(maxim) 
    min_index = distances.index(minim)
    
    y_coord_major = outer_y[max_index] #the largest distance denotes the coordinates of the major axis on the assumed ellipse
    x_coord_major = outer_x[max_index]
    
    y_coord_minor = outer_y[min_index] #the smallest distance denotes the coordinates of the minor axis
    x_coord_minor = outer_x[min_index]
    
    #Use property (Foci distance from center)**2 = major radius**2 - minor radius**2
    #Basically c**2 = a**2 - b**2
    
    foci_dist = (maxim**2 - minim**2)**0.5 
    
    #find slope between major axis coordinate and center of mass
    
    slope = (central_y_coord - y_coord_major)/(central_x_coord - x_coord_major)
    
    #after algebra, the coordinates of the foci can be determined like so
    
    foci_x_low = central_x_coord - foci_dist*(1+slope**2)**-0.5
    foci_y_low = central_y_coord - slope*foci_dist*(1+slope**2)**-0.5
    foci_x_high = central_x_coord + foci_dist*(1+slope**2)**-0.5
    foci_y_high = central_y_coord + slope*foci_dist*(1+slope**2)**-0.5
    
    constant_dist = []
    
    #Geometric property with ellipses states that at any point on the edge of the ellipse, the sum of its distances to each foci 
    #is always a constant value: twice its major axis radius.  This will test whether or not that is true.
    
    for i in range(0,len(outer_y)):
        distance_foci_low = Distance(foci_x_low,foci_y_low,outer_x[i],outer_y[i]) #find distance between edge and lower foci
        distance_foci_high = Distance(foci_x_high,foci_y_high,outer_x[i],outer_y[i]) #find distance between edge and upper foci
        total_d = distance_foci_low + distance_foci_high #find summation of distances
        constant_dist.append(total_d) #append to list of those summations
        
    constant_dist_array = np.array(constant_dist)
    
    #find standard deviation.  If standard deviation is low, it is most likely an ellipse
    
    std_constant = np.std(constant_dist_array) 
    
    #Using statistical analysis, we determined the cutoff value for the standard deviation of that list of summations is 19.36.
    #So if standard deviation of list for a given shape is less than 19.36 then it is fair to assume ellipse-like.
    
    if std_constant < 19.36:
        
        #Now to check if it is circle-like

        array_dist = np.array(distances)
    
        stand = np.std(array_dist) #Find standard deviation of distances from edges to center of mass

        #Once again, we determined the cutoff value to be 4.012 for the standard deviation of the list of distances from the 
        #edges to the center of mass.  If the shape is like a circle, the standard deviation should be relatively low.
        
        if stand < 4.012:
            return("The shape is a circle")
        else:
            return("The shape is not a circle, but is an ellipse")

    #If not ellipse-like, the shape is not a circle either since a circle is a type of ellipse so this shape is not an ellipse.

    else:
        return("Not ellipse or circle shaped",std_constant)
    
    
    
#############################################################################################
thetaeps= .001
thresh = 50
straight = (StraightCheck(img, thetaeps, thresh))


if len(straight[0])>0:
    print('straight lines > ', thresh, ' pixels detected' )
    print('Not ellipse or circle shaped')

elif len(straight[0])==0:
    print('no straight lines > ', thresh,' pixels detected')
    
    print(EllipseCheck(img))