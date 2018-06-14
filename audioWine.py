#!/usr/bin/env python3

"""

main.py will import this module and run it in a seperate thread.
run = True will serve as the kill switch.

"""


from __future__ import division

import sys
sys.path.append('/Library/Python/2.7/site-packages')

#for the live audio
import aubio
import numpy as num
import pyaudio
import time
import operator
import os

pitch = 0
volume = 0
run = True














def bar(label, value,last):
    string = ""
    count = 0
    if value > 2000:
        value = 2000
    while value > 0:
        count+=1
        string+="-" 
        value-=50        
    while count < last - 1: #add space for the memory bar
        string+=" "
        count+=1
    
    string+="|"
    print(label , string)
    return count

def between(pitch,low,high,maxValue,list):
    global position
    if pitch > low and pitch < high and pitch > maxValue:
        return list[position] 


position = 0

CHUNK = 4096 # the number of frames to split the sample rate into
CHUNK = 256
#FORMAT = pyaudio.paFloat32 #paInt16 #paInt8
#CHANNELS = 1
RATE = 44100 #44100 #sample rate i.e. number of frames per second

    ####CODING AND WINE!!
#     Frequency (Hz)	Octave	Description
# 16 to 32	1st	The lower human threshold of hearing, and the lowest pedal notes of a pipe organ.
# 32 to 512	2nd to 5th	Rhythm frequencies, where the lower and upper bass notes lie.
# 512 to 2048	6th to 7th	Defines human speech intelligibility, gives a horn-like or tinny quality to sound.
# 2048 to 8192	8th to 9th	Gives presence to speech, where labial and fricative sounds puss.
# 8192 to 16384	10th	Brilliance, the sounds of bells and the ringing of cymbals and sibilance in speech.
# 16384 to 32768	11th	Beyond brilliance, nebulous sounds approaching and just passing the upper human threshold of hearing
#  
# Map
# Everything lower than the number is included
p1 = 16
p2 = 32
p3 = 256
p4 = 512
p5 = 750
p6 = 1000 
p7 = 1500
p8 = 2000
p9 = 3000
p10 = 5000
p11 = 6500
p12 = 8192
p13 = 10000
p14 = 20000
p15 = 32768
ranges13 = [p1, p2 , p3 , p4 , p5 , p6 , p7 , p8 , p9, p10, p11, p12 ,p13, p14, p15]
lastVolume13 = []
positionVolume13 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lastPositionVolume13 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# 
# 
# 
#    



def startAudio():
    global pitch, volume

    # PyAudio object.
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Aubio's pitch detection.
    pDetection = aubio.pitch("default", CHUNK, CHUNK // 2, RATE)
    # Set unit.
    pDetection.set_unit("Hz")
    pDetection.set_silence(-40)

    # Keep track of time
    start_time = time.time()
    fiveSec = 0
    count = 0
    oneSec = 0
    tenthSec = 0.1

    #array for volume and pitch
    volumeList = []
    pitchList = []
    # maxPitch = 0
    # maxVolume = 0
    # volumePitch = {}
    # variablePitch = 1000 #wild guess!
    # variableVolume = 50
    # lowLast = 0
    # lowmidLast = 0
    # midLast = 0
    # midhighLast =0
    # highLast = 0


    # This is the main loop
    reset = 0
    while run == True:
        global position
        # Keep track of time
        runTime = time.time() - start_time
        runTime = float(runTime)

        # if there is an io overflow this handles it
        try:
            data = stream.read(CHUNK // 2)
        #except IOError as ex:
        except:
            #if ex[1] != pyaudio.paInputOverflowed:
            #    raise
            #data = '\x00' *  (CHUNK  * 2)  # or however you choose to handle it, e.g. return None
            print("Errrrrrrror Overload, skipping...but it's okay")

       

        samples = num.fromstring(data,
            dtype=aubio.float_type)
        pitch = pDetection(samples)[0]
        pitchUse = pitch 

        # Compute the energy (volume) of the
        # current frame.
        volume = num.sum(samples**2)/len(samples)

        # Format the volume output so that at most
        # it has six decimal numbers.
        volume = "{:.6f}".format(volume)
        volume = float(volume)
        volumeUse = volume * 1000000

        # save the volume and pitch to a list    
        pitchList.append(pitchUse)
        volumeList.append(volumeUse)
        #volumePitch[volumeUse] = pitchUse
        count+=1 
        
        if runTime + 5 > fiveSec:
            fiveSec += 5
            #going to use these to make a floating scale maybe


        if runTime + 1 > oneSec: #actions every second
            oneSec += 1
            FPS = count
            count = 0

        if runTime + 0.1 > tenthSec: #actions every tenth of a second
            positionVolume13 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #clear out the list for a new loop
            tenthSec += 0.1
           
            position = 0 #keeps track of the position in the list to correlate volume

            #print pitchList
            for i in pitchList: # list of pitches found during the sample

                #for range in ranges13:
                for index, range in enumerate(ranges13):
                    #print(index)

                    if i < range: #if the pitch falls under the range
                        if positionVolume13[index] < volumeList[position]:  #if the new value is greater than the old value
                            positionVolume13[index] = volumeList[position] #if so than save it
                            break #so we dont save the value to every pitch level
                position+=1
            os.system('clear')
            print
            print("FPS: ", FPS)
            print
         
            #for i in positionVolume13:
            for index, range in enumerate(positionVolume13):
                lastPositionVolume13[index] = bar(str(ranges13[index]),range,lastPositionVolume13[index])


            volumeList[:] = [] #empty the list
            pitchList[:] = [] #empty the list

    return ()


if __name__ == "__main__":
    startAudio()

