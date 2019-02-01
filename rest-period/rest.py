#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rest period of variable lengths, with different possibilities of stimulus
(photo, video, nothing...)

Author: Santiago Munoz
Universite Libre de Bruxelles
smunozmo@ulb.ac.be
"""

#========================
# Importing used modules
#========================

from __future__ import division
from psychopy import monitors, gui, visual, core, event, data, logging
from math import ceil, floor
import glob, os

#==========================================
# Store info about the experiment session
#==========================================
#------------------------------
# Experiment session GUI dialog
#------------------------------

#get values from dialog
expName='Rest'
myDlg = gui.Dlg(title=expName, pos = (860,340))
myDlg.addField(label='Participant',initial=0, tip='Participant name or code'),
myDlg.addField(label='Duration',choices=(3, 5, 10), tip='Minutes'),
myDlg.addField(label='Show',choices=('nothing','photo','beach','earth', 'forest')),
myDlg.addField(label='Hz', choices=(144, 60), tip='Refresh Rate')
myDlg.addField(label='Triggers', initial='Yes', choices=['Yes', 'No'], tip='Send Parallel Port Triggers')
dlg_data = myDlg.show()
if myDlg.OK==False: core.quit()  #user pressed cancel

#store values from dialog
expInfo = {'Participant':dlg_data[0],'Duration':dlg_data[1],'Show':dlg_data[2],
            'Hz':dlg_data[3],'Triggers':dlg_data[4]}
expInfo['date']=data.getDateStr()  #add a simple timestamp
expInfo['expName']=expName

#-----------------------
#setup files for saving
#-----------------------

if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['Participant'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#====================================================================
# Setting some static variables that we might want to tweak later on
#====================================================================

#determine screen's refresh rate
hz = int(expInfo['Hz'])
#experiment time durations in seconds
dur = float(expInfo["Duration"])*60.  # Convert minutes from dlg to seconds
times= {"BEFORE" : 6., "AFTER" : 6, "REST" : dur}
timesInFrames= {"BEFORE" : int(ceil(hz * times["BEFORE"])), 
                "AFTER" : int(ceil(hz * times["AFTER"])),
                "REST" : int(ceil(hz * times["REST"]))}

#=====================
# Open parallel port
#=====================
# Parallel port drivers need to be installed
# Note: the file inpout32.dll needs to be in the same folder

#triggers can be turned On or Off
if expInfo['Triggers']=='Yes': triggers = True
else: triggers = False

if triggers:

    from psychopy import parallel

    port = parallel.ParallelPort(address=0xDEFC) #0xB010 in new Stim PC, 0xDEFC in Personal PC

    #create function to use shorter trigger commands
    def sendTrigger(code):
        port.setData(code)  #sets combination of pins high/low (0-255)
        core.wait(0.002)
        port.setData(0)  #sets all pins low again

    # TRIGGERS:
    triggerList = {
        'restStart':100,  # rest Start
        'restEnd':101,  # rest Stop
        'eegStart':254,  # eeg rec start (set in biosemi config file)
        'eegStop':255   # eeg rec stop (set in biosemi config file)
        }

    sendTrigger(0) #sets all pins low to start
    sendTrigger(triggerList["eegStart"]) #start recording EEG
    
#===============================
# Creation of window and stimuli
#===============================

#-------------------
# Monitor and screen
#-------------------

# Monitor ('iiyama 144 Hz')
widthPix = 1920  #screen width in px
heightPix = 1080  #screen height in px
monitorwidth = 53.1  #monitor width in cm
viewdist = 60.  #viewing distance in cm
monitorname = 'iiyama'
scrn = 0  #0 to use main screen, 1 to use external screen
mon = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
mon.setSizePix((widthPix, heightPix))
mon.save()

# Initialize window
win = visual.Window(
    monitor=mon,
    size=(widthPix,heightPix),
    color=[0,0,.7255],  #'#B9B9B9' in hex
    colorSpace='hsv',  # !
    units='deg',
    screen=scrn,
    allowGUI=False,
    fullscr=True)
    
#-------------------
# Text stimuli
#-------------------

instruction_list = []
text_size = .6  #in degrees of visual angle (dva)
text_color = 'black'
text_font = 'Georgia'
restMessage = visual.TextStim(win,
    text=u"""Bienvenue. Nous allons commencer par une période de repos de trois minutes.
Vous ne devrez rien faire de particulier: trouvez simplement une position confortable et
laissez vos pensées divaguer. Evitez autant que possible les mouvements du corps.

Appuyez sur la touche « espace » pour démarrer la période de repos.""",
    color=text_color ,
    height=text_size,
    font=text_font)
OK = visual.TextStim(win,
    text=u"OK!",
    color=text_color ,
    height=text_size,
    font=text_font)
    
#--------
# IMAGES
#--------

photo = visual.ImageStim(win=win,
    image="stim/landscape-1920x1080.jpg", units="deg", size= (32, 18))
    
#--------
# VIDEO
#--------
filename = 'stim/' + expInfo["Show"] + '.mp4'
movie = visual.MovieStim(win, filename, size=(32,18), loop=True),
   
#============
# INITIALIZE
#============

if triggers: sendTrigger(triggerList["eegStart"])  #start EEG trigger

#text before rest
restMessage.draw()
win.flip()
keypress= event.waitKeys(keyList=['space', 'escape'])
if keypress[0] == 'escape': core.quit()

# Blank screen
for thisFrame in range(timeInFrames["BEFORE"]):
    win.flip()

if triggers: sendTrigger(triggerList["restStart"])  #start trigger  
    
#####
# 1 #
#####
if expInfo["Show"] is "nothing":
    for thisFrame in range(timeInFrames["REST"]):
        win.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                win.close()
                core.quit()

#####
# 2 #
#####
elif expInfo["Show"] is "photo":
    #start rest period
    for thisFrame in range(timeInFrames["REST"]):
        photo.draw() #landscape picture
        win.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                win.close()
                core.quit()
        
#####
# 3 #
#####
elif expInfo["Show"] is "beach":
    #start video
    for thisFrame in range(timeInFrames["REST"]):
        movie.draw()
        win.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                win.close()
                core.quit()

#####
# 4 #
#####
#elif expInfo["Show"] is "video-2":
    
if triggers: sendTrigger(triggerList["restEnd"])  #end trigger

# Blank screen
for thisFrame in range(timeInFrames["AFTER"]):
    win.flip()

#show 'OK!' message
OK.draw()
win.flip()
core.wait(2)
core.quit()