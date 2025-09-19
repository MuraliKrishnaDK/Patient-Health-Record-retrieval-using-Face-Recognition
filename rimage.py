import cv2
import os

def main():
    comp=0
    save=0
    cam = cv2.VideoCapture(0)
    while(True):
        
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        ret, img = cam.read()
        #print(ret)
        #img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
        
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)  
            if save==1:
                cv2.imwrite("in.jpg", img[y:y+h,x:x+w])
                comp=1
    
        cv2.imshow('Detecting face - Press S to Capture', img)
    
        k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
        if k==ord("s"):
            save=1
        if k == 27 or comp==1:
            break

    
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    #return face_id


#main()