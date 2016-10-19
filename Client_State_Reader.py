#coding:utf-8
# This script is used to get the following parameters FROM CLENT:
# Time Stamp
# GPS location(latitude,longitude)
# moving speed
# signal_power_dbm
# noise_power_dbm
# mother_board_temp_sensor2
# daughter_card_temp_sensor
# channel
# downlink_modulation
# PER
# //
# //      ┏┛ ┻━━━━━┛ ┻┓
# //      ┃　　　　　　           ┃
# //      ┃　　　━　　　         ┃
# //      ┃　┳┛　  ┗┳　     ┃
# //      ┃　　　　　　           ┃
# //      ┃　　　┻　　　         ┃
# //      ┃　　　　　　           ┃
# //      ┗━┓　　　┏━━━━━┛
# //         ┃　　　┃    Update(Oct 7 2016)-->add initial check, if GPS signal is unstable, print message and terminate script.
# //        ┃　　　┃                       -->auto check if GPS has speed module, if not, put -99 as speed for all data.
# //        ┃　　　┗━━━━━━━━━┓
# //        ┃　　　　　　　              ┣┓
# //        ┃　　　　                  ┏┛
# //        ┗━┓  ┓ ┏━━━┳┓┏━┛
# //           ┃  ┫ ┫       ┃ ┫ ┫
# //          ┗━┻━┛       ┗━┻━┛
#Those information will coma-separated and writen to the file named: Client_sysinfor_data.cvs
# in the current working directory
# Originated on August 17, 2016

import serial
import socket
import signal
import os
import subprocess
import time
import NMEA_Reader

BUFFER_SIZE = 65535

##indicate the type of sentence
STALBESEN = "$GPGSA" 
LOCATIONSEN = "$GPRMC"
SPEEDSEN = "$GPVTG"


Aowa_RPC_GetSystemInfo_NUM = 117
Aowa_Remote_GetAgentULSInfoSimple_NUM = 69
Aowa_RPC_GetLastRAInfo = 60
Aowa_RPC_EnumAgents = 35


line = ""
data_file_name = "Client_sysinfo_data.txt"


gModTable = ['QPSK','16QAM','64QAM','']
gPuncTable = ['1/2','2/3','3/4','5/6','']


# usage report function start
def getReadableTime():
    #return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    return time.strftime("%a. %d %b %Y %H:%M:%S +0000", time.localtime())

def socket_init(host, port):
    # create a TCP/IP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'socket created'
    except socket.error as msg:
        print 'socket cannot be created. C' 
        s = None
        pass

    # connect the socket to the port where the server (remote host) is listening
    try:
        server_address = (host, port)
        print 'connecting to: ',  server_address
        s.connect(server_address)
    except socket.error as msg:
        print 'Failed to connecting socket. '
        s.close()
        s = None
        pass

    if s is None:
        #print >> sys.stderr,  'could not open socket'
        print 'Could not open socket'
        #sys.exit(1)

    return s

def socket_uninit(s):
    print 'closing socket'
    s.close()
    
def AowaPingPongCmd(s, cmd, inMac):
    MESSAGE = "<RPCV1>" + str(cmd) + " " + inMac + "</RPCV1>\r\n"
    s.send(MESSAGE)
    
    data = s.recv(BUFFER_SIZE)

    # The first field is OK word, skip it
    # skip also the space, which comes the index 3
    r_data = data[3:] 
    return r_data 
    
def save_data(line):
    if os.path.isfile(data_file_name):
        with open(data_file_name, "a") as myfile:
            line = '\n'+ getReadableTime() + ','+ line
            myfile.write(line)
            myfile.close() 
    else:
            with open(data_file_name, "a") as myfile:
                line = "Time,Latitude,Longitude,Latency,Moving_Speed,Signal_Power_dbm,Noise_Power_dbm,Mother_Board_Temp,Daughter_Card_Temp,Channel,Downlink_Modulation,PER"
                myfile.write(line)
                myfile.close() 
    
def Get_parameters(s):
    line = "Connection Dropped"
    
    #get internet state
    result = subprocess.Popen("ping -w 1 8.8.8.8", shell=True, stdout=subprocess.PIPE).stdout.read()
    aa = result.split(',')
    
    recievePac = aa[1].split('=')[1]
    if int(recievePac) != 0:
        a = aa[4].split('=')
        latency = a[1]
    else:    
        latency = '-999'
           
    #get mac address
    macInfo = AowaPingPongCmd(s,Aowa_RPC_EnumAgents,'ff:ff:ff:ff:ff:ff')
    macData = macInfo.split()
    mmc = macData[1]
        
    #get system info
    sysInfo = AowaPingPongCmd(s,Aowa_RPC_GetSystemInfo_NUM,'ff:ff:ff:ff:ff:ff')  
    #check result, and save GPS info
    if len(sysInfo) > 1:
        #print sysInfo
        data = sysInfo.split()
    else:
        print "Faile in getting SystemInfo"
             
    #get modulation information and PER information
    modulationInfo = AowaPingPongCmd(s,Aowa_Remote_GetAgentULSInfoSimple_NUM,mmc)
    if len(modulationInfo) > 1:
        modulation_Data = modulationInfo.split()            
        #some time, the client give the number no meanning
        if int(modulation_Data[2]) > 2:
            modulation_Data[2] = 3
        if int(modulation_Data[3]) > 3:
            modulation_Data[3] = 4

        #use index find the phyMode
        phyMode_dl = gModTable[int(modulation_Data[2])] + ' ' + gPuncTable[int(modulation_Data[3])]  
        PER = round((float(modulation_Data[7])/float(modulation_Data[6])),3) 
                
    else:
        print 'no base linked.'
        
             
    #put all information together 
    line  = latency + ',' + data[31] + ',' + data[33] + ',' + data[41] + ',' + data[43] + ',' + data[115] + ','  + phyMode_dl +',' + str(PER) + '%' 
    return line
        


    
    
    

