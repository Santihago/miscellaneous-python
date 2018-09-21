#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from psychopy import core, data, event, visual
import numpy as np
import glob, os
from pyo import *

print("Starting server...")
# Create and boot a server
sv = Server(sr=44100, nchnls=2, buffersize=128, duplex=0, winhost="asio")
sv.verbosity = 0
sv.boot()   # Initialize audio stream
sv.start()  # Activates server processing loop

# How much to increase/decrease at every trial
volumeStart = 0.0005
volumeRatioStart = 0.812
volumeRatio = volumeRatioStart
volume = volumeStart
running_perf = np.array([])
hearing = True

#staircase
window_length = 10  #change vol unit if 3 non-detections in the last 6 trials
perf_threshold = 0.6  #XX% performance

print("Starting experiment...")

win = visual.Window([800, 600], color='Gray', units='pix')  # For testing only
idx =0
allTrials = []
while hearing is True:

    core.wait(1.)
    print("Starting new trial. Vol = " + str(volume))

    s = Sine(freq=700, mul=volume).out()

    keypress = event.waitKeys(keyList=['space', 'n', 'escape'])
    key = keypress[0]
    print(key)
    if key == 'space': detected = True
    elif key == 'n': detected = False

    s.stop()

    #------------------------------------
    # Staircase for adjusting tone volume
    #------------------------------------

    # 1. Calculate running average of perf 
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
    room4change = (volumeRatio + 0.05) < 1  # 3 decrements of unit
    # If random performance and enough trials
    if badperformance and enoughtrials and room4change:
        print("    Low performance, decreasing ratio of change")
        # Make the increments/decrements smaller
        volumeRatio += 0.05
        running_perf = np.array([])  # Re-start running average

    # If perfomance is good, return to previous ratios of change
    if goodperformance and enoughtrials and volumeRatio>volumeRatioStart:
        print("    Good performance, increasing ratio of change")
        # Make the increments/decrements bigger
        volumeRatio -= 0.05
        running_perf = np.array([])  # Re-start running average
 
    # 3. Modify volume for next trial
    if detected:
        volume *= volumeRatio
        print("    Volume decreased!")
    elif not detected:
        volume /= volumeRatio
        print("    Volume increased!")

    # Save as data
    thisTrial = [idx, volume, detected, running_perf_mean, volumeRatio]
    allTrials += [thisTrial]
    
    idx += 1
    if key == 'escape':
        print("Final volume : " + str(volume))
        arr = np.array(allTrials)
        date = data.getDateStr()
        np.savetxt('data' + os.path.sep + date + '_soundStaircase.csv', arr, delimiter=",")#, fmt = '%.10f')
        core.quit()
