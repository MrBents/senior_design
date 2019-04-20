# -*- coding: utf-8 -*-
'''
The original file has just the 2 classes. I added the main function to test
The commment section below gives an example of how to run the code.
You need the wave and pyaudio modules (pip install)
Portaudio needs to be downloaded and then compiled for it to work

It saves as a wave file. I dont know about mp3.

I was using the keyboard module (pip install) to test starting and stopping the recording based on a key press
It worked fairly well.

'''











'''recorder.py
Provides WAV recording functionality via two approaches:

Blocking mode (record for a set duration):
>>> rec = Recorder(channels=2)
>>> with rec.open('blocking.wav', 'wb') as recfile:
...     recfile.record(duration=5.0)

Non-blocking mode (start and stop recording):
>>> rec = Recorder(channels=2)
>>> with rec.open('nonblocking.wav', 'wb') as recfile2:
...     recfile2.start_recording()
...     time.sleep(5.0)
...     recfile2.stop_recording()
'''
import pyaudio
import wave
import keyboard
import time

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        print("* recording")
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        print("* done recording")
        return None

    def start_recording(self):
        print("* recording")
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        print("* done recording")
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

        
def record_audio():
    rec = Recorder(channels=2)
    with rec.open('Recording1.wav', 'wb') as recfile:
        keyboard.add_hotkey('r',recfile.start_recording)
        keyboard.add_hotkey('s',recfile.stop_recording)
        keyboard.wait('esc')        

        
if __name__=="__main__":
    pass
    #rec = Recorder(channels=2)
    #with rec.open('nonblocking.wav', 'wb') as recfile:
        # records for set duration (blocking => nothing else can happen in code while this records)
    #rec = Recorder(channels=2)
    #with rec.open('blocking.wav', 'wb') as recfile:
        #recfile.record(duration=5.0)

    # nonblocking => recording starts and stops at function calls, other stuff can happen between
    #rec = Recorder(channels=2)
    #with rec.open('nonblocking.wav', 'wb') as recfile2:
        #recfile2.start_recording()
        # any code can go here
        #time.sleep(5.0)
        #recfile2.stop_recording()
    # activate on key press, requires 'import keyboard'
    """
    rec = Recorder(channels=2)
    with rec.open('Recording1.wav', 'wb') as recfile:
        keyboard.add_hotkey('r',recfile.start_recording)
        keyboard.add_hotkey('s',recfile.stop_recording)
        keyboard.wait('esc')
    """