import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'result',0,179,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','result')
    s = cv2.getTrackbarPos('s','result')
    v = cv2.getTrackbarPos('v','result')

    # Normal masking algorithm
    # lower_blue = np.array([h,s,v])

    bound_red = np.array([110,100,139])
    bound_blue = np.array([80, 135, 80])
    bound_green = np.array([75,165, 121])
    
    # bound_red = np.array([110,100,139])
    # upper_red = np.array([180,210,195])

    # bound_blue = np.array([80, 135, 80])
    # upper_blue = np.array([165,255,230])

    # bound_green = np.array([75,165, 121])
    # upper_green = np.array([165,220,255])

    #upper_blue = np.array([180,255,255])
    upper_blue = np.array([h,s,v])

    mask = cv2.inRange(hsv,bound_red, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)

    cv2.imshow('result',result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()