import pyaudio
import wave
import os
import RPi.GPIO as GPIO
import time
from datetime import datetime

def my_function():
    time.sleep(3)
    form_1 = pyaudio.paInt16
    chans=1
    samp_rate = 44100
    chunk = 4096
    record_secs = 8     #record time
    dev_index = 7
    current_time = datetime.now().strftime("%m_%d_%Y,%H:%M:%S")
    wav_output_filename = current_time+'.wav'
    wav_input_file = 'test1.wav'


    audio = pyaudio.PyAudio()
    frames=[]

    #creates wave file with audio read in
    #Code is from the wave file audio tutorial as referenced below



    #plays the audio 
    print("start playing file")
    os.system("amixer set Master 100%")
    os.system("aplay test1.wav")
    print("done playing file")

    #setup audio input stream
    stream=audio.open(format = form_1,rate=samp_rate,channels=chans, input_device_index = dev_index, input=True, frames_per_buffer=chunk)
    print("recording")

    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data=stream.read(chunk,exception_on_overflow = False)
        frames.append(data)

    print("finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wavefile=wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()


    os.system("aplay ending.wav")
    print("done playing file")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
		if GPIO.input(10) == GPIO.HIGH: my_function()
            
		else: 
			print("Phone Hung Up")

