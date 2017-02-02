#!/usr/bin/python

import Tkinter as tk
from Tkinter import *
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.PWM as PWM

gpio = GPIO.get_platform_gpio()
pwm = PWM.get_platform_pwm()

MAINPIN = 19
RELIEFPIN = 16
VENTPIN = 26
IGNITIONPIN = 20
#GPIO.setmode(GPIO.BCM)

class MainApp:

    def __init__(self, master):
        #Check Buttons
        self.propulsion = BooleanVar()
        self.mission_control = BooleanVar()
        self.safety = BooleanVar()
        
        #Fill States
        self.fill_state = BooleanVar()
        self.relief_state = BooleanVar()
        self.manual_state = BooleanVar()

        self.propulsion.set(0)
        self.mission_control.set(0)
        self.safety.set(0)

        self.gobutton = PhotoImage(file="redbutton.gif")
        self.nobutton = PhotoImage(file="blackbutton.gif")
        
    def draw_checks(self):

        frame = Frame(root)
        #default offvalue = 0, onvalue = 1

        def p():
            print "propulsion is {0}".format(self.propulsion.get())

        def m():
            print "mission control is {0}".format(self.mission_control.get())

        def s():
            print "safety is {0}".format(self.safety.get())
            
        Propulsion_Check = Checkbutton(frame, text = "Propulsion GO", variable = self.propulsion, command = p, padx = 25)
        Mission_Control_Check = Checkbutton(frame, text = "Mission Control GO", variable = self.mission_control, command = m, padx = 25)
        Safety_Check = Checkbutton(frame, text = "Range Safety Officer GO", variable = self.safety, command = s, padx = 25)
        
        Propulsion_Check.pack(side = LEFT)
        Mission_Control_Check.pack(side = LEFT)
        Safety_Check.pack(side = LEFT)

        frame.pack(side = BOTTOM)
        

    def draw_ignition(self):
        frame = Frame(root)

        Ignition_Button = Button(frame, command = self.ignition)
        
        if self.propulsion and self.mission_control and self.safety:
            Ignition_Button.configure(image = self.gobutton)
        else:
            Ignition_Button.configure(image = self.nobutton)
            
        Ignition_Button.pack()

        frame.pack(side = BOTTOM)
    
    def ignition(self):
        if self.propulsion and self.mission_control and self.safety:
            pass

    def draw_valves(self):
        frame = Frame(root)

        Main_Button = Button(frame, text = "Toggle Main Valve", command = self.turn_valve("main"), height = 3, width = 20)
        Relief_Button = Button(frame, text = "Toggle Relief Valve", command = self.turn_valve("relief"), height = 3, width = 20)
        Vent_Button = Button(frame, text = "Toggle Vent Valve", command = self.turn_valve("vent"), height = 3, width = 20)

        Valve_State = Menubutton(frame, text = "Valve State")
        Valve_State.grid()
        Valve_State.menu = Menu(Valve_State, tearoff = 0)
        Valve_State["menu"] = Valve_State.menu

        Valve_State.menu.add_checkbutton(label = "FILL", variable = self.fill_state)
        Valve_State.menu.add_checkbutton(label = "RELIEF", variable = self.relief_state)
        Valve_State.menu.add_checkbutton(label = "MANUAL", variable = self.manual_state)
        
        Valve_State.pack(side = TOP)
        Main_Button.pack(side = LEFT)
        Relief_Button.pack(side = LEFT)
        Vent_Button.pack(side = LEFT)
        
        frame.pack()
        
    def turn_valve(self, valve):
        pass
        
    def draw_frames(self):
        self.draw_checks()
        self.draw_ignition()
        self.draw_valves()

class RealValve:

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)
        self.state = False

    def openv(self):
        gpio.output(self.pin, GPIO.HIGH)

    def close(self):
        gpio.output(self.pin, GPIO.LOW)

    def change_state(self):
        if self.state == True:
            self.open()
        else:
            self.close()

class Ignition:

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, GPIO.OUT)

        def start(self, p, m, s):
            if p and m and s:
                gpio.output(self.pin, GPIO.HIGH)

        def stop(self):
            gpio.output(self.pin, GPIO.LOW)

class ServoValve:

    def __init__(self, pin):
        self.pin = pin
        self.state = False
        
    def openv(self):
        pass
        pwm.start(self.pin, 15, 100)
        pwm.stop(self.pin)

    def close(self):
        pass
        pwm.start(self.pin, 10, 100)
        pwm.stop(self.pin)

    def change_state(self):
        if self.state == True:
            self.open()
        else:
            self.close()

root = Tk()
main_app = MainApp(root)
main_app.draw_frames()
root.geometry('800x600')
root.mainloop()

