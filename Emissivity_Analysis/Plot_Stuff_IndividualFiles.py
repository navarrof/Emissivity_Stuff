import numpy as np
import matplotlib.pyplot as plt
import os

def Read_AdcFile(filename,adcRate):
    v_V, v_I, v_Time  = [],[], []
    f = open(filename)
    k = 0
    for cont, l in enumerate(f,start=0):
        asd = l.split()
        if cont > 1:
            v_Time += [k*adcRate]
            v_V += [abs(float(asd[1]))-abs(float(asd[0]))]
            v_I += [abs(float(asd[4]))-abs(float(asd[3]))]
            k += 1
    f.close()
    v_V = np.array(v_V)
    v_I = np.array(v_I)
    v_R = abs(v_V)/abs(v_I)

    return v_Time, v_V, v_I, v_R

def Plot_AdcFile(Start, End, Time, V,I,R,filename):

    Av_I = np.mean(I[Start:End]); Std_I = np.std(I[Start:End])
    Text_I = "I = " + str(round(Av_I,5))+" +- "+str(round(Std_I,5))
    Av_V = np.mean(V[Start:End]); Std_V = np.std(V[Start:End])
    Text_V = " V = " +str(round(Av_V,5))+" +- "+str(round(Std_V,5))
    Av_R = np.mean(R[Start:End]); Std_R = np.std(R[Start:End])
    Text_R = " R = "+str(round(Av_R,5))+" +- "+str(round(Std_R,5))

    fig, axs = plt.subplots(2, 2,figsize=(12,5))
    fig.suptitle(filename.split("/")[-1].split(".")[0],fontsize=16)
    axs[0][0].plot(Time,V, color='royalblue',label=Text_V)
    axs[0][0].axvline(x = Time[Start], lw = 2, color="gray", ls="dashed")
    axs[0][0].axvline(x = Time[End], lw = 2, color="gray", ls="dashed")
    #axs[0][0].set_xlim([0.1, 1000]); axs[0][0].set_ylim([-0.1, 5])
    axs[0][0].tick_params(axis='both', which='major', labelsize=14)
    axs[0][0].set_xlabel("Time [s]",fontsize=14)
    axs[0][0].set_ylabel("Voltage [V]",fontsize=14)
    axs[0][0].legend(fontsize=10)

    axs[0][1].plot(Time,I, color='forestgreen',  label=Text_I)
    axs[0][1].axvline(x = Time[Start], lw = 2, color="gray", ls="dashed")
    axs[0][1].axvline(x = Time[End], lw = 2, color="gray", ls="dashed")
    #axs[0][1].set_xlim([0.1, 1000]); axs[0][1].set_ylim([-0.1, 5])
    axs[0][1].tick_params(axis='both', which='major', labelsize=14)
    axs[0][1].set_xlabel("Time [s]",fontsize=14)
    axs[0][1].set_ylabel("Intensity [A]",fontsize=14)
    axs[0][1].legend(fontsize=10)

    axs[1][0].plot(Time,R, color='darkred', label=Text_R)
    axs[1][0].axvline(x = Time[Start], lw = 2, color="gray", ls="dashed")
    axs[1][0].axvline(x = Time[End], lw = 2, color="gray", ls="dashed")
    #axs[1][0].set_xlim([0.1, 1000]); axs[1][0].set_ylim([0.0, 3])
    axs[1][0].tick_params(axis='both', which='major', labelsize=14)
    axs[1][0].set_xlabel("Time [s]",fontsize=14)
    axs[1][0].set_ylabel("Resistance [Ohm]",fontsize=14)
    axs[1][0].legend(fontsize=10)

    axs[1][1].plot(Time,R, color='darkred',  label="Not Cal")
    #axs[1][1].set_xlim([0.1, 10]); axs[1][1].set_ylim([0.0, 3])
    axs[1][1].tick_params(axis='both', which='major', labelsize=14)
    axs[1][1].set_xlabel("Time [s]",fontsize=14)
    axs[1][1].set_ylabel("Resistence [Ohm]",fontsize=14)

    plt.show()

def CalculateAverageToFile(Start, End, V,I,R,filename,filename_toWrite, CalCircuit_V, CalCircuit_I):
    g = open(filename_toWrite,"a+")
    Name = filename.split("/")[-1].split(".")[0]

    Av_I = np.mean(I[Start:End]); Std_I = np.std(I[Start:End])
    Av_V = np.mean(V[Start:End]); Std_V = np.std(V[Start:End])
    Av_R = np.mean(R[Start:End]); Std_R = np.std(R[Start:End])

    g.write(Name+"\t")
    g.write(str(round(Av_I,5))+"\t"+str(round(Std_I,5))+"\t")
    g.write(str(round(Av_V,5))+"\t"+str(round(Std_V,5))+"\t")
    g.write(str(round(Av_R,5))+"\t"+str(round(Std_R,5))+"\t")
    g.write(str(CalCircuit_I)+"\t"+str(CalCircuit_V)+"\n")

    g.close()



# ------------------------------------------------------------------ #
cwd = os.getcwd()
filename = cwd + "/NonVacuumData/WAu_100um/RMeas250.txt"
Time, V, I, R = Read_AdcFile(filename,10e-3)

Start = 3000; End = 6000
#Start = 2000; End = 5000
Plot_AdcFile(Start, End, Time, V, I, R,filename)

filename_toWrite = cwd+"/NonVacuumData/WAu_100um/FolderSummary.txt"

CalCircuit_V = 1; CalCircuit_I = 1
CalculateAverageToFile(Start,End,V,I,R,filename,filename_toWrite, CalCircuit_V, CalCircuit_I)