import numpy as np
import cv2
import FR_branch as fr
from FE_branch import * 
import tkinter
import PIL 
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import Customer

#TODO Customer faceID check
#

class App:
    def __init__(self, window, window_title, video_source=1, customers = None):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.fr = fr.FacialRecognition()
        # customer
        self.customers_detected = customers
        self.customer_label_text = tkinter.StringVar()
        self.customer_label_text.set("customer_current_order")
        self.customer_likelihood_text = [tkinter.StringVar() for i in range(10)]
        [self.customer_likelihood_text[i].set("customer_likelihoods") for i in range(10)]
 
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
 
        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # Customer Data Label
        self.customer_label = tkinter.Label(window, textvariable = self.customer_label_text)
        self.customer_label.pack(anchor=tkinter.CENTER, expand=True)
        self.customer_likelihood_label = []
        for i in range(10):
            self.customer_likelihood_label.append(tkinter.Label(window, textvariable = self.customer_likelihood_text[i]))
            self.customer_likelihood_label[i].pack(anchor=tkinter.CENTER, expand=True)
 
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15 
        self.update()
 
        self.window.mainloop()
 
    def snapshot(self):
        """Button functionality"""       
 
    """important"""
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # update the face detected inside the frame
        if ret:
            img = PIL.Image.fromarray(frame)
            self.fr.face_detect(frame)
            if (self.fr.faces is not None):
                # draw red rectangle on face region
                draw = PIL.ImageDraw.Draw(img)
                for (x,y,w,h) in self.fr.faces:
                    draw.rectangle([x, y, x+w, y+h], None, '#ff0000') 
                del draw

                #TODO Customer faceID check
                #   and update the labels

                # update customer current order label text
                self.customer_label_text.set(str(self.customers_detected))
                # update
                for(i, item) in enumerate(self.customers_detected.current_orders.order_list):
                    # update customer's chance of ordering an item
                    # store it in temp tempVar
                    tempVar = self.customers_detected.item_ordering_likelihood[i]
                    tempStr = "".join(item + ":  " + str(tempVar))
                    self.customer_likelihood_text[i].set(tempStr)

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
    customer1 = Customer.Customer(current_order = {"Delux Sandwich": 3}, likelihoods = [0.5, 0.6, 0.4, 0.3, 0.7, 0.9, 0.3, 0.1, 0.4, 0.4], faceid = 0)
    # Create a window and pass it to the Application object
    App(tkinter.Tk(), window_title = "Tkinter and OpenCV", customers=customer1)

        
