#!/usr/bin/python

import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFont
import socket
import json

import os

import optparse

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
#socket.setdefaulttimeout(2.5)

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
        self.vent_state = False
        
        #Valve Setting
        self.valve_setting = "DEFAULT"

        #Pressure Transducer, Load Cell, and Thermocouple
        self.pressure = 3
        self.load = 0
        self.thermo = 0
        self.p_calibrate = 0
        self.l_calibrate = 0
        self.t_calibrae = 0

        #Ignition
        self.ignition = False

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

        #self.clientsocket.connect(address_u)
        #self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
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
        if tkMessageBox.askyesno(message="Are you sure you want to attempt ignition?"):
            if self.propulsion and self.mission_control and self.safety and self.valve_setting == "IGNITION":
                self.ignition = True
                msg = tkMessageBox.showinfo(title="IGNITION",message="IGNITION!")
            else:
                error = tkMessageBox.showwarning(title="ERROR",message="Safety requirements not met!")
                error.pack()

    def draw_valves(self):

        Fill_Button = Button(self.master,text="Toggle Fill Valve",command=lambda:self.turn_valve("fill"))
        Relief_Button = Button(self.master,text="Toggle Relief Valve",command=lambda:self.turn_valve("relief"))
        Vent_Button = Button(self.master,text="Toggle Vent Valve",command=lambda:self.turn_valve("vent"))

        Fill_Label = Label(self.master,font=self.font,text="Fill Valve")
        Relief_Label = Label(self.master,font=self.font,text="Relief Valve")
        Vent_Label = Label(self.master,font=self.font,text="Vent Valve")

        Valve_Menu = Menubutton(self.master, text="Valve State: "+self.valve_setting, anchor=CENTER,height=3,width=20)
        Valve_Menu.grid(sticky="ew",pady=8)
        Valve_Menu.menu = Menu(Valve_Menu,tearoff=0)
        Valve_Menu["menu"] = Valve_Menu.menu
        Valve_Menu.menu.add_radiobutton(label="ALL CLOSED",command=lambda:self.change_valve_setting("ALL CLOSED"))
        Valve_Menu.menu.add_radiobutton(label="ALL OPEN",command=lambda:self.change_valve_setting("ALL OPEN"))
        Valve_Menu.menu.add_radiobutton(label="FILL",command=lambda:self.change_valve_setting("FILL"))
        Valve_Menu.menu.add_radiobutton(label="RELIEF",command=lambda:self.change_valve_setting("RELIEF"))
        Valve_Menu.menu.add_radiobutton(label="IGNITION",command=lambda:self.change_valve_setting("IGNITION"))
        Valve_Menu.menu.add_radiobutton(label="DEFAULT",command=lambda:self.change_valve_setting("DEFAULT"))
        Valve_Menu.menu.add_radiobutton(label="MANUAL",command=lambda:self.change_valve_setting("MANUAL"))
        #print self.fill_state, self.relief_state, self.vent_state
        
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
                
        Fill_Button.place(anchor=N,relx=.25,rely=.1)
        Relief_Button.place(anchor=N,relx=.5,rely=.1)
        Vent_Button.place(anchor=N,relx=.75,rely=.1)
        Fill_Label.place(anchor=N,relx=.25,rely=.275)
        Relief_Label.place(anchor=N,relx=.5,rely=.275)
        Vent_Label.place(anchor=N,relx=.75,rely=.275)
        Valve_Menu.place(anchor=N,relx=.5)
        
    def turn_valve(self, valve):
        #print self.valve_setting
        if self.valve_setting == "MANUAL":
            if valve == "fill":
                self.fill_state = not self.fill_state
            elif valve == "relief":
                self.relief_state = not self.relief_state
            elif valve == "vent":
                self.vent_state = not self.vent_state
            else:
                print "That valve doesn't exist, dumbass!"
            self.draw_valves()

    def change_valve_setting(self, setting):
        #print "change_valve_setting"
        if tkMessageBox.askyesno(message="Are you sure you want to set valves to "+setting+"?"):
            self.valve_setting = setting
            if setting == "ALL CLOSED":
                self.fill_state = False
                self.relief_state = False
                self.vent_state = False
            elif setting == "ALL OPEN":
                self.fill_state = True
                self.relief_state = True
                self.vent_state = True
            elif setting == "FILL":
                self.fill_state = True
                self.relief_state = True
                self.vent_state = False
            elif setting == "RELIEF":
                self.fill_state = False
                self.relief_state = True
                self.vent_state = False
            elif setting == "IGNITION":
                self.fill_state = False
                self.relief_state = False
                self.vent_state = True
                self.draw_ignition()
            elif setting == "DEFAULT":
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

    def draw_graphs(self):
        Graph_Canvas = Canvas(self.master, width=800, height=600)

        PT_Graph = Graph_Canvas.create_line(50,280,int(50+self.pressure*(1.0/5.0)*(150)),280, fill="blue", width=20)
        LC_graph = Graph_Canvas.create_line(325,280,475,280,fill="blue",width=20)
        TC_graph = Graph_Canvas.create_line(600,280,750,280,fill="blue",width=20)
        
        PT_Label = Label(self.master, font=self.font,text="Pressure: "+str(self.pressure))
        LC_Label = Label(self.master, font=self.font,text="Load Cell: "+str(self.load))
        TC_Label = Label(self.master, font=self.font,text="Thermocouple: "+str(self.thermo))

        PT_Calibrate = Button(self.master,text="Calibrate PT",command=lambda:self.calibrate("PT"))
        LC_Calibrate = Button(self.master,text="Calibrate LC",command=lambda:self.calibrate("LC"))
        TC_Calibrate = Button(self.master,text="Calibrate TC",command=lambda:self.calibrate("TC"))
        
        PT_Label.place(anchor=N,relx=.115,rely=.5)
        LC_Label.place(anchor=N,relx=.460,rely=.5)
        TC_Label.place(anchor=N,relx=.825,rely=.5)

        PT_Calibrate.place(anchor=N,relx=.11,rely=.55)
        LC_Calibrate.place(anchor=N,relx=.45,rely=.55)
        TC_Calibrate.place(anchor=N,relx=.80,rely=.55)

        Graph_Canvas.pack()

    def calibrate(self, sensor):
        pass
        
    def update_frames(self):
        self.draw_graphs()
        self.draw_checks()
        self.draw_ignition()
        self.draw_valves()
        #self.draw_menus()

    def send_data(self):
        dic = {'Fill':self.fill_state, 'Relief':self.relief_state, 'Vent':self.vent_state, 'Ignition':self.ignition}
        out = json.dumps(dic)

        print "STATUS:\n"
        print out

        self.clientsocket.sendto(out, address_u)
        #self.clientsocket.send(out)

    def recv_data(self):
        print "begin recv"

        received, addr = self.clientsocket.recvfrom(1024)
        #received = self.clientsocket.recv(1024)

        print "RECEIVED:\n"
        print received
        try:
            data = json.loads(received)
            print "DATA:\n"
            print data
            self.pressure = data["pressure"]
            self.load = data["load"]
            self.thermo = data["thermo"]
        except:
            print "Failed to receive data"

root = tk.Tk()
root.resizable(width=False,height=False)
main_app = MainApp(root)
main_app.update_frames()
root.geometry('800x600')

while True:
    main_app.recv_data()
    root.update_idletasks()
    root.update()
    main_app.send_data()