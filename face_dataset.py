import cv2
import os

def main(name):
   
    cam = cv2.VideoCapture(0)
    count = 0
    #name=input("enter name")   
    os.mkdir("dataset/"+name) 
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
            count += 1
    
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/"+name+"/"+ str(count) + ".jpg", img[y:y+h,x:x+w])
    
        cv2.imshow('Dataset capture', img)
    
        k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 100: # Take 30 face sample and stop video
             break
    
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    #return face_id


#main("00")