import numpy as np 
import NecessaryFunctions as nf
import NecessaryVariables as nv 
import matplotlib.pyplot as plt
import sys
# --------------------------------------------- MAIN --------------------------------------------- #

Wire_X = nf.CreateWire(nv.Wire_Lenght,nv.Wire_Diameter,nv.Wire_N)    # numpy arry with wire position centers.

Temp_Before = nv.T0*Wire_X**0                                 # Temperature Wire Before Starting. 
Temp_after = Temp_Before.copy()

PlotMatrix = [Temp_Before]
DiffMatrix = []

ErrCheck = "No"

R_Meas = nv.Voltage/nv.Intensity

Res_Meas = R_Meas*nv.Wire_CrossSec/nv.Wire_Lenght

alpha = nv.Material.con/(nv.Material.rho*nv.Material.Cp)
#Expected_Temp = round(nv.T0 + 1.0/alpha*(Res_Meas/nv.Material.Resist-1.0),0)
Expected_Temp = 410

Ems_a = nv.Min_Ems; Ems_b = nv.Max_Ems; Ems_c = nv.Material.eps
print(nv.Material.eps)

for k in range(0,nv.NEms):

    # --------------------- Reaching Steady State.... --------------------- #
    for m in range(0,nv.Ntime):
        Temp_Before = Temp_after.copy()
        dTemp = nf.TemperatureChange(nv.dt,Wire_X,Temp_Before)

        Temp_after = Temp_Before + dTemp
        PlotMatrix += [Temp_after]
        DiffMatrix += [np.max(np.abs(Temp_Before-Temp_after))]
        
        if DiffMatrix[-1] < nv.SSerror:
            print("Steady State Reached")
            
            nf.PlotSteadyStateTemp(PlotMatrix[-1])
            nf.PlotDiffMatrix(DiffMatrix)
            
            ErrCheck = "Yes"
            break
    
    if ErrCheck != "Yes": 
        print("Steady State not Reached, increase number of time steps.")
        nf.PlotSteadyStateTemp(PlotMatrix[-1])
        nf.PlotDiffMatrix(DiffMatrix)
        sys.exit()
    sys.exit()
    # ------ ---------- Checking Simulated temperature with expeted Temp ------ #
    Sim_MeanTemp = np.mean(Temp_after)
    
    print("")
    print("")
    print("Expected Temperature: ",Expected_Temp)
    print("Simulated Temperature: ",Sim_MeanTemp)
    print("")
    print("")

    if nv.Emserror > abs(Sim_MeanTemp-Expected_Temp):
        print("Emissivity Convergence REached!"); sys.exit()
    else:
        if Sim_MeanTemp > Expected_Temp: 
            Ems_a = Ems_c; Ems_c = (Ems_a+Ems_b)/2.0
            nv.Material.eps = Ems_c
        else: 
            Ems_b = Ems_c; Ems_c = (Ems_a+Ems_b)/2.0
            nv.Material.eps = Ems_c


        print(nv.Material.eps)

print("Final Emissivity: ",nv.Material.eps)





