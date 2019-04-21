import numpy as np
import cv2
import FR_branch as fr
from FE_branch import * 
import tkinter
import PIL 
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import Customer
from Customer import CFA_Menu
from Customer import Customer_Order
from matplotlib import pyplot as plt
import Audio as Audio_clean
import google_speech as gg 
from threading import Thread 

# TODO Customer faceID check
# TODO update the retrieval of the customer information

class App:
    def __init__(self, window, window_title, video_source=0, customer = None):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.fr = fr.FacialRecognition()
        self.audioFile = None
        self.current_order = None
        self.gg = gg.adios()
        self.ac = Audio_clean.Audio()

        # Customer Info
        self.customer_detected = customer
        self.customer_label_text = tkinter.StringVar()
        self.customer_label_text.set("customer")

        # Current Order Transcribe
        self.current_order_transcribe_text = tkinter.StringVar()
        self.current_order_transcribe_text.set("customer_current_order")
        
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
 
        # Button that lets the user record the order
        self.btn_text = tkinter.StringVar()
        self.btn_text.set("Start Order")
        self.btn_snapshot=tkinter.Button(window, textvariable=(self.btn_text), width=50, command=self.record)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # Customer Label
        self.customer_label = tkinter.Label(window, textvariable = self.customer_label_text)
        self.customer_label.pack(anchor=tkinter.CENTER, expand=True)

        # Current Order Label
        self.customer_order_transcribe_label = tkinter.Label(window, textvariable = self.current_order_transcribe_text)
        self.customer_order_transcribe_label.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15 
        self.update()
 
        self.window.mainloop()
 
    def record(self):
        '''
        Record Button
        update the audio file with recording
        '''
        print("button clicked")   
        # self.audioFile = 
        self.gg.record()
        # finished recording

        # get order
        self.current_order_transcribe_text.set(self.gg.get_adios())
        # self.get_transcribed_order()
        temp = self.get_transcribed_order()
        print(temp)
        # self.current_order_text.set(str(temp))
        self.current_order = temp 


    def get_transcribed_order(self):
        '''
        use the transcribe to get the orders
        '''
        # transcript = self.ac.getTranscript()
        # self.current_order = self.ac.getOrder(transcript=transcript)
        self.current_order = self.ac.getOrder(transcript=self.gg.get_adios())
        
        return self.current_order
 
    def get_faceID(self):
        '''
        :return: faceID 
        '''
        pass
 
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # update the face detected inside the frame
        if ret:
            img = PIL.Image.fromarray(frame)
            self.fr.face_detect(frame)
            # if a face is found
            if (self.fr.faces is not None):
                # draw red rectangle on face region
                draw = PIL.ImageDraw.Draw(img)
                for (x,y,w,h) in self.fr.faces:
                    draw.rectangle([x, y, x+w, y+h], None, '#ff0000') 
                del draw
                
                # #TODO Customer faceID check
                # #   and update the customer, customer labels
                # if (new): 
                #     # create a temporary customer
                #     self.customer_detected = Customer.Customer()
                # else:
                #     pass


                # update customer label text
                self.customer_label_text.set(str(self.customer_detected))


        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = img)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
        self.window.after(self.delay, self.update)
 

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release() 

if __name__ == '__main__':

    # Create a window and pass it to the Application object
    App(tkinter.Tk(), window_title = "CFA Counter")

        
