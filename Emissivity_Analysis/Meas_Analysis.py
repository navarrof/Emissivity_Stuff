import numpy as np
import glob 
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy import signal

def Func(t,a,b):
    y = a*(1-np.exp(-t*b))
    return y

def readMeas(filename, AdcRate):
    f = open(filename,"r")
    t = 0
    V = []; I = []; R =[]; T1 = []; T2 = []; Time = []
    for count,l in enumerate(f, start=0):
        if count > 1:
            asd = l.split(" ")
            voltage = float(asd[13])*2.0; intensity = float(asd[27])
            if (intensity > 0.1e-2) and (voltage > 0.0):
                R += [float(asd[32])]
            else:
                R += [0.0]
            
            V += [voltage]; I += [intensity]
            T1 += [float(asd[37])]; T2 += [float(asd[42].split("\n")[0])]
            Time += [t*AdcRate]; 

            t+= 1

    return Time, V, I, R, T1, T2
    
def PlotAllFiles(AdcRate):
    #namevec = glob.glob("Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/R0*")
    foldername = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/R0"
    namevec = [foldername+"Meas_50.0mA.txt"]
    namevec += [foldername+"Meas_90.0mA.txt"]

    Vec_Start = 300*np.array(range(len(namevec)))**0.0
    Vec_End = 300*np.array(range(len(namevec)))**0.0

    fig, axs = plt.subplots(1,1,constrained_layout = True, figsize=(10,8))

    for k in range(0,len(namevec)):
        Time, V,I,R,T1,T2 = readMeas(namevec[k], AdcRate)
        popt, pcov = curve_fit(Func, Time, I)

        print()
        print(namevec[k])
        print("I_st: " + str(popt[0])+" [A]     Tao: "+str(popt[1])+" [ms]")
        print()

        axs.plot(np.array(Time),I,color="green")
        axs.plot(np.array(Time),V,linestyle="dashed")
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

    plt.plot(Time, R, color="firebrick",marker="s",ms=5)

    plt.ylabel("Resistence [Ohm]",fontsize=14)
    plt.xlabel("Time [ms]",fontsize=14)
    plt.xticks(fontsize=14); plt.yticks(fontsize=14)
    #plt.xlim(0,80)

    plt.show()

def FitResistance(time,r):

    tt, rr, yfit = [], [], []; start = 0; end = 0
    for i in range(0,len(r)):
        if (r[i] > 0.5) and (start == 0): 
            asd = r[i]; start = i; s2 = int(start+5)
            rr += [r[i]-np.mean(r[start:s2])]; tt += [time[i]-time[start]]
        elif (r[i] > 0.5):
            s2 = int(start+5)
            rr += [r[i]-np.mean(r[start:s2])]; tt += [time[i]-time[start]]
        elif (start != 0) and (end == 0): end = i
    if end == 0: end = i

    popt, pcov = curve_fit(Func, tt, rr,bounds=([0.0,0.0],[3.0,5.0]))

    for k in range(0,len(tt)):
        yfit += [Func(tt[k],*popt)]

    tt = np.array(tt)+time[start]*np.array(tt)**0
    return tt, rr, yfit, popt, start, end 

