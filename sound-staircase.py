#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from psychopy import core, data, event, visual
import numpy as np
import os
from pyo import *

"""
Example of a 1-up-1-down staircase procedure to define an auditory perceptual 
threshold. 

After a detection, the volume is decreased by multiplying its value 
by 0.812, which corresponds to a 3dB reduction. If the tone is not detected, 
the volume is divided by 0.812 in order to increase its value.

A running average of performance is also calculated (ratio of correct/incorrect
detections). If performance falls below a threshold of 60%, the staircase steps
change by becoming smaller (the 0.812 value is increased by 0.05), up to 3 
changes, in order to have a fine-grained approximation of the threshold.

The data is then saved in a csv file.

Author: Santiago Munoz
Universite Libre de Bruxelles
smunozmo@ulb.ac.be
"""

#==================
# Initial settings
#==================

print("Starting server...")
#create and boot a sound server
sv = Server(sr=44100, nchnls=2, buffersize=128, duplex=0, winhost="asio")
sv.verbosity = 0
sv.boot()   # Initialize audio stream
sv.start()  # Activates server processing loop

#some staircase parameters
volumeStart = 0.0005  # Initial volume value. Corresponds to pyo's "mul" (1 dB == 0.001 mul)
volumeRatioStart = 0.812  # Volume reduction is done by dividing by this value (corresponds to -3dB decrease in perceived loudness)
volumeRatioChange = 0.05  # Value that will be added to volumeRatio to change step size (will never go above 1.0)
volumeRatio = volumeRatioStart
volume = volumeStart

#running average
running_perf = np.array([])  # Running average of performance
window_length = 10  #change vol unit if 3 non-detections in the last 6 trials
perf_threshold = 0.6  #XX% performance

# We need a window to use keyboard events (the window needs to be active)
win = visual.Window([600, 100], color='Gray', units='pix')  # For testing only
soundDur = 3.  # sound duration (float)
timer = core.clock()

# Prepare for saving data to file
allTrials = []
filename = 'data' + os.path.sep + date + '_sound-staircase.csv'

idx =0
print("Starting experiment...")
while True:

    print("Starting new trial. Vol = " + str(volume))
    timer.reset()  # Restart timer
    detected = False  # Restart default value
    timer.add(soudDur)
    s = Sine(freq=700, mul=volume).out(dur=SoundDur)  # Start playing sound
    while timer.getTime()<0:
        #listen to keyboard
        keypress = event.getKeys(keyList=['space', 'n', 'escape'])
        if keypress == 'escape': core.quit()
        if keypress == 'space': detected = True

    #====================================
    # Staircase for adjusting tone volume
    #====================================

    #--------------------------------------
    # 1. Calculate running average of perf 
    #--------------------------------------
    
    # Add last detection responses to running average
    if len(running_perf)<window_length:  # Add new value only
        running_perf = np.concatenate((running_perf[:], [detected]))
    elif len(running_perf)==window_length:  # Add a new value and remove first value
        running_perf = np.concatenate((running_perf[1:], [detected]))
    
    # Calculate running average of performance
    running_perf_mean = np.count_nonzero(running_perf)/len(running_perf)
    
    goodperformance = running_perf_mean==1.0
    badperformance = running_perf_mean <= perf_threshold
    enoughtrials =  len(running_perf)==window_length
    room4change = (volumeRatio + volumeRatioChange5) < 1  # 3 decrements of unit
    # If random performance and enough trials
    if badperformance and enoughtrials and room4change:
        print("    Low performance, decreasing ratio of change")
        # Make the increments/decrements smaller
        volumeRatio += volumeRatioChange
        running_perf = np.array([])  # Re-start running average

    # If perfomance is good, return to previous ratios of change
    if goodperformance and enoughtrials and volumeRatio>volumeRatioStart:
        print("    Good performance, increasing ratio of change")
        # Make the increments/decrements bigger
        volumeRatio -= volumeRatioChange
        running_perf = np.array([])  # Restart running average
 
    #--------------------------------
    # 3. Modify volume for next trial
    #--------------------------------
    
    if detected:
        volume *= volumeRatio
        print("    Volume decreased!")
    elif not detected:
        volume /= volumeRatio
        print("    Volume increased!")

    #--------------
    # Save as data
    #--------------
    
    thisTrial = [idx, volume, detected, running_perf_mean, volumeRatio]
    allTrials += [thisTrial]
    
    idx += 1
    if key == 'escape':
        print("Final volume : " + str(volume))
        arr = np.array(allTrials)
        date = data.getDateStr()
        np.savetxt(filename, arr, delimiter=",") #, fmt = '%.10f')
        core.quit()
