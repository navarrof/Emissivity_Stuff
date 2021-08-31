import numpy as np
import NecessaryVariables as nv
import matplotlib.pyplot as plt

def CreateWire(Wire_Lenght, Wire_Diameter, Wire_N):
    Wire_X = []; 
    for k in range(0,Wire_N):
        xpos = -Wire_Lenght/2 + k*nv.Wire_dx
        Wire_X += [xpos]

    Wire_X = np.array(Wire_X)
    return Wire_X


def TemperatureChange(dt,X_vec,Temp):

    dx = (X_vec[1]-X_vec[0])
    dV = nv.Wire_CrossSec*dx
    dtemp = Temp**0.0

    for j in range(0,len(X_vec)):
        Tj = Temp[j]
        if j == 0:
            Tjp1 = Temp[j+1]; Tjm1 = nv.Tleft
        elif j == len(X_vec)-1:
            Tjp1 = nv.Tright; Tjm1 = Temp[j-1]
        else:
            Tjp1 = Temp[j+1]; Tjm1 = Temp[j-1]
        
        alpha = nv.Material.con/(nv.Material.rho*nv.Material.Cp*1000)

        heat = nv.Intensity**2 * nv.R / ( nv.Material.Cp*nv.Material.rho*dV*1e6 ) 
        cold1 = nv.Material.eps * nv.BZ * ( Temp[j]**4 - nv.T0**4 ) * 2 * np.pi * (nv.Wire_Diameter/2.0) * dx / ( nv.Material.Cp*nv.Material.rho*dV*1e6 )
        cold2 = alpha*(Tjm1-2*Tj+Tjp1)/dx**2
        dtemp[j] =  heat * dt - cold1 *dt + cold2 * dt
    return dtemp

def PlotSteadyStateTemp(Temp):
    plt.plot(Temp)
    plt.show()


def PlotDiffMatrix(Diff):
    plt.plot(Diff)
    plt.show()
