import serial
import serial.tools.list_ports
import time
import sys
from FunctionsFolder import NecesaryFunctions as nf


# ----------------------------------- Variables Set Ups ----------------------------------- #

AdqRate = 10000                          # Adquisition Rate. Cada AdqRate Una adquisicion. Max. (1 Ac/100 us)

Flag_MeasureADCZero = "Yes"
#Flag_MeasureR0 = "No,310"                    # [mA] Ojo, max 300 mA
Flag_MeasureR = "Yes,50"                        # Current Already set in by source.
OutputFolderName = "Calibration/"

import os
print(os.getcwd())
# ----------------------------- Set up Computer Micro-Controler Conection  ----------------------------- #

COMPort = 'COM5'
serialBaudRate = 1152000
serialInterCharTimeout = 100e-3 # 100us 

print(" ###### Computer Conection Variables  ##### ")
print("  Using serial port  ",COMPort, " at ",serialBaudRate, " baud " )


try:
    ser = serial.Serial(COMPort, baudrate=serialBaudRate, bytesize=8, parity='N', stopbits=1, timeout=1)
    print("Opened")
except Exception as error:
    print("Error:", error)
    raise

ser.flushInput()
ser.flushOutput()
rl = nf.ReadLine(ser)

nf.setADCRate(ser,AdqRate)

Flag_MeasureR = "Yes,1100"                        # Current Already set in by source.
ser.write(b'GV,2')
print(ser.readline().decode())
ser.write(b'GI,0')
print(ser.readline().decode())
ser.write(b'I100')
print(ser.readline().decode())

time.sleep(2)



#nf.SetCurrent(300,ser) # [mA]


if Flag_MeasureADCZero == "Yes":
    Vzero, Izero = nf.MeasureADCZero(ser,OutputFolderName)
else: Vzero = 0.0; Izero = 0.0

print("Vzero: "+str(Vzero)+"      Izero: "+str(Izero))
# --------------------------------- Measure R --------------------------------------- #

if Flag_MeasureR.split(",")[0] == "Yes":
    nf.MeasureR_New(Izero,Vzero, ser, OutputFolderName,Flag_MeasureR.split(",")[1])