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

print("Initial Emissivity Guess: ",nv.Material.eps)

Ems_a = nv.Min_Ems; Ems_b = nv.Max_Ems; Ems_c = nv.Material.eps

for k in range(0,nv.NEms):

    # --------------------- Reaching Steady State.... --------------------- #
    for m in range(0,nv.Ntime):
        Temp_Before = Temp_after.copy()
        dTemp = nf.TemperatureChange(nv.dt,Wire_X,Temp_Before)

        Temp_after = Temp_Before + dTemp
        PlotMatrix += [Temp_after]
        DiffMatrix += [np.max(np.abs(Temp_Before-Temp_after))]
        print("Maximum Error: ",DiffMatrix[-1])

        if DiffMatrix[-1] < nv.SSerror:
            print("Steady State Reached")
            
            #nf.PlotSteadyStateTemp(PlotMatrix[-1])
            #nf.PlotDiffMatrix(DiffMatrix)

            print("Tmax: "+str(np.max(Temp_after))+"    Tmean: "+str(np.mean(Temp_after))+"   Nsteps: "+str(m))
            
            ErrCheck = "Yes"
            break
    
    if ErrCheck != "Yes": 
        print("Steady State not Reached, increase number of time steps.")
        nf.PlotSteadyStateTemp(PlotMatrix[-1])
        nf.PlotDiffMatrix(DiffMatrix)
        sys.exit()
    # ------ ---------- Checking Simulated temperature with expeted Temp ------ #
    Sim_MeanTemp = np.mean(Temp_after)
    
    print("")
    print("")
    print("Expected Temperature: ",nv.Expected_Temp)
    print("Simulated Temperature: ",Sim_MeanTemp)
    print("")
    print("")


    if Sim_MeanTemp > nv.Expected_Temp: 
        Ems_a = Ems_c; Ems_c = (Ems_a+Ems_b)/2.0
    else: 
        Ems_b = Ems_c; Ems_c = (Ems_a+Ems_b)/2.0
    
    if abs(nv.Material.eps - Ems_c) < nv.Emserror:
        print("Emissivity Convergence reached! "); break
    else: nv.Material.eps = Ems_c

print("Final Emissivity: ",nv.Material.eps)





