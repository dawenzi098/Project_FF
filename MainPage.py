#!/usr/bin/python
#-*- coding: utf8 -*-
from Tkinter import *
import NMEA_Reader 
import Client_State_Reader

# Global Variable and handler
LOGO_IMAGE_ADDRESS = "logo.gif"
Read_Taggle = 0
EnableGPS_Taggle = 0
EnableSpeed_Taggle = 0
socket_handler = None

# Callback function
def Reading():
    global Read_Taggle
    readCycle_var_ms = int(readCycle_var.get()) * 1000
    if (Read_Taggle == 1):
        GPS_info = NMEA_Reader.getLocation(enableGPS_var.get(),enableSpeed_var,serialport_var.get(),int(baudrate_var.get()))
        Device_info = Client_State_Reader.Get_parameters(socket_handler)
        info = GPS_info + ',' + Device_info
        print info
        Client_State_Reader.save_data(info)
        mainWin.after(readCycle_var_ms,Reading)     

def Stop_Command():
    global Read_Taggle
    global socket_handler
    Read_Taggle = 0
    # Close the socket
    Client_State_Reader.socket_uninit(socket_handler)

def Start_Command():
    global Read_Taggle
    global socket_handler
    Read_Taggle = 1
    # Initial the socket and start reading
    socket_handler = Client_State_Reader.socket_init(deviceIP_var.get(),32921)
    Reading()

def EnableGPS():
    global EnableGPS_Taggle
    if EnableGPS_Taggle == 0:
        EnableGPS_Taggle = 1
    else:
        EnableGPS_Taggle = 0
        EnableSpeed_Checkbutton.deselect()
    #print "GPS-->" + str(enableGPS_var.get())

def EnableSpeed():
    global EnableSpeed_Taggle
    if EnableSpeed_Taggle == 0:
        EnableSpeed_Taggle = 1
    else:
        EnableSpeed_Taggle = 0
    #print "Speed-->" + str(enableSpeed_var.get())


# main window
mainWin=Tk()
mainWin.title("Client State Reader")
mainWin.geometry('300x220')

# Variable 
baudrate_var = StringVar()
serialport_var = StringVar()
readCycle_var = StringVar()
deviceIP_var = StringVar()
enableGPS_var = IntVar()
enableSpeed_var = IntVar()

# create some frame 
logo_Frame=Frame(mainWin)
logo_Frame.pack(side=TOP)

input_Frame=Frame(mainWin)
input_Frame.pack(padx=8,ipadx=4)

button_Frame=Frame(mainWin)
button_Frame.pack(side=BOTTOM)

# Add logo
logo_PhotoImage=PhotoImage(file=LOGO_IMAGE_ADDRESS)
logo_Label=Label(logo_Frame,image=logo_PhotoImage)
logo_Label.grid(row=0,column=1,columnspan=3,pady=8)

# Add labels and entries.
baudrate_var_Label=Label(input_Frame,text="GPS baudrate:")
baudrate_var_Label.grid(row=1,column=0,columnspan=2)
baudrate_var_Entry=Entry(input_Frame,textvariable=baudrate_var)
baudrate_var.set("115200")
baudrate_var_Entry.grid(row=1,column=2,columnspan=2)


serialport_var_Label=Label(input_Frame,text="GPS Serial Port:")
serialport_var_Label.grid(row=2,column=0,columnspan=2)
serialport_var_Entry=Entry(input_Frame,textvariable=serialport_var)
serialport_var.set("COM")
serialport_var_Entry.grid(row=2,column=2,columnspan=2)


deviceIP_var_Label=Label(input_Frame,text="Device IP:")
deviceIP_var_Label.grid(row=3,column=0,columnspan=2)
deviceIP_var_Entry=Entry(input_Frame,textvariable=deviceIP_var)
deviceIP_var.set("169.254.0.9")
deviceIP_var_Entry.grid(row=3,column=2,columnspan=2)


readCycle_var_Label=Label(input_Frame, text="Read Cycle(s):")
readCycle_var_Label.grid(row=4,column=0,columnspan=2)
readCycle_var_Entry=Entry(input_Frame,textvariable=readCycle_var)
readCycle_var.set("5")
readCycle_var_Entry.grid(row=4,column=2,columnspan=2)


#Check box for enable GPS and speed module
EnableGPS_Checkbutton=Checkbutton(input_Frame,text="Enable GPS",command=EnableGPS,variable=enableGPS_var)
EnableGPS_Checkbutton.grid(row=5,column=0)

EnableSpeed_Checkbutton=Checkbutton(input_Frame,text="Enable Speed Module",command=EnableSpeed,variable=enableSpeed_var)
EnableSpeed_Checkbutton.grid(row=5,column=3)

# Add two buttons, one for test, other for real run.
Test_Button=Button(button_Frame,text="Start",command=Start_Command)
Test_Button.grid(row=0,column=0,columnspan=2,padx=30,pady=10)
Read_Button=Button(button_Frame,text="Stop",command=Stop_Command)
Read_Button.grid(row=0,column=2,columnspan=2,padx=30,pady=10)

mainWin.mainloop()
