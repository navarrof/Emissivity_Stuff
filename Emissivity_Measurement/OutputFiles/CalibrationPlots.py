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

def ReadCalFile2(Filename):
    f = open(Filename)
    Igiven, Idig, Imul = [],[],[]
    for l in f: 
        asd = l.split(" ")
        if asd[0] == "#": continue
        else: 
            Igiven += [float(asd[0])]
            Idig += [float(asd[5])]
            Imul += [float(asd[10])]

    return Igiven, Idig, Imul 

def CalibrationPlots(R0Vec,RVec):

    Igiven_R0 = np.array(R0Vec[0]); Idig_R0 = np.array(R0Vec[1]); 
    Vdig_R0 = np.array(R0Vec[2]); Imul_R0 = np.array(R0Vec[3]); Vmul_R0 = np.array(R0Vec[4])
    Igiven_R = np.array(RVec[0]); Idig_R = np.array(RVec[1]); Vdig_R = np.array(RVec[2]); 
    Imul_R = np.array(RVec[3]); Vmul_R = np.array(RVec[4])

    
    fig, axs = plt.subplots(2,2,constrained_layout = True, figsize=(12,8))
    fig.suptitle("Circuit 1: Slope Error", fontsize=16)

    axs[0,0].plot(Imul_R0,(Idig_R0-Imul_R0)/Imul_R0*100.0,label="Circuit R0",color="forestgreen",ls="dashed",marker="o",lw=2)
    axs[0,0].plot(Imul_R,(Idig_R-Imul_R)/Imul_R*100.0,label="Circuit R",color="firebrick",ls="dashed",marker="o",lw=2)
    axs[0,0].plot(Imul_R,Imul_R*0.0,label="Circuit R",color="grey",ls="dashed",marker="None",lw=2)
    axs[0,0].set_xlabel("Multimeter Intensity [A]",fontsize=14)
    axs[0,0].set_ylabel("Relative Error [%]",fontsize=14)
    axs[0,0].legend(fontsize=14)
    axs[0,0].xaxis.set_tick_params(labelsize=14)
    axs[0,0].yaxis.set_tick_params(labelsize=14)
    axs[0,0].set_xlim(0.02,0.45)
    #axs[0,0].set_ylim(0.02,0.4)

    axs[0,1].plot(Vmul_R0,(Vdig_R0-Vmul_R0)/Vmul_R0*100,label="Circuit R0", color = "royalblue",ls="dashed",marker="o",lw=2)
    axs[0,1].plot(Vmul_R,(Vdig_R-Vmul_R)/Vmul_R*100,label="Circuit R", color = "darkorange",ls="dashed",marker="o",lw=2)
    axs[0,1].plot(Vmul_R,Vmul_R*0.0,label="Circuit R",color="grey",ls="dashed",marker="None",lw=2)
    axs[0,1].set_xlabel("Multimeter Voltage [V]",fontsize=14)
    axs[0,1].set_ylabel("Relative Error [%]",fontsize=14)
    axs[0,1].legend(fontsize=14)
    axs[0,1].xaxis.set_tick_params(labelsize=14)
    axs[0,1].yaxis.set_tick_params(labelsize=14)
    axs[0,1].set_xlim(0.02,0.55)
    #axs[0,1].set_ylim(0.02,1.0)

    axs[1,0].plot(Imul_R,(Idig_R-Imul_R)/Imul_R*100,label="Intensity",color = "goldenrod",ls="dashed",marker="o",lw=2)
    axs[1,0].plot(Imul_R,Imul_R*0.0,label="Circuit R",color="grey",ls="dashed",marker="None",lw=2)
    axs[1,0].set_xlabel("Multimeter Intensity [A]",fontsize=14)
    axs[1,0].set_ylabel("Relative Error [%]",fontsize=14)
    axs[1,0].legend(fontsize=14)
    axs[1,0].xaxis.set_tick_params(labelsize=14)
    axs[1,0].yaxis.set_tick_params(labelsize=14)

    axs[1,1].plot(Vmul_R,(Vdig_R-Vmul_R)/Vmul_R*100,label="Voltage",color = "purple",ls="dashed",marker="o",lw=2)
    axs[1,1].plot(Vmul_R,Vmul_R*0.0,label="Circuit R",color="grey",ls="dashed",marker="None",lw=2)
    axs[1,1].set_xlabel("Multimeter Voltage [V]",fontsize=14)
    axs[1,1].set_ylabel("Relative Error [%]",fontsize=14)
    axs[1,1].legend(fontsize=14)
    axs[1,1].xaxis.set_tick_params(labelsize=14)
    axs[1,1].yaxis.set_tick_params(labelsize=14)


    fig, axs = plt.subplots(2,2,constrained_layout = True, figsize=(12,8))
    fig.suptitle("Circuit 1: Offset Error", fontsize=16)

    y45 = []
    for k in range(0,100): y45 += [k] 

    axs[0,0].plot(Imul_R0,Idig_R0,label="Circuit R0",color="forestgreen",ls="dashed",marker="o",lw=2)
    axs[0,0].plot(Imul_R,Idig_R,label="Circuit R",color="firebrick",ls="dashed",marker="o",lw=2)
    axs[0,0].plot(y45,y45,label="Reference",color="grey",ls="dashed",marker="None",lw=2)
    axs[0,0].set_xlabel("Multimeter Intensity [A]",fontsize=14)
    axs[0,0].set_ylabel("Intensity [A]",fontsize=14)
    axs[0,0].legend(fontsize=14)
    axs[0,0].xaxis.set_tick_params(labelsize=14)
    axs[0,0].yaxis.set_tick_params(labelsize=14)
    axs[0,0].set_xlim(0.02,0.45)
    axs[0,0].set_ylim(0.002,0.5)

    axs[0,1].plot(Vmul_R0,Vdig_R0,label="Circuit R0", color = "royalblue",ls="dashed",marker="o",lw=2)
    axs[0,1].plot(Vmul_R,Vdig_R,label="Circuit R", color = "darkorange",ls="dashed",marker="o",lw=2)
    axs[0,1].plot(y45,y45,label="Reference", color = "grey",ls="dashed",marker="None",lw=2)
    axs[0,1].set_xlabel("Multimeter Voltage [V]",fontsize=14)
    axs[0,1].set_ylabel("Voltage [V]",fontsize=14)
    axs[0,1].legend(fontsize=14)
    axs[0,1].xaxis.set_tick_params(labelsize=14)
    axs[0,1].yaxis.set_tick_params(labelsize=14)
    axs[0,1].set_xlim(0.02,0.55)
    axs[0,1].set_ylim(0.02,0.6)

    axs[1,0].plot(Imul_R,Idig_R,label="Intensity",color = "goldenrod",ls="dashed",marker="o",lw=2)
    axs[1,0].plot(y45,y45,label="Reference",color = "grey",ls="dashed",marker="None",lw=2)
    axs[1,0].set_xlabel("Multimeter Intensity [A]",fontsize=14)
    axs[1,0].set_ylabel("Intensity [A]",fontsize=14)
    axs[1,0].legend(fontsize=14)
    axs[1,0].xaxis.set_tick_params(labelsize=14)
    axs[1,0].yaxis.set_tick_params(labelsize=14)
    axs[1,0].set_xlim(0.02,1.5)
    axs[1,0].set_ylim(0.02,2.0)

    axs[1,1].plot(Vmul_R,Vdig_R,label="Voltage",color = "purple",ls="dashed",marker="o",lw=2)
    axs[1,1].plot(y45,y45,label="Reference",color = "grey",ls="dashed",marker="None",lw=2)
    axs[1,1].set_xlabel("Multimeter Voltage [V]",fontsize=14)
    axs[1,1].set_ylabel("Voltage [V]",fontsize=14)
    axs[1,1].legend(fontsize=14)
    axs[1,1].xaxis.set_tick_params(labelsize=14)
    axs[1,1].yaxis.set_tick_params(labelsize=14)
    axs[1,1].set_xlim(0.02,4.0)
    axs[1,1].set_ylim(0.02,4.0)

