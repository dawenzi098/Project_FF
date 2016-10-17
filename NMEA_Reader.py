#!/usr/bin/python
#-*- coding: utf8 -*-

import serial

def formatLocation(information):
    #read the abs value
    latitude = float(information[3])
    longitude = float(information[5])
    
    #convert to degree value
    latitudeDegree = latitude//100
    latitude=(latitude-latitudeDegree*100)/60+latitudeDegree
    longitudeDegree = longitude//100
    longitude=(longitude-longitudeDegree*100)/60+longitudeDegree
    
    #put direction
    if information[4] == 'S':
        latitude *= -1
    if information[6] == 'W':
        longitude *= -1
    
    return str(latitude) + ',' + str(longitude)


def getLocation(readPort,baudrate):
    ser = serial.Serial(readPort,baudrate)  ##read sentence from device
    while 1:      ##keep reading until get a result could be return
        serial_line = ser.readline()
        information=serial_line.split(",")
        if information[0] == stableSen and (information[2] == '2' or information[2] == '3'): ##if signal is strong enough
            lookingPosition = True
            #lookingSpeed = True
            while lookingPosition: #or lookingSpeed:     ##looking for position sentece
                serial_line = ser.readline()
                information=serial_line.split(",")
                #if information[0] == speedSen:
                #   speedInfo = information[7]
                #   lookingSpeed = False
                ##check position sentence and is active
                if information[0] == locationSen and information[2] == 'A': 
                    locationInfo = formatLocation(information)
                    lookingPosition = False
            
            return locationInfo #+ ',' + speedInfo