import speech_recognition as sr 
import Audio
import timeout_decorator

class adios:
    def __init__(self):
        self.rek = sr.Recognizer()
        self.audio = ""

    @timeout_decorator.timeout(4)
    def record(self):
        with sr.Microphone() as source:
            print('say Something')
            self.audio = self.rek.listen(source)
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