def PlotR0FitExample(filename1,filename2,AdcRate):
    Time_1, V_1,I_1,R_1,T1_1,T2_1 = readMeas(filename1, AdcRate)
    Time_2, V_2,I_2,R_2,T1_2,T2_2 = readMeas(filename2, AdcRate)

    XX_1, RR_1, yfit_1, par_1 = FitResistance(Time_1, R_1)
    XX_2, RR_2, yfit_2, par_2 = FitResistance(Time_2, R_2)

    plt.figure(figsize=(8,6))
    plt.plot(XX_1,RR_1,color = "indianred",ls="None", marker="s",ms= 4,label= "I = 0.7 [A]")
    plt.plot(XX_1,yfit_1, color = "black", lw = 2, ls="dashed")
    plt.plot(XX_2,RR_2, color = "seagreen", ls="None", marker="s",ms=4, label = "I = 0.9 [A]")
    plt.plot(XX_2,yfit_2, color = "black",lw=2, ls="dashed")

    plt.xlabel('Time [ms]',fontsize=14)
    plt.ylabel("AR [Ohm]",fontsize=14)
    plt.xticks(fontsize=14); plt.yticks(fontsize=14)

    plt.legend(loc="lower right",fontsize=14)
    text1 = r'$ \Delta R (t) = ' +str(round(par_1[0],4)) +r'\cdot \left( 1 - exp\left(- '+str(round(par_1[1],4)) +r'\cdot t\right) \right)$'
    text2 = r'$ \Delta R (t) = ' +str(round(par_2[0],4)) +r'\cdot \left( 1 - exp\left(- '+str(round(par_2[1],4)) +r'\cdot t\right) \right)$'

    plt.text(1150,0.38,text1, fontsize=14)
    plt.text(1150,0.54,text2, fontsize=14)

    plt.xlim(-50,3000)

    plt.show()

def Plot_SummaryResult(filename, AdcRate): 
    Time, V,I,R,T1,T2 = readMeas(filename, AdcRate)
    XX_1, RR_1, yfit_1, par_1, start, end = FitResistance(Time, R)
    fig, axs = plt.subplots(2,2,constrained_layout = True, figsize=(10,7))

    fig.suptitle(filename.split("/")[-1],fontsize=14)

    if len(filename.split("R0")) > 1: 
        Ixstart = int(Time[start]+500); Ixend = int(Time[end] - 1)
        Imean = np.mean(I[Ixstart:Ixend])
        Vxstart = int(Time[start]+1800); Vxend = int(Time[end]-1)
        Vmean = np.mean(V[Vxstart:Vxend])
        Rxstart = int(Time[start]+1500); Rxend = int(Time[end] - 1)
        Rmean = np.mean(R[Rxstart:Rxend])
    else:
        print(start,end)
        Ixstart = int(Time[start]+10000); Ixend = int(Time[end] - 1000)
        Imean = np.mean(I[Ixstart:Ixend])
        Vxstart = int(Time[start]+10000); Vxend = int(Time[end]-1000)
        Vmean = np.mean(V[Vxstart:Vxend])
        Rxstart = int(Time[start]+10000); Rxend = int(Time[end] - 1000)
        Rmean = np.mean(R[Rxstart:Rxend])
    
    axs[0][0].plot(Time,I, color="forestgreen",ls="None",marker=".")
    axs[0][0].axvline(x=Ixstart, lw=2, ls="dashed", color="gray")
    axs[0][0].axvline(x=Ixend, lw=2, ls="dashed", color="gray")
    axs[0][0].set_xlabel("Time [ms]",fontsize=14)
    axs[0][0].set_ylabel("Intensity [A]",fontsize=14)
    axs[0][0].xaxis.set_tick_params(labelsize=14)
    axs[0][0].yaxis.set_tick_params(labelsize=14)
    
    axs[0][0].set_xlim(left=Time[start]-1000,right=Time[end]+1000)
    axs[0][0].set_ylim(bottom=-0.1, top=np.max(I)+0.2)
    axs[0][0].text(20000,0.2,r"$I_{mean} = $"+str(round(Imean,4))+" [A]",fontsize=12,bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 6})
    axs[0][1].plot(Time,V, color = "royalblue",ls="None",marker=".")
    axs[0][1].axvline(x=Vxstart, lw=2, ls="dashed", color="gray")
    axs[0][1].axvline(x=Vxend, lw=2, ls="dashed", color="gray")
    axs[0][1].set_xlabel("Time [ms]",fontsize=14)
    axs[0][1].set_ylabel("Voltage [V]",fontsize=14)
    axs[0][1].xaxis.set_tick_params(labelsize=14)
    axs[0][1].yaxis.set_tick_params(labelsize=14)
    axs[0][1].set_xlim(left=Time[start]-1000,right=Time[end]+1000)
    axs[0][1].set_ylim(bottom=-0.1, top=np.max(V)+0.2)
    axs[0][1].text(20000,0.2,r"$V_{mean} = $"+str(round(Vmean,4))+" [V]",fontsize=12,bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 6})

    axs[1][0].plot(Time,R, color = "firebrick",ls="None",marker=".")
    axs[1][0].axvline(x=Rxstart, lw=2, ls="dashed", color="gray")
    axs[1][0].axvline(x=Rxend, lw=2, ls="dashed", color="gray")
    axs[1][0].set_xlabel("Time [ms]",fontsize=14)
    axs[1][0].set_ylabel("Resistance [Ohm]",fontsize=14)
    axs[1][0].xaxis.set_tick_params(labelsize=14)
    axs[1][0].yaxis.set_tick_params(labelsize=14)
    axs[1][0].set_xlim(left=Time[start]-1000,right=Time[end]+1000)
    axs[1][0].set_ylim(bottom=-0.1, top=np.max(R)+0.2)
    axs[1][0].text(20000,0,r"$R_{mean} = $"+str(round(Rmean,4))+r"$[ \Omega ]$",fontsize=12,bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 6})
    

    axs[1][1].plot(XX_1,RR_1,color="indianred",ls="None",marker=".")
    axs[1][1].plot(XX_1,yfit_1,lw=2,ls="dashed",color="black")
    axs[1][1].set_xlabel("Time [ms]",fontsize=14)
    axs[1][1].set_ylabel(r"$\Delta R [Ohm]$",fontsize=14)
    axs[1][1].xaxis.set_tick_params(labelsize=14)
    axs[1][1].yaxis.set_tick_params(labelsize=14)
    axs[1][1].set_xlim(left=Time[start],right=Rxstart)
    axs[1][1].set_ylim(bottom=-0.1,top=np.max(RR_1)+0.02)
    text1 = r'$ \Delta R (t) = ' +str(round(par_1[0],4)) +r'\cdot \left( 1 - exp\left(- '+str(round(par_1[1],4)) +r'\cdot t\right) \right)$'
    axs[1][1].text(4800,0.0,text1,fontsize=12,bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 6})

    plt.savefig(filename.split(".")[0]+".png")
    plt.show()
    print(filename.split(".")[0]+".png")
    

