from matplotlib.collections import PolyCollection
import numpy as np
import matplotlib.pyplot as plt
import os
from numpy.lib.financial import ppmt
from scipy.optimize import curve_fit

def Cal_GV0(vadc): return 1./0.43219*(vadc - 0.012721)
def Cal_GV1(vadc): return 1./0.885568*(vadc - 0.05580)
def Cal_GV2(vadc): return 1./1.7285*(vadc - 0.07591)
def Cal_GI0(iadc): return 1./1.03126*(iadc + 0.00465)
def Cal_GI1(iadc): return 1./1.80851*(iadc - 0.00279826)

def R0_func(I,A,B): return A+B*I**2

def ReadSummaryFile(filename):
    f = open(filename)
    V_Name,V_av, V_std, I_av, I_std, R_av, R_std = [],[],[],[],[],[],[]
    Cal_I, Cal_V = [],[]
    for cont, l in enumerate(f,start=0):
        if cont > 1:
            asd = l.split("\t")
            V_Name += [float(asd[0].split("RMeas")[-1])]
            I_av += [float(asd[1])]; I_std += [float(asd[2])]
            V_av += [float(asd[3])]; V_std += [float(asd[4])]
            R_av += [float(asd[5])]; R_std += [float(asd[6])]
            Cal_I += [int(asd[7])]; Cal_V += [int(asd[8].split("\n")[0])]
    f.close()
    V_Name = np.array(V_Name)
    V_av = np.array(V_av); V_std = np.array(V_std)
    I_av = np.array(I_av); I_std = np.array(I_std)
    R_av = np.array(R_av); R_std = np.array(R_std)
    Cal_I = np.array(Cal_I); Cal_V = np.array(Cal_V)

    return V_Name, V_av, V_std, I_av, I_std, R_av, R_std, Cal_I, Cal_V

def AppyCalibration(V_name, V_av, I_av, Cal_I, Cal_V):
    Inew, Vnew, Rnew = [],[],[]
    for k in range(0,len(V_name)):
        if Cal_I[k] == 0: Inew += [Cal_GI0(I_av[k])]
        if Cal_I[k] == 1: Inew += [Cal_GI1(I_av[k]) ]
        if Cal_V[k] == 0: Vnew += [Cal_GV0(V_av[k])]
        if Cal_V[k] == 1: Vnew += [Cal_GV1(V_av[k])]
        if Cal_V[k] == 2: Vnew += [Cal_GV2(V_av[k])]
    
    Inew = np.array(Inew); Vnew = np.array(Vnew)
    Rnew = Vnew/Inew

    return Inew, Vnew, Rnew

def Plot_Summary_CalVSNoCal(V_nam, V_av, V_std, I_av, I_std, R_av, R_std,Inew,Vnew,Rnew):
    fig, axs = plt.subplots(1, 3,figsize=(12,5))

    axs[0].set_title("Voltage Measurement",fontsize=14)
    axs[0].errorbar(V_nam,V_av,xerr=None, yerr = V_std, marker = "s", ls="None", color="royalblue",label= "w.o Calibration")
    axs[0].errorbar(V_nam,Vnew,xerr=None, yerr = V_std, marker = "s", ls="None", color="navy",label = "Calibrated") 
    axs[0].legend(fontsize=12)
    axs[0].tick_params(axis='both', which='major', labelsize=14)
    axs[0].set_xlabel("Expected I [mA]",fontsize=14)
    axs[0].set_ylabel("Measured V [V]",fontsize=14)

    axs[1].set_title("Intensity Measurement",fontsize=14)
    axs[1].errorbar(V_nam,I_av,xerr=None, yerr = I_std,marker = "s", ls="None", color="limegreen",label= "w.o Calibration")
    axs[1].errorbar(V_nam,Inew,xerr=None, yerr = I_std,marker = "s", ls="None", color="darkgreen",label= "Calibration")
    axs[1].legend(fontsize=12)
    axs[1].tick_params(axis='both', which='major', labelsize=14)
    axs[1].set_xlabel("Expected I [mA]",fontsize=14)
    axs[1].set_ylabel("Measured I [A]",fontsize=14)

    axs[2].set_title("Resistance Measurement",fontsize=14)
    axs[2].errorbar(V_nam,R_av,xerr=None, yerr = R_std,marker = "s", ls="None", color="tomato",label= "w.o Calibration")
    axs[2].errorbar(V_nam,Rnew,xerr=None, yerr = R_std,marker = "s", ls="None", color="darkred",label= "Calibration")
    axs[2].legend(fontsize=12)
    axs[2].tick_params(axis='both', which='major', labelsize=14)
    axs[2].set_xlabel("Expected I [mA]",fontsize=14)
    axs[2].set_ylabel("Measured R [Ohm]",fontsize=14)
    plt.tight_layout()
    plt.show()

