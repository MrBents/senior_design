import numpy as np
import cv2

class FacialRecognition():
    def __init__(self):
        pass

    def parse_frame(self, frame):
        pass

    def face_detect(self, frame):
        """
        Get the faces in frame

        try different cascades params

        :param frame: image
        :return: a list of images of faces
        """
        roi_color_faces = []
        # Multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            roi_color_faces.append(frame[y:y+h, x:x+w])
        return roi_color_faces
            
        
if __name__ == '__main__':
    fr = FacialRecognition()
    faces = fr.face_detect(cv2.imread("faceTest.jpg")) 
    i = 0   
    for face in faces:
        cv2.imwrite("face{}".format(i) + ".jpg", face)
        i += 1
        
