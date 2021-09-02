from os import write
import serial
import serial.tools.list_ports
import time

###################### Variables Dictionary #######################
#                       ser.write(b'A')                           #      
#    T: Temperature Read-Out                                      #
#    S: Start Adquisition, sends current                          #
#    s: Stop Adquisition                                          #
#    R: Set rate in us                                            #
#        R?: Tells you the current set rate                       #
#        Rx: Measurement every x us. Max. 100us                   #
#    O: Set DAC offset. Better not to change.                     #
#    M: Controlled Current in mA                                  #
#        M0: Stop sending current.                                #
#        M1,X : Starts sending X [mA] of Current                  #
#    A: Start ADC adquisition without sending current.            #
###################################################################

# --------------------------------------------------------- FUNCTIONS  --------------------------------------------------- #

def ADCDecode(message):
    # Transforms Temperature Data from Hexadecimal to Decimal
    try:
        rawmsg = int(message.hex(), 16)
        #print(message.hex())
    except ValueError:
        return 0,0,0,0,0
    else:
        #print(hex(rawmsg))
        msgIndex = (rawmsg >> 8*8) & 0xFF
        ADC2 = (rawmsg >> 8*6) & 0xFFFF
        ADC1 = (rawmsg >> 8*4) & 0xFFFF
        temperature1 = (rawmsg >> 20) & 0xFFF
        temperature2 = (rawmsg >> 8) & 0xFFF
    return msgIndex, ADC1, ADC2, temperature1, temperature2

def ADCConvert(ADC1, ADC2):
    Vref = 2.5
    ADCmax = 0xFFF0
    print()
    V1 = (2 * ADC1 - ADCmax) * Vref /ADCmax
    V2 = -(2 * ADC2 - ADCmax) * Vref /ADCmax
    return V1, V2


# got this Readline from https://github.com/pyserial/pyserial/issues/216#issuecomment-369414522, so i guess it works faster??
class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

def setADCRate(ser,ADCRate):
    cmd = "R"
    cmd += str(ADCRate)
    bytecmd = bytearray(cmd.encode())
    ser.write(bytecmd)
    print(ser.readline().decode())

def setVoffset(channel, voltage,ser):
    cmd = "O"
    cmd += str(channel)
    cmd += ","
    cmd += str(int(voltage))
    bytecmd = bytearray(cmd.encode())
    ser.write(bytecmd)
    print(ser.readline().decode())

def stopMeasureR0():
    cmd = "M0"
    bytecmd = bytearray(cmd.encode())
    ser.write(bytecmd)
    print(ser.readline().decode())

def MeasureADCZero(ser,foldername):
    # ------------------------------------------- Get ADC zero ------------------------------------ #
    #    Here we are measuring the wire voltage/current without putting a current on the wire       #
    #    There are 20 measurements of "zero" voltage                                                #

    f = open(foldername+"ADCZero.txt","w+")
    f.write("  ---------- ADC Measurements at Zero Voltage.   ---------- \n")
    f.write("      V [V]       I [mA]     \n")

    ser.write(b'A')
    Vzero = 0; Izero = 0

    for i in range(20):
        message = ser.read(9)
        msgIndex, ADC1, ADC2, temperature1, temperature2 = ADCDecode(message)
        V, I = ADCConvert(ADC1, ADC2)

        f.write(str(round(V,5))+"       "+str(round(I,5))+"\n")
        Vzero += V; Izero += I
        print(msgIndex, ADC1, ADC2, temperature1, temperature2)
        print (V,I)

    ser.write(b's')

    Vzero /= 20; Izero /= 20

    print ("Vzero",Vzero,"Izero",Izero)
    f.write("  ----------------------------------------------------------\n ")
    f.write("Vzero = "+str(round(Vzero,5))+"       Izero = "+str(round(Izero,5))+"\n")
    f.write("  ---------------------------------------------------------- \n")
    f.close()

    time.sleep(1)

    ser.flushInput()
    ser.flushOutput()
    return Vzero, Izero

