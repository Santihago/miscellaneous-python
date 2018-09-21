from __future__ import division
from psychopy import visual, core, event

"""
Creating my own rating scale for full flexibility.
Guidelines from Matejka 2016: No ticks (use bands), 2 labels, dynamic text
feedback
"""

#open a window
win = visual.Window([800, 600], color='Gray', units='deg')
#create a mouse object
mouse = event.Mouse(visible=True, win=win)

#--------------
# RATING SCALE
#--------------

#------------- You can adjust these
rs_size = 14 #scale size in degrees of visual angle (DVA)
scale_max = 100 #maximum rating in the rating scale (int)
rs_col = '#373F51'  #charcoal color
rs_txt_col = '#373F51'
rs_txt_size = .7  #text height in dva
labelsYPos = -1  #y position (in DVA) of text labels
dynTxtYPos = 1 #y position (in DVA) of dynamic rating text
labels = ["0 %", "100 %"]  #text value of scale labels
labels_pos = [-1, 1]  #pos values from -1 to 1
ticks_pos = [-.5, 0, .5]  #pos values of ticks/bands

#------------- No need to adjust these
_rs_max = rs_size/2  #scale rightmost value
_rs_min = (-1 * _rs_max)  #scale leftmost value
rs_stims = []  #scale stimuli list
#horizontal bar
rs_stims += [visual.Rect(win, width=_rs_max*2, height=.1, fillColor = rs_col,
             lineColor = rs_col)]
#add text labels
labelsXPos = [x * _rs_max for x in labels_pos]
for nr, thisXPos in enumerate(labelsXPos):
    rs_stims += [visual.TextStim(win, text=labels[nr], height=rs_txt_size,
                 pos = [thisXPos, labelsYPos], color = rs_txt_col)]
#add ticks / bands
ticksXPos = [x * _rs_max for x in ticks_pos]
for thisXPos in ticksXPos: # Mini-ticks
    rs_stims += [visual.Rect(win, width=1, height=.25, pos = [thisXPos, 0], 
                 fillColor = rs_col, opacity = .75)]
#moving slider
rs_slider = visual.Rect(win, width=.25, height=1., fillColor = rs_col,
                        lineColor = rs_col)
#moving text
dyn_txt = visual.TextStim(win, text=u"", height=rs_txt_size, color = rs_txt_col)

#--------------------------------------
# Preparation before showing the scale
#--------------------------------------

#prepare and reset between repeated uses of the same scale
event.clearEvents()
detected = False
detectedRT = None
RATING = None
ratings_thisTrial = []  #continuous rating vector
rs_slider.setFillColor('#FEFFFA')
mouse.setPos([0,0])
mouse.clickReset() 

#start showing the scale    
while True:

    #draw all components of the rating scale
    for stim in rs_stims:
        stim.draw()
    #set slider and dynamic text position to mouse and draw 
    m_x, m_y = mouse.getPos()
    if m_x < _rs_min: m_x = _rs_min  #clipped -X position
    if m_x > _rs_max: m_x = _rs_max  #clipped +X position
    rs_slider.setPos([m_x, 0])
    rs_slider.draw()
    #re-scale rating value to given range
    RATING = int(((m_x+_rs_max)/_rs_max)*(scale_max/2))
    #draw value of rating on the screen at mouse position
    dyn_txt.setPos([m_x, dynTxtYPos])
    dyn_txt.setText(str(RATING)+ " %")
    dyn_txt.draw()
    #flip everything
    win.flip()
    
    #listen to mouse click and record timestamp
    buttons, RT = mouse.getPressed(getTime=True)  #returns 3-item list and time since reset
    if not detected and buttons[0]:  #first click detected
        detected = True
        detectedRT = round(RT[0], 2)  #timestamp
        rs_slider.setFillColor('#1A7AF8')  #change slider color to blue
        mouse.clickReset()  #reset mouse
    #save continuous rating sampled at each frame in a vector
    ratings_thisTrial.append(RATING)
    
    if event.getKeys(['escape']): core.quit()