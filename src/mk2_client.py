#!/usr/bin/python

import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFont
import socket
import json

import os

import optparse

DRAW_RATE = 5

parser = optparse.OptionParser()

parser.add_option('--s', action="store", dest="server", help="ip address", default = "127.0.0.1")
parser.add_option('--c', action="store", dest="client", help="ip address", default = "127.0.0.1")
options, args = parser.parse_args()
print "SERVER IP:", options.server
print "CLIENT IP:", options.client

parent = os.path.pardir
assets = os.path.join(parent, "assets")
output = os.path.join(parent, "output")

address_me = (options.client, 5005)
address_u = (options.server, 5004)
socket.setdefaulttimeout(2.5)

class MainApp:

    def __init__(self, m):
        self.master = m
        self.font = tkFont.Font(family="Helvetica", size=12)

        #Software Safety Checks
        self.propulsion = False
        self.mission_control = False
        self.safety = False

        #Valve States
        self.fill_state = False
        self.relief_state = True
        self.relief_power = True
        self.vent_state = False

        #Valve Setting
        self.valve_setting = "DEFAULT"
        self.valve_var = IntVar()

        #Pressure Transducer, Load Cell, and Thermocouple
        self.pressure = 0
        self.load = 0
        self.thermo = 0
        self.l_calibrate = [[1001, 0.0], [1122, 32.8]]
        self.p_calibrate = [[0,0],[1,1]]
        self.t_calibrate = [[0,0],[1,1]]

        deltax = (self.l_calibrate[0][0]-self.l_calibrate[1][0])
        deltay = (self.l_calibrate[0][1]-self.l_calibrate[1][1])

        if deltax == 0:
            self.LC_slope = 1
            self.LC_y_intercept = 0
        else:
            self.LC_slope = deltay/deltax
            self.LC_y_intercept = self.l_calibrate[0][1]-self.l_calibrate[0][0]*self.LC_slope

        self.PT_slope = 1
        self.PT_y_intercept = 0

        self.PT_str = tk.StringVar()
        self.LC_str = tk.StringVar()
        self.TC_str = tk.StringVar()

        #Ignition
        self.ignition = False

        #Heating
        self.heating = False

        #Default values
        self.set_safety_defaults()

        #Images
        self.gobutton = PhotoImage(file=os.path.join(assets, "redbutton.gif"))
        self.nobutton = PhotoImage(file=os.path.join(assets, "blackbutton.gif"))
        self.opened = PhotoImage(file=os.path.join(assets, "opened.gif"))
        self.closed = PhotoImage(file=os.path.join(assets, "closed.gif"))

        #Client Socket
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientsocket.bind(address_me)

    def set_safety_defaults(self):
        self.propulsion = False
        self.mission_control = False
        self.safety = False
        self.ignition = False

        self.fill_state = False
        self.relief_state = True
        self.vent_state = False

    def draw_checks(self):

        def p():
            self.propulsion = not self.propulsion
            #print "propulsion is", self.propulsion
            self.draw_ignition()

        def m():
            self.mission_control = not self.mission_control
            #print "mission control is", self.mission_control
            self.draw_ignition()

        def s():
            self.safety = not self.safety
            #print "safety is ", self.safety
            self.draw_ignition()

        Propulsion_Check = Checkbutton(self.master,text="Propulsion GO",command=p,padx=25)
        Mission_Control_Check = Checkbutton(self.master,text="Mission Control GO",command=m,padx = 25)
        Safety_Check = Checkbutton(self.master,text="Range Safety Officer GO",command=s,padx =25)

        Propulsion_Check.place(anchor=N,relx=.25,rely=.95)
        Mission_Control_Check.place(anchor=N,relx=.5,rely=.95)
        Safety_Check.place(anchor=N,relx=.75,rely=.95)

    def draw_ignition(self):
        Ignition_Button = Button(self.master, command = self.attempt_ignition)

        if self.propulsion and self.mission_control and self.safety and self.valve_setting == "IGNITION":
            Ignition_Button.configure(image=self.gobutton)
        else:
            Ignition_Button.configure(image=self.nobutton)

        Ignition_Button.place(anchor=N,relx=.5,rely=.7)

    def attempt_ignition(self):
        #if tkMessageBox.askyesno(message="Are you sure you want to attempt ignition?"):
        if self.propulsion and self.mission_control and self.safety and self.valve_setting == "PRE-IGNITION":
            self.ignition = True
            msg = tkMessageBox.showinfo(title="IGNITION",message="IGNITION!")
        else:
            tkMessageBox.showwarning(title="ERROR",message="Safety requirements not met!")

    def draw_valves(self):

        def heat():
            self.heating = not self.heating

        Fill_Button = Button(self.master,text="Toggle Fill Valve",command=lambda:self.turn_valve("fill"))
        Relief_Button = Button(self.master,text="Toggle Relief Valve",command=lambda:self.turn_valve("relief"))
        Vent_Button = Button(self.master,text="Toggle Vent Valve",command=lambda:self.turn_valve("vent"))
        Heat_Button = Button(self.master,text="Heating Tape",command=heat,height=3,width=10)
        Fill_Label = Label(self.master,font=self.font,text="Fill Valve")
        Relief_Label = Label(self.master,font=self.font,text="Relief Valve")
        Vent_Label = Label(self.master,font=self.font,text="Vent Valve")

        Closed_State = Radiobutton(self.master,text="ALL CLOSED",width=10,var=self.valve_var,value=0,command=lambda:self.change_valve_setting("ALL CLOSED"))
        Open_State = Radiobutton(self.master,text="ALL OPEN",width=10,var=self.valve_var,value=1,command=lambda:self.change_valve_setting("ALL OPEN"))
        Fill_State = Radiobutton(self.master,text="FILL",width=10,var=self.valve_var,value=2,command=lambda:self.change_valve_setting("FILL"))
        Relief_State = Radiobutton(self.master,text="RELIEF",width=10,var=self.valve_var,value=3,command=lambda:self.change_valve_setting("RELIEF"))
        Pre_Ignition_State = Radiobutton(self.master,text="PRE-IGNITION",width=10,var=self.valve_var,value=4,command=lambda:self.change_valve_setting("PRE-IGNITION"))
        Default_State = Radiobutton(self.master,text="DEFAULT",width=10,var=self.valve_var,value=5,command=lambda:self.change_valve_setting("DEFAULT"))
        Manual_State = Radiobutton(self.master,text="MANUAL",width=10,var=self.valve_var,value=6,command=lambda:self.change_valve_setting("MANUAL"))

        Closed_State.place(anchor=N,relx=.12,rely=.035)
        Open_State.place(anchor=N,relx=.25,rely=.035)
        Fill_State.place(anchor=N,relx=.38,rely=.035)
        Relief_State.place(anchor=N,relx=.51,rely=.035)
        Pre_Ignition_State.place(anchor=N,relx=.64,rely=.035)
        Default_State.place(anchor=N,relx=.77,rely=.035)
        Manual_State.place(anchor=N,relx=.90,rely=.035)
        #print self.valve_setting

        if self.fill_state:
            Fill_Button.configure(image=self.opened)
        else:
            Fill_Button.configure(image=self.closed)

        if self.relief_state:
            Relief_Button.configure(image=self.opened)
        else:
            Relief_Button.configure(image=self.closed)

        if self.vent_state:
            Vent_Button.configure(image=self.opened)
        else:
            Vent_Button.configure(image=self.closed)

        def relief_power():
            self.relief_power = not self.relief_power

        Relief_Power_Button = Button(self.master,text="Relief Power",command=relief_power)
        Relief_Power_Button.place(anchor=N,relx=.375,rely=.2)

        Fill_Button.place(anchor=N,relx=.25,rely=.1)
        Relief_Button.place(anchor=N,relx=.5,rely=.1)
        Vent_Button.place(anchor=N,relx=.75,rely=.1)
        Fill_Label.place(anchor=N,relx=.25,rely=.275)
        Relief_Label.place(anchor=N,relx=.5,rely=.275)
        Vent_Label.place(anchor=N,relx=.75,rely=.275)

        Heat_Button.place(anchor=N,relx=.5,rely=.33)

    def turn_valve(self, valve):
        #print self.valve_setting
        if self.valve_setting == "MANUAL":
            if valve == "fill":
                self.fill_state = not self.fill_state
            elif valve == "relief":
                self.relief_state = not self.relief_state
            elif valve == "vent":
                self.vent_state = not self.vent_state
            self.draw_valves()

    def change_valve_setting(self, setting):
        #print "change_valve_setting"
        self.valve_setting = setting
        #if tkMessageBox.askyesno(message="Are you sure you want to set valves to "+self.valve_setting+"?"):
        if self.valve_setting == "ALL CLOSED":
            self.fill_state = False
            self.relief_state = False
            self.vent_state = False
        elif self.valve_setting == "ALL OPEN":
            self.fill_state = True
            self.relief_state = True
            self.vent_state = True
        elif self.valve_setting == "FILL":
            self.fill_state = True
            self.relief_state = True
            self.vent_state = False
        elif self.valve_setting == "RELIEF":
            self.fill_state = False
            self.relief_state = True
            self.vent_state = False
        elif self.valve_setting == "PRE-IGNITION":
            self.fill_state = False
            self.relief_state = False
            self.vent_state = True
            self.draw_ignition()
        elif self.valve_setting == "DEFAULT":
            self.fill_state = False
            self.relief_state = True
            self.vent_state = False
        self.draw_valves()

    def draw_menus(self):
        menubar = Menu(self.master)
        filemenu = Menu(self.master, tearoff=0)
        filemenu.add_command(label="New",)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Close")

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

    def display_readings(self):
        self.PT_str.set("Pressure: "+str(round(self.pressure*self.PT_slope+self.PT_y_intercept, 1)))
        self.LC_str.set("Load Cell: "+str(round(self.load*self.LC_slope+self.LC_y_intercept, 1)))
        self.TC_str.set("Thermocouple: "+str(self.thermo))

    def make_calibrators(self):
        #Graph_Canvas = Canvas(self.master, width=800, height=600)

        #PT_Graph = Graph_Canvas.create_line(50,280,int(50+self.pressure*(1.0/5.0)*(150)),280, fill="blue", width=20)
        #LC_graph = Graph_Canvas.create_line(325,280,int(325+self.load*(1.0/5.0)*(150)),280,fill="blue",width=20)
        #TC_graph = Graph_Canvas.create_line(600,280,int(600+self.thermo*(1.0/5.0)*(150)),280,fill="blue",width=20)

        self.display_readings()

        PT_Label = Label(self.master, font=self.font,width=30,textvariable=self.PT_str)
        LC_Label = Label(self.master, font=self.font,width=30,textvariable=self.LC_str)
        TC_Label = Label(self.master, font=self.font,textvariable=self.TC_str)

        PT_Label.place(anchor=N,relx=.115,rely=.5)
        LC_Label.place(anchor=N,relx=.460,rely=.5)
        TC_Label.place(anchor=N,relx=.825,rely=.5)

        def calibrate_sensor(sensor, index):
            if sensor == "PT":
                self.p_calibrate[index] = [self.pressure, float(PT_Entry.get())]

                deltax = (self.p_calibrate[0][0]-self.p_calibrate[1][0])
                deltay = (self.p_calibrate[0][1]-self.p_calibrate[1][1])

                if deltax == 0:
                    self.PT_slope = 1
                    self.PT_y_intercept = 0
                else:
                    self.PT_slope = deltay/deltax
                    self.PT_y_intercept = self.p_calibrate[0][1]-self.p_calibrate[0][0]*self.PT_slope
            if sensor == "LC":
                self.l_calibrate[index] = [self.load, float(LC_Entry.get())]

                deltax = (self.l_calibrate[0][0]-self.l_calibrate[1][0])
                deltay = (self.l_calibrate[0][1]-self.l_calibrate[1][1])

                if deltax == 0:
                    self.LC_slope = 1
                    self.LC_y_intercept = 0
                else:
                    self.LC_slope = deltay/deltax
                    self.LC_y_intercept = self.l_calibrate[0][1]-self.l_calibrate[0][0]*self.LC_slope
                print self.l_calibrate
            if sensor == "TC":
                self.p_calibrate[index] = [self.pressure, float(PT_Entry.get())]
                print self.t_calibrate





        PT_C0 = Button(self.master,text="Calibrate 1",command=lambda:calibrate_sensor("PT",0))
        LC_C0 = Button(self.master,text="Calibrate 1",command=lambda:calibrate_sensor("LC",0))
        TC_C0 = Button(self.master,text="Calibrate 1",command=lambda:calibrate_sensor("TC",0))

        PT_Calibrate = Button(self.master,text="Calibrate 2",command=lambda:calibrate_sensor("PT",1))
        LC_Calibrate = Button(self.master,text="Calibrate 2",command=lambda:calibrate_sensor("LC",1))
        TC_Calibrate = Button(self.master,text="Calibrate 2",command=lambda:calibrate_sensor("TC",1))

        PT_Entry = Entry(self.master,width=10)
        LC_Entry = Entry(self.master,width=10)
        TC_Entry = Entry(self.master,width=10)
        PT_Entry.place(anchor=N,relx=.11,rely=.55)
        LC_Entry.place(anchor=N,relx=.45,rely=.55)
        TC_Entry.place(anchor=N,relx=.80,rely=.55)

        PT_C0.place(anchor=N,relx=.11,rely=.6)
        LC_C0.place(anchor=N,relx=.45,rely=.6)
        TC_C0.place(anchor=N,relx=.80,rely=.6)

        PT_Calibrate.place(anchor=N,relx=.21,rely=.6)
        LC_Calibrate.place(anchor=N,relx=.55,rely=.6)
        TC_Calibrate.place(anchor=N,relx=.90,rely=.6)

        #Graph_Canvas.pack()

    def update_frames(self):
        #self.draw_graphs()
        self.draw_checks()
        self.draw_ignition()
        self.draw_valves()
        #self.draw_menus()

    def send_data(self):
        dic = {'fill':self.fill_state, 'relief':self.relief_state, 'relief_enable':self.relief_power, 'vent':self.vent_state, 'ignition':self.ignition, 'heater_enable':self.heating}
        out = json.dumps(dic)

        #print "STATUS:\n"
        #print out

        self.clientsocket.sendto(out, address_u)
        
    def recv_data(self):
        #print "begin recv"

        received, addr = self.clientsocket.recvfrom(1024)

        try:
            data = json.loads(received)
            #print "DATA:\n"
            #print data
            self.pressure = data["pressure"]
            self.load = data["load"]
            self.thermo = data["thermo"]
        except:
            pass
            #print "Failed to receive data"

root = tk.Tk()
root.resizable(width=False,height=False)
main_app = MainApp(root)
main_app.update_frames()
root.geometry('800x600')

main_app.make_calibrators()

i = 0
while True:
    #print i
    main_app.recv_data()
    if (i % DRAW_RATE == 0): main_app.display_readings()

    root.update_idletasks()
    root.update()
    main_app.send_data()
    i = (i + 1)