def PlotCalibrationFactors(R0Vec,RVec):
    Igiven_R0 = np.array(R0Vec[0]); Idig_R0 = np.array(R0Vec[1]); 
    Vdig_R0 = np.array(R0Vec[2]); Imul_R0 = np.array(R0Vec[3]); Vmul_R0 = np.array(R0Vec[4])
    Igiven_R = np.array(RVec[0]); Idig_R = np.array(RVec[1]); Vdig_R = np.array(RVec[2]); 
    Imul_R = np.array(RVec[3]); Vmul_R = np.array(RVec[4])

    fig, axs = plt.subplots(1,2,constrained_layout = True, figsize=(12,5))
    fig.suptitle("Circuit 1: Calibration Factors", fontsize=16)
    axs[0].plot(Imul_R,Imul_R/Idig_R,color = "darkblue",ls="dashed",marker="o",lw=2)
    axs[0].plot(Imul_R,Imul_R/Imul_R,color = "grey",ls="dashed",marker="None",lw=2)
    axs[0].set_xlabel("Intensity [A]",fontsize=14)
    axs[0].set_ylabel("Calibration Factor",fontsize=14)
    axs[0].xaxis.set_tick_params(labelsize=14)
    axs[0].yaxis.set_tick_params(labelsize=14)

    axs[1].plot(Vmul_R,Vmul_R/Vdig_R,color = "darkred",ls="dashed",marker="o",lw=2)
    axs[1].plot(Vmul_R,Vmul_R/Vmul_R,color = "grey",ls="dashed",marker="None",lw=2)
    axs[1].set_xlabel("Voltage [V]",fontsize=14)
    axs[1].set_ylabel("Calibration Factor",fontsize=14)
    axs[1].xaxis.set_tick_params(labelsize=14)
    axs[1].yaxis.set_tick_params(labelsize=14)

    g = open("CalibrationFactors_Circuit1_Intensity.txt","w")
    g.write("# ----------------------------------------------------- #\n")
    g.write("#  Intensity Calibration Factor: Circuit 1              #\n")
    g.write("# ----------------------------------------------------- #\n")
    g.write("# ADC Intensity [A]             Calibration             #\n")
    g.write("# ----------------------------------------------------- #\n")

    for k in range(0,len(Imul_R)):
        rk = Imul_R[k]/Idig_R[k]
        g.write(str(round(Imul_R[k],4))+"     "+str(round(rk,4))+"\n")
    
    g.close()

    h = open("CalibrationFactors_Circuit1_Voltage.txt","w")
    h.write("# ----------------------------------------------------- #\n")
    h.write("#  Voltage Calibration Factor: Circuit 1              #\n")
    h.write("# ----------------------------------------------------- #\n")
    h.write("# ADC Voltage [V]             Calibration             #\n")
    h.write("# ----------------------------------------------------- #\n")
    for j in range(0,len(Vmul_R)):
        rj = Vmul_R[j]/Vdig_R[j]
        h.write(str(round(Vmul_R[j],4))+"     "+str(round(rj,4))+"\n")

        
    h.close()


# -------------------------- MAIN --------------------------- #


Igiven, Idig, Vdig, Imul, Vmul  = ReadCalFile("Emissivity_Measurement/OutputFiles/CalibrationR0_Circuit1")
R0Vec = [Igiven, Idig, Vdig, Imul, Vmul]
Igiven, Idig, Vdig, Imul, Vmul  = ReadCalFile("Emissivity_Measurement/OutputFiles/CalibrationR_Circuit1.txt")

Igiven2, Idig2, Imul2  = ReadCalFile2("Emissivity_Measurement/OutputFiles/CalibrationR_GoldCircuit1.txt")
RVec = [Igiven2, Idig2, Vdig, Imul2, Vmul]

#CalibrationPlots(R0Vec,RVec)

PlotCalibrationFactors(R0Vec,RVec)
plt.show()