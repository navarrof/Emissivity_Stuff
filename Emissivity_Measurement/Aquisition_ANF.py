import serial
import serial.tools.list_ports
import time
import sys
from FunctionsFolder import NecesaryFunctions as nf


# ----------------------------------- Variables Set Ups ----------------------------------- #

AdqRate = 1000                          # Adquisition Rate. Max. (1 Ac/100 us)

Flag_MeasureADCZero = "Yes"
Flag_MeasureR0 = "No,300"                    # [mA] Ojo, max 300 mA
Flag_MeasureR = "Yes,21"                        # Current Already set in by source.
OutputFolderName = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/"

import os
os.chdir(os.path.dirname(os.getcwd()))
print(os.getcwd())
# ----------------------------- Set up Computer Micro-Controler Conection  ----------------------------- #

COMPort = 'COM4'
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


# ------------------------------- Measure Zero Current State ----------------------------- #

nf.setVoffset(0,1000,ser)

if Flag_MeasureADCZero == "Yes":
    Vzero, Izero = nf.MeasureADCZero(ser,OutputFolderName)
else: Vzero = 0.0; Izero = 0.0

# -------------------------------- Measure R0  ------------------------------------- #
if Flag_MeasureR0.split(",")[0] == "Yes":
    V, I, R0 = nf.MeasureR0(float(Flag_MeasureR0.split(",")[1]), Vzero, Izero, ser,OutputFolderName)
else: 
    V = 0.0; I = 0.0; R0 = 0.0

# --------------------------------- Measure R --------------------------------------- #

if Flag_MeasureR.split(",")[0] == "Yes":
    nf.MeasureR_New(Vzero,Izero, ser, OutputFolderName,Flag_MeasureR.split(",")[1])