def MeasureR0(I0,Vzero, Izero, ser,foldername):
    Nmeas = 100000
    cmd = "M1,"
    cmd += str(I0)

    ser.write(bytearray(cmd.encode()))
    f = open(foldername+"R0Meas_"+str(I0)+"mA.txt","w+")
    f.write("  ---------- Measurements R0 at " + str(I0)+ " [mA]  ---------- \n")
    f.write("      Vzero [V]    Vmeas [V]    V [V]    Izero[mA]     Imeas [mA]      I [mA]         R0 [Ohm]      T1[Np]      T2[Np]  \n")


    print(ser.readline().decode())
    for i in range(Nmeas):
        message = ser.read(9)
        msgIndex, ADC1, ADC2, temperature1, temperature2 = ADCDecode(message)
        print(msgIndex, ADC1, ADC2, temperature1, temperature2)
        V, I = ADCConvert(ADC1, ADC2)
        R0 = round((V-Vzero)/(I-Izero), 5)
        print ("V:", round(V-Vzero, 4), "I:", round(I-Izero, 4), "R0: ",  R0)
        f.write(str(round(Vzero,5))+"      "+str(round(V,5))+"       "+str(round(V-Vzero,5)))
        f.write("      "+str(round(Izero,5))+"    "+str(round(I,5))+"    "+str(round(I-Izero,5)) + "     "+str(round(R0,5))+ "     ")
        f.write(str(temperature1)+"     "+str(temperature2)+"\n")
    f.close()
    ser.write(b'M0')
    ser.write(b's')
    ser.close()
    print("Stopped")

    return V, I, R0

def ReadMesage(Vzero,Izero,ser):
    message = ser.read(9)
    msgIndex, ADC1, ADC2, temperature1, temperature2 = ADCDecode(message)
    
    print(msgIndex, ADC1, ADC2, temperature1, temperature2)
    
    V, I = ADCConvert(ADC1, ADC2)
    R = round((V-Vzero)/(I-Izero), 5)
    
    print ("V:", round(V-Vzero, 4), "I:", round(I-Izero, 4), "R:",  R)
    
    return V, I, R, temperature1, temperature2

def MeasureR_New(Vzero,Izero,ser,foldername,NumberMeas):
    Nmeas_SP1 = 1000; Nmeas_P1P0 = 50000; Nmeas_P0s = 5000
    vec_I, vec_V, vec_R, vec_T1, vec_T2 = [],[],[],[],[]

    print("    Measurement ON current OFF     ")
    ser.write(b'S')

    for i in range(Nmeas_SP1):  
        V, I, R, temperature1, temperature2 = ReadMesage(Vzero,Izero,ser)
        vec_I += [I]; vec_R += [R]; vec_V += [V]
        vec_T1 += [temperature1]; vec_T2 += [temperature2]

    print("     Measurement ON current ON     ")
    ser.write(b'P1')
    for j in range(Nmeas_P1P0):
        V, I, R, temperature1, temperature2 = ReadMesage(Vzero,Izero,ser)
        vec_I += [I]; vec_R += [R]; vec_V += [V]
        vec_T1 += [temperature1]; vec_T2 += [temperature2]

    print("     Measurement ON current OFF    ")
    ser.write(b'P0')
    for k in range(Nmeas_P0s):
        V, I, R, temperature1, temperature2 = ReadMesage(Vzero,Izero,ser)
        vec_I += [I]; vec_R += [R]; vec_V += [V]
        vec_T1 += [temperature1]; vec_T2 += [temperature2]

    print("      Measurement STOP        ")
    ser.write(b's')
    ser.close()
    print()
    print("Writting file........")

    f = open(foldername+"RMeas"+str(NumberMeas)+".txt","w+")
    f.write("  ---------- Measurements R  ---------- \n")
    f.write("      Vzero [V]    Vmeas [V]    V [V]    Izero[mA]     Imeas [mA]      I [mA]         R0 [Ohm]      T1[Np]      T2[Np]  \n")

    for k in range(0,len(vec_I)):
        f.write(str(round(Vzero,5))+"      "+str(round(vec_V[k],5))+"       "+str(round(vec_V[k]-Vzero,5)))
        f.write("      "+str(round(Izero,5))+"    "+str(round(vec_I[k],5))+"    "+str(round(vec_I[k]-Izero,5)) + "     "+str(round(vec_R[k],5))+ "     ")
        f.write(str(vec_T1[k])+"     "+str(vec_T2[k])+"\n")
    f.close()

    print("FINISHED!")



    

    
