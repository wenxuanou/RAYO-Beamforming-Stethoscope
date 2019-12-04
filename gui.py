#!/usr/bin/env python
# -*- coding: utf-8 -*-

import soundcard as sc

# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
from random import randrange, uniform
import pyqtgraph as pg
from scipy.signal import lfilter
import scipy.io as sio
#import serial
Num = sio.loadmat('lpf.mat')
Num = Num['Num']
# get a list of all speakers:
speakers = sc.all_speakers()
# get the current default speaker on your system:
default_speaker = sc.default_speaker()
# get a list of all microphones:
mics = sc.all_microphones()
# get the current default microphone on your system:
default_mic = sc.default_microphone()




# Create object serial port
portName = "COM12"                      # replace this port name by yours!
baudrate = 9600
#ser = serial.Serial(portName,baudrate)

### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Signal from serial port") # creates a window
p = win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
p.setYRange(-0.002,0.002)
curve = p.plot()                        # create an empty "plot" (a curve to plot)

windowWidth = 500                      # width of the window displaying the curve
Xm = linspace(0,0,windowWidth)          # create array that will contain the relevant time series
ptr = -windowWidth                      # set first x position

# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global curve, ptr, Xm

    # alternatively, get a `Recorder` and `Player` object
    # and play or record continuously:
    with default_mic.recorder(samplerate=48000) as mic:
    #, default_speaker.player(samplerate=48000) as sp:
        for _ in range(5):
            value = mic.record(numframes=32)   #1024 samples
            #value[:,0] = lfilter(Num[0], 1, value[:,0])
            #value[:,1] = lfilter(Num[0], 1, value[:,1])
            #sp.play(value)

        (row,col) = value.shape
        for i in range(row):
            Xm[:-1] = Xm[1:]                      # shift data in the temporal mean 1 sample left
            #value = ser.readline()                # read line (single value) from the serial port
            # value = uniform(0, 10)

#            Xm[-1] = float(value)                 # vector containing the instantaneous values
            Xm[-1] = float(value[i,0])
            ptr += 1                              # update x position for displaying the curve


    curve.setData(Xm)                     # set the curve with this data
    curve.setPos(ptr,0)                   # set x position in the graph to 0
    QtGui.QApplication.processEvents()    # you MUST process the plot now

### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot
while True: update()

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################
