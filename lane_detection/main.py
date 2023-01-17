import cv2
import numpy as np

import warnings

# SOURCE https://medium.com/analytics-vidhya/lane-detection-for-a-self-driving-car-using-opencv-e2aa95105b89

# NOTE:
# need to change paremeters through test and fail does not work for all images with the same parameters

# TODO:
# 1. Warp perspective lane OK!
# 2. Draw circle on lane image
# 3. Use circle to find intersection point
#    1. Two images: one circle on each
#    2. Circle white, background black
#    3. Check pixel for pixel which pixel that’s white on each picture
# 4. Draw back lane on original image with the circles if wanted??? OK!


def get_lane_region(image):
    offset = 250
    height = image.shape[0]
    width = image.shape[1]
    triangle = np.array(
        [[(0, height-offset), (width, height-offset),
          (int(width/2), int(height / 2.7))]]
    )
    black_image = np.zeros_like(image)
    mask = cv2.fillPoly(black_image, triangle, (255, 255, 255))
    mask = cv2.rectangle(mask, (0, height-offset),
                         (width, height), (255, 255, 255), -1)
    return cv2.bitwise_and(image, mask)


def get_line_coordinates_from_parameters(image, line_parameters):
    slope = line_parameters[0]
    intercept = line_parameters[1]
    y1 = image.shape[0]  # since line will always start from bottom of image
    y2 = int(y1 * (2.5 / 5))  # some random point at 3/5
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def get_average_lines(image, lines):
    if lines is not None:
        left_fit = []  # will hold m,c parameters for left side lines
        right_fit = []  # will hold m,c parameters for right side lines

        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    parameters = np.polyfit((x1, x2), (y1, y2), 1)
                    slope = parameters[0]
                    intercept = parameters[1]
                    if slope < 0:
                        left_fit.append((slope, intercept))
                    else:
                        right_fit.append((slope, intercept))
                except np.RankWarning:
                    pass

        left_line = None
        right_line = None

        # now we have got m,c parameters for left and right line, we need to know x1,y1 x2,y2 parameters
        if len(left_fit) > 0:
            left_fit_average = np.average(left_fit, axis=0)
            left_line = get_line_coordinates_from_parameters(
                image, left_fit_average)
        if len(right_fit) > 0:
            right_fit_average = np.average(right_fit, axis=0)
            right_line = get_line_coordinates_from_parameters(
                image, right_fit_average)
        return np.array([left_line, right_line], dtype=object)
    return None


def get_lane_lines(image, kernel_size):
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussianBlur = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    low_threshold = 100
    high_threshold = 200
    canny = cv2.Canny(gaussianBlur, low_threshold, high_threshold)
    dilate = cv2.dilate(canny, (3, 3), iterations=1)
    roi = get_lane_region(dilate)
    lines = cv2.HoughLinesP(
        roi, 1, np.pi / 180, 40, np.array([]), minLineLength=200, maxLineGap=30
    )
    return lines


def show_lines(image, lines):
    if lines is not None:
        for line in lines:
            if line is not None:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 20)


def get_diff_from_center_info(image, lines):
    if lines is not None:
        width = image.shape[1]
        center_car = width/2
        center_lane = 0
        start = None
        stop = None

        real_width = 200
        for line in lines:
            if line is not None:
                x1, _, _, _ = line.reshape(4)
                if start is None:
                    start = x1
                elif stop is None:
                    stop = x1

        diff = None
        if start is not None and stop is not None:
            center_lane = start + (stop-start)/2
            diff = (center_car - center_lane)/width * real_width
        return diff


