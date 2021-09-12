import cv2
import numpy as np
from time import sleep


offset = 6
line = 300
delay = 60

detec = []
count = 0

	
def center_find(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy 

cap=cv2.VideoCapture(0)



while True:
    _, frame=cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red=np.array([150,150,50])
    up_red=np.array([180,255,255])

    mask=cv2.inRange(hsv, lower_red, up_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    ret, frame1 = cap.read()
    tempo = float(1/delay)
    sleep(tempo) 
  
    contour, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (25, line), (600, line), (0, 0, 255), 3)
    for(i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x,y), (x+w,y+h), (255, 0, 255))
        validatecontour = (w >= 80) and (h >= 60)
        if not validatecontour:
            continue

        center = center_find(x, y, w, h)
        detec.append(center)
        cv2.circle(frame, center, 4, (0, 0, 255), -1)

        for (x, y) in detec:
            if (y < (line + offset)) and (y > (line-offset)):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                count += 1
                cv2.line(frame, (25, line), (1200, line), (0, 127, 255), 3)
                detec.remove((x, y))
                print("Count : " + str(count))
                sleep(2)


    cv2.putText(frame1, "Count : "+str(count), (280, 70), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 4)
    cv2.imshow("Video", frame1)


    k=cv2.waitKey(5) & 0xFF
    if cv2.waitKey(1) == 27:
        break

   
cv2.destroyAllWindows()
cap.release()