def ReadFolderSummary(filesumary):
    f = open(filesumary)
    vName, vIe, vIm, vVm, vRm, va, vb = [],[],[],[],[],[],[]
    for cont,l in enumerate(f,start=0):
        asd = l.split(" ")
        print(asd)
        if cont > 1: 
            if asd[10] == "-": continue

            vName += [asd[0]]; vIe += [float(asd[5])]

            try:    vIm += [float(asd[10])]
            except ValueError:  vIm += [asd[10]]

            try: vVm += [float(asd[15])]
            except ValueError: vVm += [asd[15]]

            try: vRm += [float(asd[20])]
            except ValueError: vRm += [asd[20]]

            try: va += [float(asd[25])]
            except ValueError: va += [asd[25]]

            try: vb += [float(asd[28].split("\n")[0])]
            except ValueError: vb += [asd[28].split("\n")[0]]

    return vName, vIe, vIm, vVm, vRm, va,vb

def Plot_FolderSummary(filesumary):
    vName, vIe, vIm, vVm, vRm, va,vb = ReadFolderSummary(filesumary)
    print(vIe,vIm,vVm,vRm,va,vb)

    fig, axs = plt.subplots(2,2,constrained_layout = True, figsize=(10,7))

    fig.suptitle(filesumary.split("/")[-2],fontsize=14)
    axs[0][0].plot(vIe,vIm, color="forestgreen",ls="None",marker="o",markerfacecolor="None",markeredgewidth=1.5)
    axs[0][0].set_xlabel("$I_{expected}$ [A]",fontsize=14)
    axs[0][0].set_ylabel("$I_{measured}$ [A]",fontsize=14)
    axs[0][0].xaxis.set_tick_params(labelsize=14)
    axs[0][0].yaxis.set_tick_params(labelsize=14)
    #axs[0][0].set_xlim(left=Time[start]-1000,right=Time[end]+1000)
    #axs[0][0].set_ylim(bottom=-0.1, top=np.max(I)+0.2)

    axs[1][0].plot(vIm,vVm, color="royalblue",ls="None",marker="^",markerfacecolor="None",markeredgewidth=1.5)
    axs[1][0].set_xlabel("I [A]",fontsize=14)
    axs[1][0].set_ylabel("Voltage [V]",fontsize=14)
    axs[1][0].xaxis.set_tick_params(labelsize=14)
    axs[1][0].yaxis.set_tick_params(labelsize=14)
    #axs[1][0].set_xlim(left=Time[start]-1000,right=Time[end]+1000)
    #axs[1][0].set_ylim(bottom=-0.1, top=np.max(R)+0.2)

    axs[0][1].plot(vIm,vRm, color="firebrick",ls="None",marker="s",markerfacecolor="None",markeredgewidth=1.5)
    axs[0][1].set_xlabel('I [A]',fontsize=14)
    axs[0][1].set_ylabel(r"Resistance [$\Omega$]",fontsize=14)
    axs[0][1].xaxis.set_tick_params(labelsize=14)
    axs[0][1].yaxis.set_tick_params(labelsize=14)
    #axs[0][1].set_xlim(left=Time[start]-1000,right=Time[end]+1000)
    #axs[0][1].set_ylim(bottom=-0.1, top=np.max(V)+0.2)

    va2, vb2,vIe2 = [],[],[]
    for j in range(0,len(va)):
        if va[j] == "-": continue
        else:
            vIe2 += [vIm[j]]; va2 += [va[j]]; vb2 += [vb[j]]


    axs[1][1].plot(vIe2,va2, color="brown",ls="None",marker="+",markeredgewidth=3, label= "a")
    axs[1][1].plot(vIe2,vb2, color="darkcyan",ls="None",marker="3",markeredgewidth=3, label = "b")
    axs[1][1].set_xlabel("$I_{expected}$ [A]",fontsize=14)
    axs[1][1].set_ylabel(r"$\Delta R [Ohm]$",fontsize=14)
    axs[1][1].xaxis.set_tick_params(labelsize=14)
    axs[1][1].yaxis.set_tick_params(labelsize=14)
    axs[1][1].legend()
    text = r"$\Delta R = a \cdot \left( 1 - exp\left( - b \cdot t \right) \right)$"
    axs[1][1].text(0.3,0.6,text,fontsize=12,bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 6})
    axs[1][1].set_xlim(left=vIm[0],right=vIm[-1])
    #axs[1][1].set_ylim(bottom=-0.1,top=np.max(RR_1)+0.02)

    plt.show()

