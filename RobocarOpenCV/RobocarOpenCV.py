import cv2
import numpy as np
import time
import imutils
import lane_lines as ll
import autocanny
import COSMOSopencv as cosmos

cap = cv2.VideoCapture('testvid.mp4')

while(1):
    time.sleep(1/20);
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_orange = np.array([0,70,50])
    upper_orange = np.array([35,255,255])
    
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    orangeMask = cv2.bitwise_and(frame,frame, mask= mask)
    orangePixelCount = np.sum(orangeMask)

    cv2.imshow('Original',frame)
    edges = cv2.Canny(frame,100,200)
    cv2.imshow('Edges',edges)
    cv2.imshow('AutoCanny', autocanny.auto_canny(frame))

    whitePixels = ll.filter_white(frame)
    whitePixelCount = np.sum(whitePixels)
    cv2.imshow('White', whitePixels)#, [0, 0, 175], [180, 80, 255]))

    print('White Pixels: ' + str(whitePixelCount) +  ' Currently ' + ('VALID' if  (50000 < whitePixelCount) and (whitePixelCount < 3500000) else 'ABSOLUTE GARBAGE'))
    #print('Orange Pixels: ' + str(orangePixelCount) +  'Currently ' + ('VALID' if  (50000 < orangePixelCount) and (orangePixelCount < 3500000) else 'INVALID'))
    

    cv2.imshow('Lines', ll.annotate_image_array(frame))

    cv2.imshow("Orange", orangeMask)
    cv2.imshow('Center Line', ll.annotate_center_lines(frame))
    
    try:
        cv2.imshow('cosmos', cosmos.lane_lines(frame))
    except:
        print("cosmos u fail")

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()