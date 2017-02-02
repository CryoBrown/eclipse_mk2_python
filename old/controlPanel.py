#!/usr/bin/python

#import glob
#import os
#import re
#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from matplotlib.figure import Figure
#from matplotlib import style
#import matplotlib.dates as mdates
#import datetime
#import numpy as np
#from datetime import datetime
import Tkinter as tk
import ttk
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.PWM  as PWM

gpio = GPIO.get_platform_gpio()
pwm = PWM.get_platform_pwm()

MAINPIN = 19#"P9_23"
RELIEFPIN = 16#"P9_25"
VENTPIN = 26#"P9_14"
IGNITIONPIN = 20#"P9_30"

# style.use("ggplot")

lastframe = ''
LARGE_FONT = ("Helvetica", 12, "bold")
SMALL_FONT = ("Helvetica", 10, "bold")

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(11, GPIO.out)

# fignamelist = ["ping", "RSRP", "RSRQ", "RSSI", "SNR", "TX", "RX"]
# figlist = {name:Figure(figsize=(2,1), dpi=60) for name in fignamelist}
# sublist = {name:figlist[name].add_subplot(111) for name in fignamelist}
# axlist = {name:figlist[name].gca() for name in fignamelist}

# def animate(figure, subplot, axis, x_set, y_set):

#   subplot.clear()
#   subplot.plot(x_set, y_set)
#   figure.autofmt_xdate()
#   axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

class mainApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand="True")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [ControlPanel]:
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ControlPanel)

    def show_frame(self, cont):
        global lastframe
        lastframe = cont
        frame = self.frames[cont]
        frame.tkraise()

class ControlPanel(tk.Frame):

    def __init__(self, parent, controller):
        #Solenoid Valves
        mainv = RealValve(MAINPIN)
        reliefv = RealValve(RELIEFPIN)

        #This will be a ServoValve in actual setup
        ventv = ServoValve(VENTPIN)

        #Ignition
        ignition = Ignition(IGNITIONPIN)

        tk.Frame.__init__(self, parent)

        #buttnames = ['Close All', 'Open All', 'Fill', 'Relief' 'Light a fire']
        buttnames = ['Close All', 'Open All', 'Close Main', 'Open Main', 'Close Relief', 'Open Relief', 'Close Vent', 'Open Vent', 'Start Ignition', 'Stop Ignition']
        def closeAll():
            mainv.close()
            reliefv.close()
            ventv.close()

        def openAll():
            mainv.open()
            reliefv.open()
            ventv.open()

        buttfuncs = [closeAll, openAll, mainv.close, mainv.open, reliefv.close, reliefv.open, ventv.close, ventv.open, ignition.start, ignition.stop]

        buttlist = [None]*len(buttnames)

        for i in xrange(len(buttnames)):
            buttlist[i] = tk.Button(self, text=buttnames[i], command=buttfuncs[i])

        alllabel = tk.Label(self, text='All Valves')
        mainlabel = tk.Label(self, text='Main Valve')
        relieflabel = tk.Label(self, text='Relief Valve')
        ventlabel = tk.Label(self, text='Vent Valve')
        ignlabel = tk.Label(self, text='Ignition')

        alllabel.grid(row=0, columnspan=3, pady=5)
        mainlabel.grid(row=2, columnspan=3, pady=5)
        relieflabel.grid(row=4, columnspan=3, pady=5)
        ventlabel.grid(row=6, columnspan=3, pady=5)
        ignlabel.grid(row=8, columnspan=3, pady=5)

        buttlist[0].grid(row=1, column=0)
        buttlist[1].grid(row=1, column=1)
        buttlist[2].grid(row=3, column=0)
        buttlist[3].grid(row=3, column=1)
        buttlist[4].grid(row=5, column=0)
        buttlist[5].grid(row=5, column=1)
        buttlist[6].grid(row=7, column=0)
        buttlist[7].grid(row=7, column=1)
        buttlist[8].grid(row=9, column=0)
        buttlist[9].grid(row=9, column=1)

class RealValve:

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)

    def open(self):
        gpio.output(self.pin, GPIO.HIGH)

    def close(self):
        gpio.output(self.pin, GPIO.LOW)

class Ignition:

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)

    def start(self):
        gpio.output(self.pin, GPIO.HIGH)

    def stop(self):
        gpio.output(self.pin, GPIO.LOW)

class ServoValve:

    def __init__(self, pin):
        self.pin = pin

    def open(self):
        pwm.start(self.pin, 15, 100)
        pwm.stop(self.pin)

    def close(self):
        pwm.start(self.pin, 10, 100)
        pwm.stop(self.pin)

app = mainApp()
app.geometry('800x600')
app.mainloop()