def Func_R(x,R0,A):
    return R0 + A*x**2

def Plot_TrickedR(filesumary):
    vName, vIe, vIm, vVm, vRm, va,vb = ReadFolderSummary(filesumary)
    fig, axs = plt.subplots(1,1,constrained_layout = True, figsize=(10,7))
    vI2, vR2 = [], []
    for k in range(0,len(vIe)):
        if (vIm[k] > 0.34) and (vIm[k] < 1.45):
            vI2 += [vIm[k]]; vR2 += [vRm[k]]

    #p = np.polyfit(vI2,vR2,3); 
    #print(p[0],p[1],p[2],p[3])
    #fFunc = p[3]*np.array(vI2)**0+p[2]*np.array(vI2)**1+p[1]*np.array(vI2)**2+p[0]*np.array(vI2)**3

    popt, pcov = curve_fit(Func_R, vI2[:10], vR2[:10])
    print(popt)
    fFunc = Func_R(np.array(vI2),*popt)

    #axs.plot(vI2,fFunc,color="gray",ls="dashed",lw=2)
    axs.plot(vI2,vR2/popt[0], color="firebrick",ls="None",marker="s",markerfacecolor="None",markeredgewidth=2,ms=8)
    #text = "R = "+str(round(p[3],3))+"  +"+str(round(p[2],3))+r"$\cdot I  +$"+str(round(p[1],3))+r"$\cdot I^2$   +"+str(round(p[0],3))+r"$ \cdot I^3$"
    #axs.text(vI2[0],vR2[-2],text,fontsize=12,bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 6})
    text = "R = "+str(round(popt[0],3))+"  + "+str(round(popt[1],3))+r"$\cdot I^2$"
    axs.text(vI2[0],1.4,text,fontsize=12,bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 6})

    axs.set_xlabel('I [A]',fontsize=14)
    axs.set_ylabel(r"$R/R_0$",fontsize=14)
    axs.xaxis.set_tick_params(labelsize=14)
    axs.yaxis.set_tick_params(labelsize=14)
    

    plt.show()

