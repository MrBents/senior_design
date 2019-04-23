import speech_recognition as sr 
import Audio
import multiprocessing

class adios:
    def __init__(self):
        self.rek = sr.Recognizer()
        self.audio = ""
        #self.pool = multiprocessing.Pool(1)
        # self.pool.apply_async(self.record())

   

    def record(self):
        #pool = multiprocessing.Pool(1)
        
        with sr.Microphone() as source:
            print('say Something')
            try:
                # p = multiprocessing.Process(target=self.rek.listen, args=(source,))
                #res = pool.apply_async(self.rek.listen, [source])
                self.audio = self.rek.listen(source,timeout=0, phrase_time_limit=5)
                # p.start()
                # p.join()
            except Exception as e:
                print('something timed out, ' + str(e))
            print('somthing said')
            # write audio to a WAV file
            #with open("Recording1.wav", "wb") as f:
                #f.write(self.audio.get_wav_data())
                #f.close()
            

    def get_adios(self):

            # print('Google transcribe:')
            # print('{}'.format(self.rek.recognize_google(self.audio)))

        return (self.rek.recognize_google(self.audio,language = 'en-EN'))

    
if __name__ == "__main__":
    adddd = Audio.Audio()
    aids = adios()
    aids.record()
    
    a = adddd.getOrder(aids.get_adios())
    print(a)