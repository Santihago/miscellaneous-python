#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from psychopy import visual

# Best fixation cross from Thales, Shutz, Goodale & Gegenfurtner (2013)
# Combination of bulls eye and cross hair
# Produces highest stability of gaze
# heard about it from blog.johnkiat.com who provides a .png with the cross
# here I wanted to recreate it entirely in python/psychopy for full flexibility 
# of color and size

# it consists of three different layers, bigger circle, cross and smaller circle
# can be adjusted to visual degrees by changing the win units, but will require
# monitor dimensions

win = visual.Window([400, 300], color = 'Gray', units = 'pix')  # For testing only

cRad = 13

# create a big circle
a = visual.Circle(win, radius=cRad, lineColor = 'black', fillColor = 'black')
# add a cross inside
b = visual.ShapeStim(win,
                    vertices = ((-cRad, -cRad/10), (-cRad/10, -cRad/10),
                    (-cRad/10, -cRad), (cRad/10, -cRad), (cRad/10, -cRad/10),
                    (cRad, -cRad/10), (cRad, cRad/10), (cRad/10, cRad/10), 
                    (cRad/10, cRad), (-cRad/10, cRad), (-cRad/10, cRad/10), 
                    (-cRad, cRad/10)),
                    lineWidth = 1, 
                    lineColor = 'white',
                    fillColor = 'white')
# add a small dot inside
c = visual.Circle(win, radius=cRad/12, lineColor = 'black', fillColor = 'black')

# Show on screen
a.draw()
b.draw()
c.draw()
win.flip()