import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny_image = cv2.Canny(blur, 100, 200)
    return canny_image

def reagon_of_interest(image):
    polygons = np.array([[(0,250),(0,200),(150,100),(500,100),(650,200),(650,250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons,255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1), (x2, y2), (0,255,0), 5)
    return line_image

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = 300
    y2 = 120
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append([slope,intercept])
        else:
            right_fit.append([slope,intercept])
    left_fit_average = np.average(left_fit,axis=0) if len(left_fit) > 0 else [1,1]
    right_fit_average = np.average(right_fit,axis=0) if len(right_fit) > 0 else [1,1]
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

#image = cv2.resize(np.copy(img), (650,500))

def lane_lines(image):
    canny_image = canny(image)

    cropped_image = reagon_of_interest(canny_image)

    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 50, np.array([]),minLineLength=40,maxLineGap=5)
    averaged_lines = average_slope_intercept(image,lines)

    line_image = display_lines(image, averaged_lines)

    combo_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)

    return combo_image