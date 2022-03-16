#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pyaudio
from numpy import zeros,linspace,short,fromstring,hstack,transpose,log2, log
from scipy import fft, signal
from time import sleep
import struct
from scipy.signal import hamming, convolve

frequencyoutput = True

C_NORMAL = 0
CSHARP_NORMAL = .06
D_NORMAL = .13
EFLAT_NORMAL = .21
E_NORMAL = .29
F_NORMAL = .37
FSHARP_NORMAL = .46
G_NORMAL = .56
GSHARP_NORMAL = .66
A_NORMAL = .76
BFLAT_NORMAL = .88
B_NORMAL = 1


NUM_SAMPLES = 2048
SAMPLING_RATE = 48000
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

print("Detecting Frequencies. Press CTRL-C to quit.")

while True:
    while _stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
    audio_data  = fromstring(_stream.read(
        _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
    
    normalized_data = audio_data / 32768.0    
    w = hamming(2048)  
        
    intensity = abs(w*fft.fft(normalized_data))[:1024]

    
    if frequencyoutput:
        which = intensity[1:].argmax()+1
        # use quadratic interpolation around the max
        if which != len(intensity)-1:
            y0,y1,y2 = log(intensity[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*SAMPLING_RATE/NUM_SAMPLES
        else:
            thefreq = which*SAMPLING_RATE/NUM_SAMPLES
       
        if(audio_data[0] > 275):
            octave = 0
            normalizedFreq = 0
            freq = thefreq
            freqMin = 16.35
            freqMax = 30.87
            
            normalizedFreq = (freq - freqMin) / (freqMax - freqMin)
            
            while(normalizedFreq < 0 or normalizedFreq > 1):
                octave += 1;
                freqMin *= 2;
                freqMax *= 2;
                
                normalizedFreq = (freq - freqMin) / (freqMax - freqMin);

            print(normalizedFreq)
            
            if(abs(normalizedFreq - C_NORMAL) <= .02):
                print("The Note is C on octave "+str(octave))
            if(abs(normalizedFreq - CSHARP_NORMAL) <= .02):
                print("The Note is C Sharp on octave "+str(octave))
            if(abs(normalizedFreq - D_NORMAL) <= .02):
                print("The Note is D on octave "+str(octave))
            if(abs(normalizedFreq - EFLAT_NORMAL) <= .02):
                print("The Note is E Flat on octave "+str(octave))
            if(abs(normalizedFreq - E_NORMAL) <= .02):
                print("The Note is E on octave "+str(octave))
            if(abs(normalizedFreq - F_NORMAL) <= .02):
                print("The Note is F on octave "+str(octave))
            if(abs(normalizedFreq - FSHARP_NORMAL) <= .02):
                print("The Note is F Sharp on octave "+str(octave))
            if(abs(normalizedFreq - G_NORMAL) <= .02):
                print("The Note is G on octave "+str(octave))
            if(abs(normalizedFreq - GSHARP_NORMAL) <= .02):
                print("The Note is G Sharp on octave "+str(octave))
            if(abs(normalizedFreq - A_NORMAL) <= .02):
                print("The Note is A on octave "+str(octave))
            if(abs(normalizedFreq - BFLAT_NORMAL) <= .02):
                print("The Note is B FLat on octave "+str(octave))
            if(abs(normalizedFreq - B_NORMAL) <= .02):
                print("The Note is B on octave "+str(octave))
 


# In[ ]:




