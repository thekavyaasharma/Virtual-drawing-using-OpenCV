import numpy as np # for numerical ops 
import cv2 # main mdoule 
from collections import deque # double ended queue used to store points to draw efficiently

# create track bars for color adjustment -> helper function
def setValues(x):
    print("") #placeholder function for track bar. it is called whenever TB changes

# create TB for color adjustment
cv2.namedWindow("Color detectors") # trackbar window name -> create 6 TB

# upper hue,saturation , value same for lower (HSV-> to detect marker color) by default is blue
cv2.createTrackbar("Upper Hue","Color detectors",153,180, setValues)
cv2.createTrackbar("Upper Saturation","Color detectors",255,255, setValues)
cv2.createTrackbar("Upper Value","Color detectors",255,255, setValues)

cv2.createTrackbar("Lower Hue","Color detectors",64,180, setValues)
cv2.createTrackbar("Lower Saturation","Color detectors",72,255, setValues)
cv2.createTrackbar("Lower Value","Color detectors",49,255, setValues)

# create color buffer using deque -> blue green red yellow 
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)] 
""" list of deque to store drawing points fro BGRY marker each deque has max size 
of 1024 to limit memory usage . this array store the points(co ordinates) which is 
drawn with specific color"""

blue_index = 0  # these vars(as pointers to current deque in respective colors array) 
green_index = 0
red_index = 0
yellow_index = 0 

# kernel for morphological operations 
kernel = np.ones((5,5),np.uint8) # unsigned 8 bit integers(0-255)


# define colors 
colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)] # blue green red yellow 
colorIndex = 0

# canvas 
paintWindow = np.zeros((471,636,3)) + 255 # -> 3 color channel 
# np.zeroes -> black image , +255 gives white image 

paintWindow = cv2.rectangle(paintWindow, (40,1),(140,65),(0,0,0),2) # clear button
cv2.putText(paintWindow, "CLEAR", (49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2,cv2.LINE_AA)

paintWindow = cv2.rectangle(paintWindow, (160,1),(255,65),colors[0],-1) # blue color button 
paintWindow = cv2.rectangle(paintWindow, (275,1),(370,65),colors[1],-1)
paintWindow = cv2.rectangle(paintWindow, (390,1),(485,65),colors[2],-1)
paintWindow = cv2.rectangle(paintWindow, (505,1),(600,65),colors[3],-1)

# cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read() # read all frames in the cap variable return two result bool val , actual img frame
    frame = cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")

    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")

    # hsv range for upper and lower
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])

    frame = cv2.rectangle(frame, (40,1),(140,65),(0,0,0),-1) # clear button
    cv2.putText(frame, "CLEAR", (49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA) # add text to clear button

    frame = cv2.rectangle(frame, (160,1),(255,65),colors[0],-1) # blue color button 
    frame = cv2.rectangle(frame, (275,1),(370,65),colors[1],-1)
    frame = cv2.rectangle(frame, (390,1),(485,65),colors[2],-1)
    frame = cv2.rectangle(frame, (505,1),(600,65),colors[3],-1)

#   identify pointer by creating a mask
#   object detection and color based segmentation / color detection -> give marker object
    mask = cv2.inRange(hsv,Lower_hsv, Upper_hsv)  # this will return black window which will detect marker
    mask = cv2.erode(mask,kernel,iterations=1) # number of times errosion will be applied by removing boundary pixels of white area

        # remove all small noise 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # expand white area to restore the shape 
    mask = cv2.dilate(mask,kernel,iterations=1)
    #cv2.imshow("mask",mask)

    #cv2.imshow("White Winodw",paintWindow)
    #cv2.imshow("Cam",frame)

# detect the contours in the binary mask (contours: curve joining all continuous points along boundary of object having same intensity)
    cnts, z = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    centre = None # (store cordinates o fthe centre of largest contour)

    # process largest contour (object tracking application)
    if len(cnts) > 0:
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0] 
        ((x,y),radius) = cv2.minEnclosingCircle(cnt) # use x y and radius to make circle around contour
        cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
        # detect centre point after making circle 
        M = cv2.moments(cnt)
        #M['m10'] and M['m01']: first order moments 
        #M['m00'] : zero order moment (area of the contour)
        # variable to calculate centre point
        centre = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))


    # handle button clicks red , yellow , green ,blue, clear
        if centre[1] <= 65: # checks if the centre of the object is within top region of screen if y > 65 -> area is reserved for clickable button
            if 40 <= centre[0]<=140: # if x lies between this range id true then clear button action is triggered 
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)] 

                blue_index = 0   
                green_index = 0
                red_index = 0
                yellow_index = 0 
            # remove drawing -> del all strokes of all colors from paint window make all pixels white
                paintWindow[67:,:,:] = 255

            elif 160 <= centre[0]<=255:
                colorIndex = 0 # blue color
            elif 275 <= centre[0]<=370:
                colorIndex = 1 # green color
            elif 390 <= centre[0]<=485:
                colorIndex = 2 # red color
            elif 505 <= centre[0]<=600:
                colorIndex = 3 # yellow color

        else : 
            if colorIndex == 0 : # blue 
                bpoints[blue_index].appendleft(centre)
            elif colorIndex ==1 :
                gpoints[green_index].appendleft(centre)
            elif colorIndex ==2:
                rpoints[red_index].appendleft(centre)
            elif colorIndex ==3:
                ypoints[yellow_index].appendleft(centre)

    else : 
        bpoints.append(deque(maxlen=512))
        blue_index += 1

        gpoints.append(deque(maxlen=512))
        green_index += 1

        rpoints.append(deque(maxlen=512))
        red_index += 1

        ypoints.append(deque(maxlen=512))
        yellow_index += 1
    
    points = [bpoints,gpoints,rpoints,ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1,len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame,points[i][j][k-1], points[i][j][k],colors[i],2)
                cv2.line(frame,points[i][j][k-1], points[i][j][k],colors[i],2)

    cv2.imshow('Live Drawing', frame)
    cv2.imshow('paint',paintWindow)
    cv2.imshow('mask', mask)


    # condition to exit the loop after 1 milisec press q 
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release() # realease capture / webcam
cv2.destroyAllWindows()

 
