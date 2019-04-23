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
import firebase_admin
from firebase_admin import credentials, firestore
import time
from time import sleep
import multiprocessing
import csv

# TODO Customer faceID check
# TODO update the retrieval of the customer information

class App:
    def __init__(self, window, window_title, video_source=0, customer = None, database_ref = None):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.fr = fr.FacialRecognition()
        self.audioFile = None
        self.current_order = None
        self.gg = gg.adios()
        self.ac = Audio_clean.Audio()
        self.database_ref = database_ref
        self.id_list = []

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
        print('Adam and Eve')
        # get order
        self.current_order_transcribe_text.set(self.gg.get_adios())
        # self.get_transcribed_order()
        temp = self.get_transcribed_order()
        # print(temp)
        # self.current_order_text.set(str(temp))
        self.current_order = temp 


    def get_transcribed_order(self):
        '''
        use the transcribe to get the orders
        '''
        # transcript = self.ac.getTranscript()
        # self.current_order = self.ac.getOrder(transcript=transcript)
        transcript = self.gg.get_adios()
        print(transcript)
        self.current_order = self.ac.getOrder(transcript=transcript)
        print(self.current_order)
        # self.get_customer()
        self.write_csv()
        return self.current_order
 

    def get_unordered_customer(self):
        '''
        :return: faceID 
        '''
        pass

    def parallel_request(self, x, l):
        try:
            print('before')
            x._reference.set({u'probabilities': l})
            print('after')
        except Exception as e:
            print(e)
            print(l)
            print('after - Exc')
        

    def write_csv(self):
        filename = 'customer_order.csv'
        with open(filename, 'wb') as csv_file:
            csv_writer = csv.writer(csv_file, deimiter=',')
            time_stamp = time.time()
            csv_writer.writerow(time_stamp)

    # not
    def get_customer(self):
        '''
        check for the customer in the database
        proceed accordingly
        '''
        order1 = self.current_order
        va = 'sam'
        a_ref = self.database_ref.where(u'face_id', u'==', u'{}'.format(va)).get()
        print('got the sam doc')
        # print((a_ref))
        for a in a_ref:
            print('inside loop')
            abc = (a._data['probabilities'])
            # print(type(abc))
            l = []
            for item in abc:
                if item['name'] in order1.keys():
                    # print(item['name'])
                    # print(order1.get((item['name'])))
                    item['value'] += order1.get((item['name']))
                    # a._reference.update()
                l.append(item)
            print(l)
            a._reference.set({u'probabilities': l},merge=True)
            print('finished setting list on db')
            # a = Thread(target=self.parallel_request, args=(a, l,))
            # try:
            #     a.start()
            #     a.join()
            # except Exception as e:
            #     print(str(e))
            #     a._delete()
            #     continue
            #print('lksdfhlsdkafhlkdsfhakjsdcfbfgcbajhgcfbajcgbasdf\n\n\nn\kdjfgkjdhkajsdhfkajsdfhkasjd')
        # if face id is found in the database
        # 1. add current order to customer
        # if self.custome
        # else
        # else:


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
                # id = self.get_faceID()
                # previously unseen customer
                # if id not in self.id_list:
                    # self.id_list.append(id)
                    # retrieve customer info, with face id



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
    App(tkinter.Tk(), window_title = "CFA Counter")
    # cred = credentials.Certificate("serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)

    # db = firestore.client()

    # order_list = [{'value': 50, 'name': "Chicken Sandwich"}, {'value': 25, 'name': "Deluxe Sandwich"}, {'value': 10, 'name': "Spicy Chicken Sandwich"}, {'value': 5, 'name': "Spicy Deluxe Sandwich"}, {'value': 5, 'name': "Grilled Chicken Sandwich"}, {'value': 3, 'name': "Grilled Chicken Club"}, {'value': 2, 'name': "Nuggets"}]
    # doc_ref = db.collection(u'Customer').document(u'max')

    # doc_ref.set({
    #     u'age': 18,
    #     u'ethnicity': u'white',
    #     u'gender': u'female',
    #     u'inLine': True,
    #     u'face_id': u'max',
    #     u'probabilities': order_list
    # })
    # cus_ref = db.collection(u'Customer')

    # Create a window and pass it to the Application object
    # print(a.retrieval)
    # print(App.retrieval())
        
