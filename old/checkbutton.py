from Tkinter import *

master = Tk()

var = BooleanVar()

def cb():
    print "variable is {0}".format(var.get())

c = Checkbutton(master, text="Press me", variable=var, command=cb)
c.pack()

mainloop()
