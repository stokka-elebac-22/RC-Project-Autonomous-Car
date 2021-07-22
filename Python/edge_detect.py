# https://stackoverflow.com/questions/7263621/how-to-find-corners-on-a-image-using-opencv
# import the necessary packages
import numpy as np
import cv2

vid = cv2.VideoCapture(0)
bound_red = np.array([110,100,139])
upper = np.array([180,255,255])

running = 0
while(running < 1):
    ret, image = vid.read()
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, bound_red, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    gray = cv2.cvtColor(output,cv2.COLOR_HSV2RGB)    #--- convert to grayscale 
    gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)    #--- convert to grayscale 

    # bi = cv2.bilateralFilter(gray, 5, 75, 75)
    # dst = cv2.cornerHarris(bi, 2, 3, 0.04)

   #  #--- create a black image to see where those corners occur ---
   #  # black = np.zeros_like(dst)
       #--- applying a threshold and turning those pixels above the threshold to white ---           
    #black[dst>0.01*dst.max()] = 255
    canny = cv2.Canny(gray, 120, 255, 1)

    corners = cv2.goodFeaturesToTrack(canny,4,0.5,50)
    for corner in corners:
        x,y = corner.ravel()
        cv2.circle(image,(x,y),5,(36,255,12),-1)

    cv2.imshow("images", np.hstack([image, output]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running += 1


  
vid.release()
cv2.destroyAllWindows()

