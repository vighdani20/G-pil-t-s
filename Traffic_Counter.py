import cv2
import numpy as np
from time import sleep
from constans import *


def takes_center(x, y, width, height):
    """
    :param x: x object
    :param y: y object
    :param width: width object
    :param height: height object
    :return: that contains the coordinates of the center of an object
    """
    x1 = width // 2
    y1 = height // 2
    cx = x + x1
    cy = y + y1
    return cx, cy


def set_info(detect):
    global cars
    for (x, y) in detect:
        if (pos_line + offset) > y > (pos_line - offset):
            cars += 1
            cv2.line(frame1, (25, pos_line), (1200, pos_line), (0, 127, 255), 3)
            detect.remove((x, y))
            print("Cars detected: " + str(cars))


def show_info(frame1, dilated):
    text = f'Cars: {cars}'
    cv2.putText(frame1, text, (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Motorway camera", frame1)
    cv2.imshow("toDetect", dilated)


cars = caminhoes = 0
cap = cv2.VideoCapture('video.mp4')
subtraction = cv2.bgsegm.createBackgroundSubtractorMOG()  # Take the bottom and subtract from what is moving

while True:
    ret, frame1 = cap.read()  # Take each frame of the video
    tempo = float(1 / delay)
    sleep(tempo)  # Delays between each processing
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Take the frame and transform it to black and white
    blur = cv2.GaussianBlur(grey, (3, 3), 5)  # Blur to try to remove imperfections from the image
    img_sub = subtraction.apply(blur)  # Subtracts the image applied in the blur
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))  # "Thicken" what's left of the subtraction
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
        5, 5))  # Creates a 5x5 matrix, where the matrix format between 0 and 1 forms an ellipse inside
    dilated = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)  # Try to fill all the "holes" in the image
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    contour, img = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1, (25, pos_line), (1200, pos_line), (255, 127, 0), 3)
    for (i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_outline = (w >= width_min) and (h >= height_min)
        if not validate_outline:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center = takes_center(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)

    set_info(detect)
    show_info(frame1, dilated)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()

