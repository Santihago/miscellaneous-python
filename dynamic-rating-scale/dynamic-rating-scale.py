from __future__ import division
from psychopy import visual, core, event

#--------------
# CREATE WINDOW
#--------------

win = visual.Window([800, 600], color='Gray', units='pix')  # For testing only

#--------------
# RATING SCALE
#--------------

# Creating my own rating scale for full flexibility.
# You should set exp units in deg (degrees of visual angle)
# I follow guidelines from Matejka 2016: No ticks, 2 labels, dynamic text
# feedback

#------------- You can adjust these
scale_max = 100 # Maximum rating in the rating scale (int)
rs_max = 7.5  # scale upper limit in degrees of visual angle

#------------- No need to adjust these
rs_col = 'black'
rs_txt_col = 'black'
rs_txt_size = .6
labelsYPos = -1
dynTxtYPos = 1
_rs_min = (-1 * rs_max)
ticksXPos = [x * rs_max for x in [-.5, 0, .5]]  # Bands
labelsXPos = [x * rs_max for x in [-1, 1]]
labels = ["0 %", "100 %"]
dyn_txt = visual.TextStim(win, text=u"", height=rs_txt_size, color = rs_txt_col)

# Scale stimuli: horizontal bar, labels, ticks/bands
rs_stims = []
rs_stims += [visual.Rect(win, width=rs_max*2, height=.1, fillColor = rs_col, 
             lineColor = rs_col)]
#for thisXPos in ticksXPos: # Mini-ticks
#    rs_stims += [visual.Rect(win, width=1, height=.25, pos = [thisXPos, 0], 
#                 fillColor = 'white', opacity = .75)]
for nr, thisXPos in enumerate(labelsXPos):  # Text
    rs_stims += [visual.TextStim(win, text=labels[nr], height=rs_txt_size, 
                 pos = [thisXPos, labelsYPos], color = rs_txt_col)]

# Moving slider
rs_slider = visual.Rect(win, width=.25, height=.75, opacity = 1, 
                        fillColor = rs_col, lineColor = rs_col)

#-------
# MOUSE
#-------

mouse = event.Mouse(visible=True, win=win)

while True:
#---------------------------
# Rating Scale during sound
#---------------------------

    # Prepare and reset between repeated uses of the same scale
    event.clearEvents()  
    detected = False
    detectedRT = None
    rating = None
    rs_slider.setOpacity(.5)
    mouse.setPos(0,0)
    mouse.clickReset()
    # Start showing the scale
    for thisFrame in range(timeInFrames["CS"]): 
        # Draw all components of the rating scale
        for stim in rs_stims:
            stim.draw()
        # Set slider position (with limits)
        m_x, m_y = mouse.getPos()
        if m_x < _rs_min: m_x = _rs_min
        if m_x > rs_max: m_x = rs_max
        # Re-scale rating
        RATING = int(((m_x+rs_max)/rs_max)*(scale_max/2))
        rs_slider.setPos([m_x, 0])
        rs_slider.draw()
        dyn_txt.setPos([m_x, dynTxtYPos])
        dyn_txt.setText(str(RATING)+ " %")
        dyn_txt.draw()
        win.flip()
        # Listen to keyboard and mouse
        #rating = m_x  # values in degrees
        buttons, RT = mouse.getPressed(getTime=True)  # returns 3-item list and time since reset
        if not detected and buttons[0]:  # First click detected
            detected is True
            detectedRT = RT[0]
            if triggers: sendTrigger(triggerList["resp"])
            rs_slider.setOpacity(1)
            mouse.clickReset()
        if event.getKeys(['escape']): core.quit()
        #print("Rating: " + str(rating))
        #print("FrameNr: " + str(thisFrame))