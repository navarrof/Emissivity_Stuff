import numpy as np
import matplotlib.pyplot as plt

def readMeas(filename):
    f = open(filename,"r")

    V = []; I = []; R =[]; T1 = []; T2 = []
    for count,l in enumerate(f, start=0):
        if count > 1:
            asd = l.split(" ")
            voltage = float(asd[13]); intensity = float(asd[27])
            if (voltage > 0) & (intensity > 0):
                V += [voltage]
                I += [intensity]
                R += [float(asd[32])]
                T1 += [float(asd[37])]
                T2 += [float(asd[42].split("\n")[0])]
    return V, I, R, T1, T2

def Plot_Meas(V,I,R,T1,T2):
    fig, axs = plt.subplots(1,2,constrained_layout = True, figsize=(10,4))
    
    axs[0].set_title("Electrical Measurements",fontsize=14)
    axs[1].set_title("Temperature Measurements",fontsize=14)

    axs[0].plot(V,linewidth=2,color="royalblue",label="V [v]")
    axs[0].plot(I,linewidth=2, color = "forestgreen",label="I [A]")
    axs[0].plot(R,linewidth=2, color = "orchid",label = "R [Ohm]")

    axs[0].legend()

    axs[1].plot(T1,linewidth=2,color="indianred",label="T1 [Npulses]")
    axs[1].plot(T2,linewidth=2,color="orange",label="T2 [Npulses]")

    axs[1].legend()


    plt.show()

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

# ------------------------- MAIN ------------------------ #

V,I,R,T1,T2 = readMeas("DaTa/Copper_NoVacuum_Try3/RMeas1.txt")

Plot_Meas(V,I,R,T1,T2)
#Plot_MeasCompa("DaTa/Copper_NoVacuum_Try2/R0Meas_140.0mA.txt","DaTa/Copper_NoVacuum_Try2/R0Meas_300.0mA.txt")
