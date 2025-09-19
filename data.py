import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
cnt=0 
while(True):
    
    ret, frame = cap.read()
    #frame = cv2.flip(frame, -1) # Flip camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    cnt=cnt+1
    cv2.imwrite("../nomask/"+str(cnt)+".jpg",frame)
    k = cv2.waitKey(30) & 0xff
    if cnt==200: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
