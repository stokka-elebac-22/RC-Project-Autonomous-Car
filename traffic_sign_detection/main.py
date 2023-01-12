import cv2

def detect_signs(img):
    signs = cascade.detectMultiScale(img)
    return signs

def show_signs(image, signs):
    for (x,y,w,h) in signs:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 5)

if __name__ == "__main__":

    cascade = cv2.CascadeClassifier('traffic_sign_detection/stop_sign_model.xml')
    img = cv2.imread('traffic_sign_detection/testimg.jpg')

    scale_percent = 30 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    signs = detect_signs(img)
    show_signs(img, signs)
            
    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()