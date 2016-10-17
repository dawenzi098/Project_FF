#!/usr/bin/python
#-*- coding: utf8 -*-
from Tkinter import *
#from NMEA_Reader import *
import time

LOGO_IMAGE_ADDRESS = "logo.gif"

Read_Taggle = 0

# Callback function
def Reading():
    global Read_Taggle
    if (Read_Taggle == 1):
        print "Running"
        mainWin.after(1000,Reading)           

def Stop_Command():
    #print "Test! Reading Speed-->" + ReadingSpeed_Entry.get() + ". Serial Port-->" + Serialport_Entry.get() + ". Read Cycle-->" + ReadCycle_Entry.get() + "."
    global Read_Taggle
    Read_Taggle = 0

def Start_Command():
    global Read_Taggle
    Read_Taggle = 1
    Reading()

# main window
mainWin=Tk()
mainWin.title("GPS Reader")
mainWin.geometry('300x200')

# Variable 
readingSpeed = StringVar()
serialport = StringVar()
readCycle = StringVar()

# create some frame 
logo_Frame=Frame(mainWin)
logo_Frame.pack(side=TOP)

input_Frame=Frame(mainWin)
input_Frame.pack(padx=8,pady=8,ipadx=4)

button_Frame=Frame(mainWin)
button_Frame.pack(side=BOTTOM)

# Add logo
logo_PhotoImage=PhotoImage(file=LOGO_IMAGE_ADDRESS)
logo_Label=Label(logo_Frame,image=logo_PhotoImage)
logo_Label.grid(row=0,column=1,columnspan=3,pady=8)

# Add labels and entries.
ReadingSpeed_Label=Label(input_Frame,text="Baudrate:")
ReadingSpeed_Label.grid(row=1,column=0,columnspan=2)
ReadingSpeed_Entry=Entry(input_Frame,textvariable=readingSpeed)
ReadingSpeed_Entry.grid(row=1,column=2,columnspan=2)


Serialport_Label=Label(input_Frame,text="GPS Serial Port:")
Serialport_Label.grid(row=2,column=0,columnspan=2)
Serialport_Entry=Entry(input_Frame,textvariable=serialport)
Serialport_Entry.grid(row=2,column=2,columnspan=2)


ReadCycle_Label=Label(input_Frame, text="Read Cycle(s):")
ReadCycle_Label.grid(row=3,column=0,columnspan=2)
ReadCycle_Entry=Entry(input_Frame,textvariable=readCycle)
ReadCycle_Entry.grid(row=3,column=2,columnspan=2)

# Add two buttons, one for test, other for real run.
Test_Button=Button(button_Frame,text="Start",command=Start_Command)
Test_Button.grid(row=0,column=0,columnspan=2,padx=30,pady=15)
Read_Button=Button(button_Frame,text="Stop",command=Stop_Command)
Read_Button.grid(row=0,column=2,columnspan=2,padx=30,pady=15)

mainWin.mainloop()
