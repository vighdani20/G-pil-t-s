import cv2
import numpy as np
from time import sleep
from constans import *
"""
beimportaljuk a cv2-t, a numpyt, az idot (szukseges),

illetve a kulsoleg letrehozott constansot, igy konnyebb modositas, es rovidebb a main kodunk
"""
def takes_center(x, y, width, height):
    
    x1 = width // 2
    y1 = height // 2
    cx = x + x1
    cy = y + y1
    return cx, cy
"""
definialjuk kozepre az x, y, szelesseget, magassagot
"""

def set_info(detect):
    global cars
    for (x, y) in detect:
        if (pos_line + offset) > y > (pos_line - offset):
            cars += 1
            cv2.line(frame1, (25, pos_line), (1200, pos_line), (0, 127, 255), 3)
            detect.remove((x, y))
            print("Cars detected: " + str(cars))

"""
pozicionaljuk, hogy amely auto atmegy a vonalon a szamlalo szamoljon
"""

def show_info(frame1, dilated):
    text = f'Cars: {cars}'
    cv2.putText(frame1, text, (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Motorway camera", frame1)
    cv2.imshow("toDetect", dilated)

"""
Itt pedig informaljuk a kulso szemlelot, elnevezzuk, feliratozunk
"""
cars = 0
cap = cv2.VideoCapture('video.mp4')
subtraction = cv2.bgsegm.createBackgroundSubtractorMOG()  

"""
CAP= halmozott pontossagi profil // video.mp4 fajlt hasznaljuk, aminek egy mappaban
kell lennie az main, és a contanssal
"""

while True:
    ret, frame1 = cap.read()  # Keszitsuk el a video kepkockait
    tempo = float(1 / delay) #ezert kellett a time, hogy alkalmazhassunk delayt
    sleep(tempo)  # Kesleltetjuk a feldolgozast
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  #fekete-feherre alakitsuk a keretet
    blur = cv2.GaussianBlur(grey, (3, 3), 5)  #A kep hibait el kell tavolitani, mivel a video csak mp4 tipusu
    
    img_sub = subtraction.apply(blur)  #homalyt kivonjuk a keprol
    
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))  #suritjuk ami maradt a kivonasbol
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
        5, 5))  #Letrehozunk egy 5x5 matrixot, es a matrixot 0,1 kozotti resznel ellipszist keszitunk
    
    dilated = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)  #kepjavitas, itt igazabol a pixelhibakat kuszboljuk a morph segitsegevel, automata kitoltes
    
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



