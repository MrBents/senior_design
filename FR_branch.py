import numpy as np
import cv2
import RepeatedTimer

class FacialRecognition():
    def __init__(self):
        total_images = 10

    def parse_frame(self, frame):
        pass

    def face_detect(total_images, frame):
        
        # Multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
            roi_color_face = frame[y:y+h, x:x+w]
            # writes image out
            # cv2.imwrite("face-" + str(index) + ".png", roi_color_face)
            
        
if __name__ == '__main__':
    fr = FacialRecognition()
    for i in range():        
        rt = RepeatedTimer.RepeatedTimer(1,face_detect(1, i))

