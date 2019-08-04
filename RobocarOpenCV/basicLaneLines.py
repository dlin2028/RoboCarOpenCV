import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(lane_image,cv2.COLOR_RGB2GRAY)
    blur = cv2GaussianBlur(gray,(5,5),0)
    canny_image = cv2.Canny(blur, 100, 200)
    return (canny_image)

def reagon_of_interest(image):
    polygons = np.array([[(0,250),(0,200),(150,100),(500,100),(650,200),(650,250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons,255)
    maked_image = cv2.bitwise_and(image,mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeroes_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1), (x2, y2), (0,255,0), 5)
    return line_image

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = 300
    y2 = 120
    x1 = int((y1-intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.aray([x1, y2, x2, y2])

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
    left_fit_average = np.average(left_fit,axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, leftleft_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


            

image = cv2.imread('img3.jpg')
lane_image = np.copy(image)
lane_image = cv2.resize(lane_image (650,500))
canny_image = canny(lane_image)

cv2.waitKey()