def show_circles(image, points_coordinates, diff):

    coordinates_x = [points_coordinates[0][0], points_coordinates[1][0]]
    coordinates_y = [points_coordinates[0][3], points_coordinates[1][3]]
    width = max(coordinates_x) - min(coordinates_x)

    # NEED TO FIX HERE:: HEIGHT IS DIFF??
    height = image.shape[0]

    offset = int(image.shape[1]/2 - min(coordinates_x))

    output = np.float32([[0, 0],
                        [0, height],
                        [width, height],
                        [width, 0]])

    input = np.float32([[points_coordinates[0][2], points_coordinates[0][3]],
                        [points_coordinates[0][0], points_coordinates[0][1]],
                        [points_coordinates[1][0], points_coordinates[1][1]],
                        [points_coordinates[1][2], points_coordinates[1][3]]])

    pertransform = cv2.getPerspectiveTransform(input, output)

    warped = cv2.warpPerspective(
    image, pertransform, (width, height), flags=cv2.INTER_LINEAR)

    x1 = offset
    y1 = warped.shape[0]

    x3 = int(warped.shape[1]/2)
    y3 = int(warped.shape[0]*0.6)

    cv2.line(warped, (x3, y1), (x3, 0), (255,255,0), 20)

    cv2.circle(
        warped, (x1, y1), 10, (0, 0, 255), 20)
    cv2.circle(
        warped, (x3, y1), 10, (255, 0, 0), 20)
    cv2.circle(
        warped, (x3, y3), 10, (255, 0, 0), 20)
    
    x2 = int(offset + (x3 - offset)/2)
    y2 = int(y3 + (warped.shape[0]-y3)/2)

    #z = np.polyfit([x1, x1, x1, x1,x1, x1, x1, x1,x1, x1, x1, x1,x1, x1, x1, x1,x1, x1, x1, x1,x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x1, x3, x3, x3, x3, x3, x3, x3, x3, x3], 
    #[y1, y1, y1,y1,y1, y1, y1,y1,y1, y1, y1,y1,y1, y1, y1,y1,y1, y1, y1,y1,y1, y1, y1,y1,y1, y1, y1,y1,y1, y1, y1,y1, y1, y1, y1, y1*0.8, y1*0.6, y3, y3*0.8, y3*0.6, 0, 0, 0, 0, 0, 0],15)
    #z = np.polyfit([x1, x2, x3, x3, x3, x3, x3], [y1, y2, y3*0.6, y3*0.4, 0, 0, 0], 20)
    z = np.polyfit([x1, x2, x3], [y1, y2, y1], 2)
    lspace = np.linspace(x1, x2, 100)

    draw_x = lspace
    draw_y = np.polyval(z, draw_x)   # evaluate the polynomial

    draw_points = (np.asarray([draw_x, draw_y]).T).astype(np.int32)   # needs to be int32 and transposed

    cv2.polylines(warped, [draw_points], False, (0,0,0), 15)  # args: image, points, closed, color

    z = np.polyfit([x1, x2, x3], [y3, y2, y3,], 2)
    lspace = np.linspace(x2, x3, 100)

    draw_x = lspace
    draw_y = np.polyval(z, draw_x)   # evaluate the polynomial

    draw_points = (np.asarray([draw_x, draw_y]).T).astype(np.int32)   # needs to be int32 and transposed

    cv2.polylines(warped, [draw_points], False, (0,0,0), 15)  # args: image, points, closed, color


    cv2.circle(
        warped, (x2, y2), 10, (0, 255, 0), 20)


    unwarped = cv2.warpPerspective(warped, np.linalg.inv(
        pertransform), (image.shape[1], height), cv2.BORDER_TRANSPARENT)

    weighted = cv2.addWeighted(image, 0.4, unwarped, 0.2, 0)

    cv2.imshow("warped", warped)
    cv2.imshow("unwarped", unwarped)
    cv2.imshow("weighted", weighted)


if __name__ == "__main__":
    #cap = cv2.VideoCapture("./assets/challenge_video.mp4")
    frame = cv2.imread("lane_detection/assets/sykkelbane.jpg")

    scale_percent = 30  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    while True:
        '''ret, frame = cap.read()

        if cv2.waitKey(1) == ord('q') or ret == False:
            break
        '''
        lines = get_lane_lines(frame, 5)
        lines = get_average_lines(frame, lines)
        show_lines(frame, lines)
        diff = get_diff_from_center_info(frame, lines)

        if diff is not None:
            cv2.putText(
                frame, f"Diff from center: {diff}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        show_circles(frame, lines, diff)

        #cv2.imshow('frame', frame)
        cv2.waitKey(0)
        break

    # cap.release()
    cv2.destroyAllWindows()
