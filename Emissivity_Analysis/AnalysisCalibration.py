import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os

def readMeas(filename, AdcRate):
    f = open(filename,"r")
    t = 0
    V0 = []; I0 = []; V = []; I = []; R =[]; T1 = []; T2 = []; Time = []
    for count,l in enumerate(f, start=0):
        if count > 1:
            asd = l.split(" ")
            V0 += [float(asd[0])]
            I0 += [float(asd[19])]
            V += [-float(asd[6])]
            I += [float(asd[23])]
            Time += [t*AdcRate]

            t+= 1; 

    return Time, V0, I0, V, I

def PlotMeas(foldername,filename, AdcRate):
    Start_AvI = 500; End_AvI = 4000
    Start_AvV = 500; End_AvV = 4000
    cwd = os.getcwd()
    Time, V0, I0, V, I = readMeas(cwd+foldername+filename,AdcRate)
    fig, axs = plt.subplots(1,2,constrained_layout = True, figsize=(10,4))
    axs[0].plot(Time,V0,color = "black",lw=2,label="V0")
    axs[0].plot(Time,V,color = "blue",lw=2,label="V")
    axs[0].axvline(Time[Start_AvV],color="red",lw=2)
    axs[0].axvline(Time[End_AvV],color="red",lw=2)
    axs[0].set_ylabel("Voltage [V]",fontsize=14)
    axs[0].set_xlabel("Time [s]",fontsize=14)

    axs[1].plot(Time,I0,color="black",lw=2,label="I0")
    axs[1].plot(Time,I,color="green",lw=2,label="I")
    axs[1].axvline(Time[Start_AvI],color="red",lw=2)
    axs[1].axvline(Time[End_AvI],color="red",lw=2)
    axs[1].set_ylabel("Intensity [A]",fontsize=14)
    axs[1].set_xlabel("Time [s]",fontsize=14)

    axs[0].legend(fontsize=14)
    axs[1].legend(fontsize=14)
    plt.show()

def CalculateAverage(Time, V0,V, I0, I):
    Av_V, Av_I = 0.0,0.0

    Start_AvI = 500; End_AvI = 4000
    Start_AvV = 500; End_AvV = 4000


    Av_I0 = np.mean(I0[Start_AvI:End_AvI]); std_I0 = np.std(I0[Start_AvI:End_AvI])
    Av_I = np.mean(I[Start_AvI:End_AvI]); std_I = np.std(I[Start_AvI:End_AvI])

    Av_V0 = np.mean(V0[Start_AvV:End_AvV]); std_V0 = np.std(V0[Start_AvV:End_AvV])
    Av_V = np.mean(V[Start_AvV:End_AvV]); std_V = np.std(V[Start_AvV:End_AvV])

    print("         Summary Measurements               ")
    print("I0: "+str(Av_I0)+" +- "+str(std_I0))
    print("I:" +str(Av_I)+" +- "+str(std_I))
    print()
    print("V0: "+str(Av_V0)+" +- "+str(std_V0))
    print("V:" +str(Av_V)+" +- "+str(std_V))
    print()

    #plt.show()

    return Av_I0, Av_I, std_I, Av_V0, Av_V, std_V

def CalibrationDAtaExtraction(foldername, filename_measum, AdcRate):
    MeasI, MeasV, AvI0, AvI, ErrI, AvV0, AvV, ErrV = [],[],[],[],[],[],[],[]
    cwd = os.getcwd()
    print(foldername+filename_measum)
    f = open(cwd+foldername+filename_measum)
    
    cont = 0 
    for l in f: 
        if cont > 1:
            asd = l.split(" ")
            MeasI += [float(asd[5])]
            MeasV += [float(asd[-1].split("\n")[0])]

            filename_datafile = "RMeas"+asd[0]+".txt"
            print("Current Data: "+filename_datafile)
            Time, V0, I0, V, I = readMeas(cwd+foldername+filename_datafile,AdcRate)
            avI0, avI, erI, avV0, avV, erV = CalculateAverage(Time, V0, I0, V, I )

            AvI0 += [avI0]; AvI += [avI]; ErrI += [erI]; AvV0 += [avV0]; AvV += [avV]; ErrV += [erV]
        cont += 1

    return np.array(MeasI), np.array(MeasV), np.array(AvI0), np.array(AvI), np.array(ErrI), np.array(AvV0), np.array(AvV), np.array(ErrV)

def PlotCalibration(MeasI, MeasV, AvI0, AvI, ErrI, AvV0, AvV, ErrV):
    fig, axs = plt.subplots(1,2,constrained_layout = True, figsize=(10,4))
    axs[0].errorbar(MeasI,AvI,xerr=None,yerr=ErrI,color = "black",label="I", fmt='o')
    axs[0].errorbar(MeasI,AvI0,xerr=None,yerr=ErrI,color = "blue",label="I0",linestyle=None, fmt='o')
    axs[0].set_ylabel("Intensity [A]",fontsize=14)
    axs[0].set_xlabel("Intensity [A]",fontsize=14)

    axs[1].errorbar(MeasV,AvV,xerr=None,yerr=ErrV,color="black",label="V",linestyle=None, fmt='o')
    axs[1].errorbar(MeasV,AvV0,xerr=None,yerr=ErrV,color="green",label="V0",linestyle=None, fmt='o')
    axs[1].set_ylabel("Voltage [V]",fontsize=14)
    axs[1].set_xlabel("Voltage [V]",fontsize=14)

    axs[0].legend(fontsize=14)
    axs[1].legend(fontsize=14)

    plt.show()
    
    return 0.0

# ----------------------- MAIN: Calculate Calibrations ------------------- #


# 1st Load the Summarty Measurements file. For each measurement there should be one data file 
# called RMeas + str(Requested_I)
# That file is opened, averages are calculated and data is aded to a vector. 




cwd = os.getcwd()
print("Current Directory: "+cwd)
MeasI, MeasV, AvI0, AvI, ErrI, AvV0, AvV, ErrV = CalibrationDAtaExtraction("/Calibration/GV1GI0/","MeasuredPoints.txt",10e-3)
PlotCalibration(MeasI, MeasV, AvI0, AvI, ErrI, AvV0, AvV, ErrV)


PlotMeas("/Calibration/GV1GI0/","RMeas630.txt",10e-3)