def Calculate_R0_Plot(I,V,R):

    popt,pcov = curve_fit(R0_func,I[5:15],R[5:15])
    yfit = R0_func(I,popt[0],popt[1])
    cname = "R = "+ str(round(popt[0],3))+" + "+str(round(popt[1],3))+" I^2"
    fig, axs = plt.subplots(1, 1,figsize=(5,5))
    axs.set_title("Resistance Measurement",fontsize=14)
    axs.errorbar(I,R,xerr=None,marker = "s", ls="None", color="black",label= "Measured R")
    axs.errorbar(I[5:15],R[5:15],xerr=None,marker = "s", ls="None", color="darkred",label= "Points for R0")
    axs.errorbar(I,yfit,xerr=None, ls="dashed", color="indianred",lw=3,label=cname)
    axs.legend(fontsize=12)
    axs.tick_params(axis='both', which='major', labelsize=14)
    axs.set_xlabel("Measured I [mA]",fontsize=14)
    axs.set_ylabel("Measured R [Ohm]",fontsize=14)
    plt.tight_layout()

    fig2, axs2 = plt.subplots(1, 1,figsize=(5,5))
    axs2.set_title("Resistance Measurement",fontsize=14)
    axs2.errorbar(I,R/popt[0],xerr=None,marker = "s", ls="None", color="black",label= "Measured R")
    #axs2.legend(fontsize=12)
    axs2.tick_params(axis='both', which='major', labelsize=14)
    axs2.set_xlabel("Measured I [mA]",fontsize=14)
    axs2.set_ylabel(" R/R0 ",fontsize=14)

    plt.show()

    return popt[0]

def Read_ResT(filename):
    f = open(filename);  T, Res = [],[]
    for cont,l in enumerate(f,start=0):
        asd = l.split("\t")
        if cont > 1: 
            T += [float(asd[0])]; Res += [float(asd[2].split("\n")[0])]
            
    return T, Res

def Calculate_IT_Plot(Imeas,Rmeas, R0, theofile):
    T, Rtheo = Read_ResT(theofile)

    #      Res(T) = a*T^2+b*T+c
    a = 3.65e-7; b = 4.77e-3; d = 5.862e-2
    vT = []
    for R in Rmeas: 
        print(R)
        c = d - R/R0
        print(R/R0)
        vT += [(-b+np.sqrt(b**2-4*a*c))/(2*a)]


    fig, axs = plt.subplots(1,1,constrained_layout = True, figsize=(6,6))
    axs.scatter(Imeas,vT,color="red",lw=3)
    axs.set_xlabel("Intensity [A]",fontsize=14)
    axs.set_ylabel("Temperature [K]",fontsize=14)
    plt.show()
# ---------------------------------------------------------------- # 

cwd = os.getcwd()
V_name, V_av, V_std, I_av, I_std, R_av, R_st, Cal_I, Cal_V = ReadSummaryFile(cwd+"/NonVacuumData/WAu_100um/FolderSummary.txt")

Inew, Vnew, Rnew = AppyCalibration(V_name, V_av, I_av, Cal_I, Cal_V)

Plot_Summary_CalVSNoCal( V_name, V_av, V_std, I_av, I_std, R_av, R_st,Inew,Vnew,Rnew)

#R0 = Calculate_R0_Plot(Inew,Vnew,Rnew)

#theofile = cwd+"/Emissivity_Analysis/Tungsten_Res(T).txt"
#Calculate_IT_Plot(Inew,Rnew,R0,theofile)
