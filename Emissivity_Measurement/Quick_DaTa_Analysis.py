
import numpy as np
import matplotlib.pyplot as plt
import glob

def readMeas(filename, AdcRate):
    f = open(filename,"r")
    t = 0
    V = []; I = []; R =[]; T1 = []; T2 = []; Time = []
    for count,l in enumerate(f, start=0):
        if count > 1:
            asd = l.split(" ")
            voltage = float(asd[13])*2.0; intensity = float(asd[27])
            if (intensity > 1e-3) and (voltage > 1e-3):
                R += [float(asd[32])]
            else:
                R += [0.0]
            
            V += [voltage]; I += [intensity]
            T1 += [float(asd[37])]; T2 += [float(asd[42].split("\n")[0])]
            Time += [t*AdcRate]; 

            t+= 1

    return Time, V, I, R, T1, T2

def Plot_Meas(Time,V,I,R,T1,T2):
    fig, axs = plt.subplots(1,2,constrained_layout = True, figsize=(10,4),  gridspec_kw={'width_ratios': [2, 1]})
    
    ss1 = 300; ss2 = 8000
    Av_I = np.mean(I[ss1:ss2]); Av_V = np.mean(V[ss1:ss2]); Av_R = np.mean(R[ss1:ss2])
    St_I = np.std(I[ss1:ss2]); St_V = np.std(V[ss1:ss2]); St_R = np.std(R[ss1:ss2])

    axs[0].set_title("Electrical Measurements",fontsize=14)
    axs[1].set_title("Temperature Measurements",fontsize=14)

    axs[0].plot(Time,V,linewidth=2,color="royalblue",label="V  = "+str(round(Av_V,4))+" [v]")
    axs[0].plot(Time,I,linewidth=2, color = "forestgreen",label="I = "+str(round(Av_I,4))+" [A]")
    axs[0].plot(Time,R,linewidth=2, color = "orchid",label = "R = "+str(round(Av_R,4))+" [Ohm]")
    #axs[0].axvline(x=ss1,linewidth=2,color = "grey", linestyle="dashed")
    #axs[0].axvline(x=ss2,linewidth=2,color = "grey", linestyle="dashed", label = "ss Window")
    axs[0].set_xlabel("Time [ms]",fontsize = 14)

    axs[0].legend(loc=1)

    axs[1].plot(Time,T1,linewidth=2,color="indianred",label="T1 [Npulses]")
    axs[1].plot(Time,T2,linewidth=2,color="orange",label="T2 [Npulses]")
    axs[1].set_xlabel("Time [ms]",fontsize = 14)

    axs[1].legend(loc=4)

    return Av_I, St_I, Av_V, St_V, Av_R , St_R   

def Plot_MeasCompa(filename1,filename2):
    V_1,I_1, R_1, T1_1, T2_1 = readMeas(filename1)
    V_2,I_2, R_2, T1_2, T2_2 = readMeas(filename2)

    fig, axs = plt.subplots(2,3,constrained_layout = True, figsize=(10,4))

    axs[0,0].plot(V_1,linewidth=2,color = "mediumblue",label = "V_1 [V]")
    axs[0,0].plot(V_2,linewidth=2,color = "darkturquoise",label = "V_2 [V]")

    axs[0,0].legend()

    axs[0,1].plot(I_1,linewidth=2,color = "seagreen",label = "I_1 [A]")
    axs[0,1].plot(I_2,linewidth=2,color = "lawngreen",label = "I_2 [A]")
    axs[0,1].legend()

    axs[0,2].plot(R_1,linewidth=2,color = "mediumorchid",label = "R_1 [Ohm]")
    axs[0,2].plot(R_2,linewidth=2,color = "magenta",label = "R_2 [Ohm]")
    axs[0,2].legend()

    axs[1,0].plot(T1_1,linewidth=2,color = "darkred",label = "T1_1 [Npulses]")
    axs[1,0].plot(T1_2,linewidth=2,color = "orangered",label = "T1_2 [Npulses]")
    axs[1,0].legend()

    axs[1,1].plot(T2_1,linewidth=2,color = "orange",label = "T2_1 [Npulses]")
    axs[1,1].plot(T2_2,linewidth=2,color = "gold",label = "T2_2 [Npulses]")
    axs[1,1].legend()

    plt.show()


# -------------------------------------------------------- #
## Simple Data visualization. 
AdcRate=1
Time, V,I,R,T1,T2 = readMeas("Emissivity_Measurement/OutputFiles/Tungsten_Vacuum_Try1/RMeas750.txt", AdcRate)
Av_I, St_I, Av_V, St_V, Av_R , St_R = Plot_Meas(Time,V,I,R,T1,T2); plt.show()

# -------------------------------------------------------- #
## Comparison of two Intensities. 
#Plot_MeasCompa("Copper_NoVacuum_Try1/R0Meas_140.0mA.txt","Copper_NoVacuum_Try1/R0Meas_300.0mA.txt")

# -------------------------------------------------------- #

## Creates .png from files in namevec. and calculates steady state I,  V and R. 
#namevec = glob.glob("Emissivity_Measurement/OutputFiles/Copper_NoVacuum_Try3/R0*")
#namevec = glob.glob("OutputFiles/Copper_NoVacuum_Try3/RMeas5.txt")
#SummaryMeasurements(namevec,AdcRate)

# -------------------------------------------------------- #
# Plot R vs I
#filename = "Emissivity_Measurement/LittleResults/Copper_IR.txt"
#PlotSummary_R_vs_I(filename)


# -------------------------------------------------------- #

#PlotAllFiles(AdcRate)