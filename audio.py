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

import log
file = str(os.path.basename(__file__))

pitch = 0
volume = 0
run = True #this is for the external kill switch
on = False #this is for whether to currently calculate audio
volumeList = []
pitchList = []
maxVolumeScale = 2000

maxVolumeLoop = 0
maxVolumeList = []

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


def bar(label, value,last):

    if last >= value:
        last = value
    elif last < value:
        if last < 14:
            last+=.5

    return last



def between(pitch,low,high,maxValue,list):
    global position
    if pitch > low and pitch < high and pitch > maxValue:
        return list[position] 

def getResults():
    global positionVolume15
    global lastpositionVolume15
    positionVolume15,lastpositionVolume15 = getPositionVolume()

def calcVolume(maxLoopList):
    
    loopMax = max(maxLoopList)
    global maxVolumeScale
    if loopMax > maxVolumeScale * 2: #if the max is way off, help it get there faster
        maxVolumeScale *= 1.9
    if loopMax > maxVolumeScale * 2: #if the max is way off, help it get there faster
        maxVolumeScale *= 1.9
    #Aim to be about a third higher than the average max
    if loopMax + (loopMax*.3) > maxVolumeScale and loopMax > 2:
        maxVolumeScale *= 1.1
    if loopMax + (loopMax*.3) < maxVolumeScale and loopMax > 2:
        maxVolumeScale *= .75

    return maxVolumeScale #assign this to maxVolumeScale

    

def getPositionVolume():
    global maxVolumeLoop
    global maxVolumeList
    global maxVolumeScale
    maxVolumeLoop = 0
    positionVolume15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #clear out the list for a new loop
    position = 0 #keeps track of the position in the list to correlate volume


            #print pitchList
    for i in pitchList: # list of pitches found during the sample

        #for range in ranges15:
        for index, range in enumerate(ranges15):
            #print(index)

            if i < range: #if the pitch falls under the range
                if positionVolume15[index] < volumeList[position]:  #if the new value is greater than the old value
                    positionVolume15[index] = volumeList[position] #if so than save it
                    if volumeList[position] > maxVolumeLoop: #if the current volume is larger, add it to the recorded volume for the loop
                        maxVolumeLoop = volumeList[position]
                    break #so we dont save the value to every pitch level
        position+=1
    for index, i in enumerate(positionVolume15):
        if i > maxVolumeScale:
            i = maxVolumeScale
        if maxVolumeScale > 0: #Avoid division by zero error
            positionVolume15[index] = scale(i,(0,maxVolumeScale),(14,0))


    #for i in positionVolume15:
    for index, range in enumerate(positionVolume15):
        lastpositionVolume15[index] = bar(str(ranges15[index]),range,lastpositionVolume15[index])

    #Dynamic volume adjustments
    maxVolumeList.append(maxVolumeLoop)
    if len(maxVolumeList) > 5:
        maxVolumeScale = calcVolume(maxVolumeList)
        
        log.info(file,"maxScale: ",int(maxVolumeScale), " maxLoop: " ,max(maxVolumeList))
        
        maxVolumeList[:] = []

    volumeList[:] = [] #empty the list
    pitchList[:] = [] #empty the list
    return(positionVolume15,lastpositionVolume15)





position = 0

CHUNK = 4096 # the number of frames to split the sample rate into
CHUNK = 256
#FORMAT = pyaudio.paFloat32 #paInt16 #paInt8
#CHANNELS = 1
RATE = 44100 #44100 #sample rate i.e. number of frames per second

   
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
ranges15 = [p1, p2 , p3 , p4 , p5 , p6 , p7 , p8 , p9, p10, p11, p12 ,p13, p14, p15]
lastVolume15 = []
positionVolume15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lastpositionVolume15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
 


def start():
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



    # This is the main loop

    reset = 0
    while run == True:
        while on == True:
            global position
            # Keep track of time
            runTime = time.time() - start_time
            runTime = float(runTime)

            # if there is an io overflow this handles it
            try:
                data = stream.read(CHUNK // 2)
            #except IOError as ex:
            except KeyboardInterrupt:
                print()
                print("Interup detected")
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            except:
                #if ex[1] != pyaudio.paInputOverflowed:
                #    raise
                #data = '\x00' *  (CHUNK  * 2)  # or however you choose to handle it, e.g. return None
                log.warning(file,"Errrrrrrror Overload, skipping...but it's okay")

        

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
                
                tenthSec += 0.1
        
    #return ()


if __name__ == "__main__":
    startAudio()

