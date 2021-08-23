import numpy as np
import matplotlib.pyplot as plt

def Read_ResT(filename):
    f = open(filename);  T, Res = [],[]
    for cont,l in enumerate(f,start=0):
        asd = l.split("\t")
        if cont > 1: 
            T += [float(asd[0])]; Res += [float(asd[2].split("\n")[0])]
            
    return T, Res
def Plot_TRes(filename):
    fig, axs = plt.subplots(1,2,constrained_layout = True, figsize=(10,4))
    T, Res = Read_ResT(filename)
    
    z = np.polyfit(np.array(T),np.array(Res),2)
    w = np.polyfit(np.array(T),np.array(Res)/Res[0],2)

    polz, polw = [], []
    for k in range(0,len(T)):
        polz += [z[0]*T[k]**2+z[1]*T[k]+z[2]]
        polw += [w[0]*T[k]**2+w[1]*T[k]+w[2]]
        axs[0].errorbar(T[k],Res[k],marker="s",mfc="blue",mec="blue",ms=5,lw=3,c="blue")
        axs[1].errorbar(T[k],Res[k]/Res[0],marker="s",mfc="blue",mec="blue",ms=5,lw=3,c="blue")

    axs[0].plot(T,polz,color="grey",lw=3,ls="dashed")
    axs[1].plot(T,polw,color="grey",lw=3,ls="dashed")

    axs[0].set_ylabel("Resistivity [Ohm m]",fontsize=14)
    axs[0].set_xlabel("Temperature [K]",fontsize=14)
    axs[1].set_ylabel("Res/Res0",fontsize=14)
    axs[1].set_xlabel("Temperature [K]",fontsize=14)
    fig.suptitle("Literature: R vs T",fontsize=14)

    textstr0 = str('{:0.3e}'.format(z[0]))+" T^2 + "+str('{:0.3e}'.format(z[1]))+" T + "+str('{:0.3e}'.format(z[2]))
    textstr1 = str('{:0.3e}'.format(w[0]))+" T^2 + "+str('{:0.3e}'.format(w[1]))+" T + "+str('{:0.3e}'.format(w[2]))
    axs[0].text(0.05, 0.95, textstr0, transform=axs[0].transAxes, fontsize=14,
        verticalalignment='top')
    axs[1].text(0.05, 0.95, textstr1, transform=axs[1].transAxes, fontsize=14,
        verticalalignment='top')

    plt.show()

def Read_RI(filename):
    vI, vR, vT = [],[],[]
    f = open(filename)
    for count,l in enumerate(f,start=0):
        if count > 1:
            asd = l.split(" ")
            vI += [float(asd[0])]; vR += [float(asd[38])]

    return vI, vR
def FromMeasuredR_to_T(filename):
    # Res(T) = a*T^2+b*T+c
    a = 9.521e-7; b = 3.015e-3; d = 2.938e-2
    vI, vR = Read_RI(filename)
    fact = (np.pi*(0.1e-3)**2.0)/(2e-2)
    R0 = 0.0285
    vT = []
    for R in vR: 
        print(R)
        c = d - R/R0
        print(R/R0)
        vT += [(-b+np.sqrt(b**2-4*a*c))/(2*a)]

    return vI, vR, vT

def Plot_IntensityTemperature(filename):
    fig, axs = plt.subplots(1,1,constrained_layout = True, figsize=(10,4))
    vI, vR, vT = FromMeasuredR_to_T(filename)
    axs.scatter(vI,vT,color="red",lw=3)
    axs.set_xlabel("Intensity [A]",fontsize=14)
    axs.set_ylabel("Temperature [K]",fontsize=14)
    plt.show()

# -------------------------------- MAIN ------------------------- #
#filename = "Emissivity_Analysis/Copper_Res(T).txt"
#Plot_TRes(filename)

filename = "Emissivity_Measurement/LittleResults/Copper_IR.txt"
Plot_IntensityTemperature(filename)