import numpy as np
import glob 
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def Func(t,a,b):
    y = a*(1-np.exp(-t/(b)))
    return y

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

    Vec_Start = 300*np.array(range(len(namevec)))**0.0
    Vec_End = 300*np.array(range(len(namevec)))**0.0

    fig, axs = plt.subplots(1,1,constrained_layout = True, figsize=(10,8))


    for k in range(0,1):
        Time, V,I,R,T1,T2 = readMeas(namevec[k], AdcRate)
        popt, pcov = curve_fit(Func, Time, I)

        print()
        print(namevec[k])
        print("I_st: " + str(popt[0])+" [A]     Tao: "+str(popt[1])+" [ms]")
        print()

        axs.plot(np.array(Time),I,color="green")
        axs.plot(np.array(Time),Func(np.array(Time),*popt),linestyle="dashed")
        axs.plot(np.array(Time),R)
        

    axs.set_ylabel("Intensity [A]",fontsize=14)
    axs.set_xlabel("Time [s]",fontsize=14)

    plt.show()

def PlotExpectedIntensity(AdcRate,filename):
    import matplotlib as mpl

    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False

    plt.figure(figsize=(6,4))
    Time, V,I,R,T1,T2 = readMeas(filename, AdcRate)
    popt, pcov = curve_fit(Func, Time, I)
    print()
    print("I_st: " + str(popt[0])+" [A]     Tao: "+str(popt[1])+" [ms]")
    print()

    
    plt.plot(Time, np.array(I),lw=2,marker="s",ms=5,color="forestgreen",label="Measured I = 0.797 [A]")
    plt.hlines( y = 0.8, xmin = 5000, xmax = Time[-1],lw=2,color='black',label="Expected I = 0.800 [A]")
    plt.vlines(x = 5000, ymin=0.0,ymax=0.8,lw=2,color='black')
    #plt.xlim(-5,40)
    plt.legend(fontsize=14,loc='lower right')
    plt.ylabel("Intensity [a]",fontsize=14)
    plt.xlabel("Time [ms]",fontsize=14)
    plt.xticks(fontsize=14); plt.yticks(fontsize=14)
    
    
    plt.show()

def PlotR0Example(filename,AdcRate):
    Time, V,I,R,T1,T2 = readMeas(filename, AdcRate)
    popt, pcov = curve_fit(Func, Time, I)

    plt.plot(Time, R, color="firebrick",marker="s",ms=5)
    plt.ylabel("Resistence [Ohm]",fontsize=14)
    plt.xlabel("Time [ms]",fontsize=14)
    plt.xticks(fontsize=14); plt.yticks(fontsize=14)
    #plt.xlim(-5,40)

    plt.show()



# ------------------------- MAIN ------------------------ #

AdcRate = 1.0

#PlotAllFiles(AdcRate)

filename = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/RMeas10.txt"
#PlotExpectedIntensity(AdcRate,filename)

#PlotR0Example(filename,AdcRate)