def Read_ResT(filename):
    f = open(filename);  T, Res = [],[]
    for cont,l in enumerate(f,start=0):
        asd = l.split("\t")
        if cont > 1: 
            T += [float(asd[0])]; Res += [float(asd[2].split("\n")[0])]
            
    return T, Res

def Plot_MeasuredResistanceIntensity(filesumary):
    vName, vIe, vIm, vVm, vRm, va,vb = ReadFolderSummary(filesumary)
    vI2, vR2 = [], []
    for k in range(0,len(vIe)):
        if (vIm[k] > 0.34) and (vIm[k] < 1.4):
            vI2 += [vIm[k]]; vR2 += [vRm[k]]
    popt, pcov = curve_fit(Func_R, vI2[:11], vR2[:11])
    print(popt)
    fFunc = Func_R(np.array(vI2),*popt)
    vRR0 = vR2/popt[0]

    filename = "Emissivity_Analysis/Tungsten_Res(T).txt"
    T,Res = Read_ResT(filename)
    w = np.polyfit(np.array(T),np.array(Res)/Res[0],2)

    vTmeas = []
    for k in range(0,len(vI2)):
        coeff = [w[0],w[1],w[2]-vRR0[k]]
        sol = np.roots(coeff)
        vTmeas += [sol[1]]
        print(sol)

    fig, axs = plt.subplots(1,1,constrained_layout = True, figsize=(6,5))
    
    axs.plot(vI2,vTmeas, color="mediumorchid",ls="None",marker="s",markerfacecolor="None",markeredgewidth=2,ms=8)
    axs.set_xlabel('I [A]',fontsize=14)
    axs.set_ylabel("Temperature [K]",fontsize=14)
    axs.xaxis.set_tick_params(labelsize=14)
    axs.yaxis.set_tick_params(labelsize=14)
    plt.show()









# ------------------------- MAIN ------------------------ #

AdcRate = 1.0

#PlotAllFiles(AdcRate)

#filename = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try4/RMeas1250.txt"
#PlotExpectedIntensity(AdcRate,filename)
#PlotR0Example(filename,AdcRate)

#filename1 = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/R0Meas_300.0mA.txt"
#filename2 = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try3/RMeas13.txt"

#PlotExpectedIntensity(AdcRate,filename2)
#PlotR0FitExample(filename1, filename2, AdcRate)

#PlotAllFiles(AdcRate)

#Plot_SummaryResult(filename,AdcRate)

filesumari = "Emissivity_Measurement/OutputFiles/Tungsten_NoVacuum_Try4/SummaryResults.txt"
#Plot_FolderSummary(filesumari)
#Plot_TrickedR(filesumari)

Plot_MeasuredResistanceIntensity(filesumari)