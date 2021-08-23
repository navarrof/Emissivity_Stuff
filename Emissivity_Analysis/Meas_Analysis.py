import numpy as np
import glob 
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def readMeas(filename, AdcRate):
    f = open(filename,"r")
    t = 0
    V = []; I = []; R =[]; T1 = []; T2 = []; Time = []
    for count,l in enumerate(f, start=0):
        if count > 1:
            asd = l.split(" ")
            voltage = float(asd[13]); intensity = float(asd[27])
            if (intensity > 1e-3) and (voltage > 1e-3):
                R += [float(asd[32])]
            else:
                R += [0.0]
            
            V += [voltage]; I += [intensity]
            T1 += [float(asd[37])]; T2 += [float(asd[42].split("\n")[0])]
            Time += [t*AdcRate]; 

            t+= 1

    return Time, V, I, R, T1, T2
    
def PlotAllFiles(AdcRate):
    namevec = glob.glob("Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/R0*")
    n = int(len(namevec)/2.0)+1

    Vec_Start = 300*np.array(range(len(namevec)))**0.0
    Vec_End = 300*np.array(range(len(namevec)))**0.0

    fig, axs = plt.subplots(1,1,constrained_layout = True, figsize=(10,8))


    for k in range(0,12):
        Time, V,I,R,T1,T2 = readMeas(namevec[k], AdcRate)
        axs.plot(np.array(Time)*1e-3,I)

    axs.set_ylabel("Intensity [A]",fontsize=14)
    axs.set_xlabel("Time [s]",fontsize=14)
    axs.set_title("R0 Measurement")
    plt.show()


def Fit_CurveToData(filename,AdcRate):
    def Func(t,a,b):
        y = a*(1-np.exp(-t/(b)))
        return y

    Time, V,I,R,T1,T2 = readMeas(filename, AdcRate)
    popt, pcov = curve_fit(Func, Time, I)

    plt.figure()
    plt.plot(Time,I,color="green")
    plt.plot(np.array(Time),Func(np.array(Time), *popt))

    plt.show()

    







    return 0

# ------------------------- MAIN ------------------------ #

AdcRate = 1.0

#PlotAllFiles(AdcRate)

filename = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/R0Meas_100.0mA.txt"
Fit_CurveToData(filename,AdcRate)