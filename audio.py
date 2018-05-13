#!/usr/bin/env python



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
    maxPitch = 0
    maxVolume = 0
    volumePitch = {}
    variablePitch = 1000 #wild guess!
    variableVolume = 50
    lowLast = 0
    lowmidLast = 0
    midLast = 0
    midhighLast =0
    highLast = 0

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


            # print
            # print ("Run time (m) %f ") % (runTime / 60)
            # print ("Volume: %f") % volume
            # print ("Pitch: %f") % pitch
            # print



           
        if runTime + 1 > oneSec: #actions every second
            oneSec += 1
            #print "Number of loops per second" , count
            FPS = count
            count = 0
            
            #print time.time()

            #print volumeList
            #print len(volumeList)


        if runTime + 0.1 > tenthSec: #actions every tenth of a second
            tenthSec += 0.1
           
            # oldMaxPitch = maxPitch
            # oldMaxVolume = maxVolume
            # pitIndex, maxPitch = max(enumerate(pitchList), key=operator.itemgetter(1))
            # volIndex, maxVolume = max(enumerate(volumeList), key=operator.itemgetter(1))

            # if variablePitch > maxPitch * 2:
            #     variablePitch*=0.99
            # if variablePitch < maxPitch * 2:
            #     variablePitch*=1.01
            # if variableVolume > maxVolume * 2:
            #     variableVolume*=0.99
            # if variableVolume < maxVolume * 2:
            #     variableVolume*=1.01

            #print "Max volume: " , volValue , " Index: " , volIndex
            #print "Max pitch: " , pitValue , " Index: " , pitIndex
            #print "variable pitch" , variablePitch
            position = 0 #keeps track of the position in the list to correlate volume
            low = 0
            lowcount = 0
            lowmid = 0
            lowmidcount = 0
            mid = 0
            midcount = 0
            midhigh = 0
            midhighcount = 0
            high = 0
            highcount = 0
            #print pitchList
            for i in pitchList:
                # low =     between(i,   0,   32,    low,volumeList)
                # lowmid =  between(i,  32,  512, lowmid,volumeList)
                # mid =     between(i, 512, 2048,    mid,volumeList)
                # midhigh = between(i,2048, 8192,midhigh,volumeList)
                # high =    between(i,8192,99999,   high,volumeList)

                if i > 0 and i < 32: #lows
                #if i > 0 and i < 512: #lows
                    #print "Low Pitch: " , pitchList[position], "Volume: " , volumeList[position]
                    low+=volumeList[position]
                    lowcount+=1
                elif i > 32 and i < 512: #low-mid
                #elif i > 512 and i < 1024: #low-mid
                   #print "low-mid Pitch: " , pitchList[position], "Volume: " , volumeList[position]
                   lowmid+=volumeList[position]
                   lowmidcount+=1
                elif i > 512 and i < 2048: #mid
                    #print "mid Pitch: " , pitchList[position], "Volume: " , volumeList[position]
                    mid+=volumeList[position]
                    midcount+=1
                elif i > 2048 and i < 8192:#mid-high
                    #print "mid-high Pitch: " , pitchList[position], "Volume: " , volumeList[position]
                    midhigh+=volumeList[position]
                    midhighcount+=1
                elif i > 8192: #high
                    #print "high Pitch: " , pitchList[position], "Volume: " , volumeList[position]
                    high+=volumeList[position]
                    highcount+=1
                position+=1 #keeps track of the position in the list to correlate volume
            if lowcount > 0:
                low = low / lowcount
            if lowmidcount > 0:
                lowmid = lowmid / lowmidcount
            if midcount > 0:
                mid = mid / midcount
            if midhighcount > 0:
                midhigh = midhigh / midhighcount
            if highcount > 0:
                high = high / highcount
            os.system('clear')
            print
            print("FPS: ", FPS)
            print
            lowLast = bar("Low's Volume:      ",low,lowLast)
            lowmidLast = bar("Low-Mid's Volume:  ",lowmid,lowmidLast)
            midLast = bar("Mid's Volume:      ",mid,midLast)
            midhighLast = bar("Mid-High's Volume: ",midhigh,midhighLast)
            highLast = bar("High's Volume:     " ,high,highLast)
            # print "max pitch          " , "{:.2f}".format(variablePitch)
            # print "Low's Volume:      " , "{:.2f}".format(low)
            # print "Low-Mid's Volume:  " , "{:.2f}".format(lowmid)
            # print "Mid's Volume:      " , "{:.2f}".format(mid)
            # print "Mid-High's Volume: " , "{:.2f}".format(midhigh)
            # print "High's Volume:     " , "{:.2f}".format(high)

            
            
            volumeList[:] = [] #empty the list
            pitchList[:] = [] #empty the list
            ##maxPitch = max(volumePitch.iteritems(), key=operator.itemgetter(1))[0]
            #minPitch = min(volumePitch.iteritems(), key=operator.itemgetter(1))[0]
            #print maxPitch, minPitch
            #print volumePitch
            #print "Length: " ,len(volumePitch)
            #volumePitch.clear()
            
        #print "Volume: " , volumeUse , "Pitch: ", pitchUse
    return ()

startAudio()

