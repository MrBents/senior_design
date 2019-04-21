import speech_recognition as sr 
import Audio

class adios:
    def __init__(self):
        self.rek = sr.Recognizer()
        self.audio = ""

    def record(self):
        with sr.Microphone() as source:
            print('say Something')
            self.audio = self.rek.listen(source)
            # write audio to a WAV file
            with open("Recording1.wav", "wb") as f:
                f.write(self.audio.get_wav_data())

    def get_adios(self):
        try:
            # print('Google transcribe:')
            # print('{}'.format(self.rek.recognize_google(self.audio)))
            return (self.rek.recognize_google(self.audio))
        except:
            pass
    
if __name__ == "__main__":
    adddd = Audio.Audio()
    aids = adios()
    aids.record()
    
    a = adddd.getOrder(aids.get_adios())
    print(a)