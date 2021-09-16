import numpy as np 
import matplotlib.pyplot as plt

def ReadCalFile(Filename):
    f = open(Filename)
    Igiven, Idig, Vdig, Imul, Vmul = [],[],[],[],[]
    for l in f: 
        asd = l.split(" ")
        if asd[0] == "#": continue
        else: 
            Igiven += [float(asd[0])]
            Idig += [float(asd[5])]
            Vdig += [float(asd[10])]
            Imul += [float(asd[15])]
            Vmul += [float(asd[-1].split("\n")[0])]

    
    return Igiven, Idig, Vdig, Imul, Vmul 

def CalibrationPlots(R0Vec,RVec):

    Igiven_R0 = R0Vec[0]; Idig_R0 = R0Vec[1]; Vdig_R0 = R0Vec[2]; Imul_R0 = R0Vec[3]; Vmul_R0 = R0Vec[4]
    Igiven_R = RVec[0]; Idig_R = RVec[1]; Vdig_R = RVec[2]; Imul_R = RVec[3]; Vmul_R = RVec[4]
    
    fig, axs = plt.subplots(2,2,constrained_layout = True, figsize=(12,8))
    fig.suptitle("Circuit 1: Calibration Curves", fontsize=16)
    
    axs[0,0].plot(Igiven_R0,Idig_R0,label="Processed R0",color="forestgreen",ls="dashed",marker="o",lw=2)
    axs[0,0].plot(Igiven_R0,Imul_R0,label="Multimeter R0",color = "firebrick",ls="dashed",marker="o",lw=2)
    axs[0,0].plot(Igiven_R,Idig_R,label="Processed R",color = "goldenrod",ls="dashed",marker="o",lw=2)
    axs[0,0].plot(Igiven_R,Imul_R,label="Multimeter R",color = "turquoise",ls="dashed",marker="o",lw=2)
    axs[0,0].set_xlabel("Given Intensity [A]",fontsize=14)
    axs[0,0].set_ylabel("Measured Intensity [A]",fontsize=14)
    axs[0,0].legend(fontsize=14)
    axs[0,0].xaxis.set_tick_params(labelsize=14)
    axs[0,0].yaxis.set_tick_params(labelsize=14)
    axs[0,0].set_xlim(0.02,0.45)
    axs[0,0].set_ylim(0.02,0.4)

    axs[0,1].plot(Igiven_R0,Vdig_R0,label="Processed R0", color = "royalblue",ls="dashed",marker="o",lw=2)
    axs[0,1].plot(Igiven_R0,Vmul_R0,label="Multimeter R0", color = "darkorange",ls="dashed",marker="o",lw=2)
    axs[0,1].plot(Igiven_R,Vdig_R,label="Processed R",color = "purple",ls="dashed",marker="o",lw=2)
    axs[0,1].plot(Igiven_R,Vmul_R,label="Multimeter R",color = "crimson",ls="dashed",marker="o",lw=2)
    axs[0,1].set_xlabel("Given Intensity [A]",fontsize=14)
    axs[0,1].set_ylabel("Measured Voltage [V]",fontsize=14)
    axs[0,1].legend(fontsize=14)
    axs[0,1].xaxis.set_tick_params(labelsize=14)
    axs[0,1].yaxis.set_tick_params(labelsize=14)
    axs[0,1].set_xlim(0.02,0.45)
    axs[0,1].set_ylim(0.02,1.0)

    axs[1,0].plot(Igiven_R,Idig_R,label="Processed R",color = "goldenrod",ls="dashed",marker="o",lw=2)
    axs[1,0].plot(Igiven_R,Imul_R,label="Multimeter R",color = "turquoise",ls="dashed",marker="o",lw=2)
    axs[1,0].set_xlabel("Given Intensity [A]",fontsize=14)
    axs[1,0].set_ylabel("Measured Voltage [V]",fontsize=14)
    axs[1,0].legend(fontsize=14)
    axs[1,0].xaxis.set_tick_params(labelsize=14)
    axs[1,0].yaxis.set_tick_params(labelsize=14)

    axs[1,1].plot(Igiven_R,Vdig_R,label="Processed R",color = "purple",ls="dashed",marker="o",lw=2)
    axs[1,1].plot(Igiven_R,Vmul_R,label="Multimeter R",color = "crimson",ls="dashed",marker="o",lw=2)
    axs[1,1].set_xlabel("Given Intensity [A]",fontsize=14)
    axs[1,1].set_ylabel("Measured Voltage [V]",fontsize=14)
    axs[1,1].legend(fontsize=14)
    axs[1,1].xaxis.set_tick_params(labelsize=14)
    axs[1,1].yaxis.set_tick_params(labelsize=14)

    
    

# -------------------------- MAIN --------------------------- #

Igiven, Idig, Vdig, Imul, Vmul  = ReadCalFile("Emissivity_Measurement/OutputFiles/CalibrationR0_Circuit1")
R0Vec = [Igiven, Idig, Vdig, Imul, Vmul]
Igiven, Idig, Vdig, Imul, Vmul  = ReadCalFile("Emissivity_Measurement/OutputFiles/CalibrationR_Circuit1.txt")
RVec = [Igiven, Idig, Vdig, Imul, Vmul]

CalibrationPlots(R0Vec,RVec)
plt.show()