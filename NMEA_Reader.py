#!/usr/bin/python
#-*- coding: utf8 -*-

def getLocation(readPort,readSpeed):
    ser = serial.Serial(readPort,readSpeed)  ##read sentence from device
    while 1:      ##keep reading until get a result could be return
        serial_line = ser.readline()
        information=serial_line.split(",")
        if information[0] == stableSen and (information[2] == '2' or information[2] == '3' or information[2] == '1'): ##if signal is strong enough
            lookingPosition = True
            lookingSpeed = True
            while lookingPosition or lookingSpeed:     ##looking for position sentece
                serial_line = ser.readline()
                information=serial_line.split(",")
                if information[0] == speedSen:
                    speedInfo = information[7]
                    lookingSpeed = False
                ##check position sentence and is active
                if information[0] == locationSen and information[2] == 'A': 
                    locationInfo = formatLocation(information)
                    lookingPosition = False
            
            return locationInfo + ',' + speedInfo