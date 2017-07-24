#!/usr/bin/env python

"""

main.py will import this module and run it in a seperate thread.
run = True will serve as the kill switch.

"""


from __future__ import division

#for the live audio
import aubio
import numpy as num
import pyaudio
import time

pitch = 0
volume = 0
run = True





CHUNK = 4096
FORMAT = pyaudio.paFloat32 #paInt16 #paInt8
CHANNELS = 1
RATE = 44100 #44100 #sample rate





def startAudio():
    global pitch, volume

    # PyAudio object.
    p = pyaudio.PyAudio()


    # Open stream.
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Aubio's pitch detection.
    pDetection = aubio.pitch("default", CHUNK, CHUNK // 2, 44100)
    # Set unit.
    pDetection.set_unit("Hz")
    pDetection.set_silence(-40)

    # Keep track of time
    start_time = time.time()
    fiveSec = 0

    # This is the main loop
    reset = 0
    while run == True:

        # Keep track of time
        runTime = time.time() - start_time
        runTime = float(runTime)

        # if there is an io overflow this handles it
        try:
            data = stream.read(CHUNK // 2)
        except IOError as ex:
            if ex[1] != pyaudio.paInputOverflowed:
                raise
            data = '\x00' *  (CHUNK  * 2)  # or however you choose to handle it, e.g. return None
            print "Errrrrrrror Overload, skipping...but it's okay"

        #data = stream.read(CHUNK // 2)

        samples = num.fromstring(data,
            dtype=aubio.float_type)
        pitch = pDetection(samples)[0]

        # Compute the energy (volume) of the
        # current frame.
        volume = num.sum(samples**2)/len(samples)

        # Format the volume output so that at most
        # it has six decimal numbers.
        volume = "{:.6f}".format(volume)
        volume = float(volume)

        if runTime + 5 > fiveSec:
            fiveSec += 5
            print
            print ("Run time (m) %f ") % (runTime / 60)
            print ("Volume: %f") % volume 
            print ("Pitch: %f") % pitch
            print



    return ()

#startAudio()
