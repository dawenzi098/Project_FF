#!/usr/bin/python
#-*- coding: utf8 -*-
from Tkinter import *
import tkMessageBox

def callback():
    tkMessageBox.showinfo("Python command","Hello,Tkinter")



mainWin=Tk()

# change the title of main window
mainWin.title("Hello,Tkinter!")

# set some button.
Button(mainWin, text="Button-BackColor",bg="red").pack()

Button(mainWin, text="Button-State",state=DISABLED).pack()

Button(mainWin, text="Button-Position", compound="left",bitmap="error").pack()

Button(mainWin, text="Button-Hello", fg="blue",bd=2,width=28,command=callback).pack()

Button(mainWin, text ="Button-Color",anchor = 'sw',width = 30,height = 2).pack()

mainWin.mainloop()