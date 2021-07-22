# import the necessary packages
import numpy as np
import cv2
# construct the argument parse and parse the arguments

# define a video capture object
vid = cv2.VideoCapture(0)

# define boundaries (lower)
bound_red = np.array([110,100,139])
upper_red = np.array([180,210,195])

bound_blue = np.array([80, 135, 80])
upper_blue = np.array([165,255,230])

bound_green = np.array([75,165, 121])
upper_green = np.array([165,220,255])

running = 0
while(running < 4):
    # Capture the video frame by frame
    ret, image = vid.read()
    
    # loop over the boundaries
    # for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
    # lower = np.array(lower, dtype = "uint8")
    # upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply
        # the mask
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, bound_red, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
        # show the images
    cv2.imshow("images", np.hstack([image, output]))
        # cv2.waitKey(0)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running += 1


  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

