import numpy as np
import sys
from numpy.linalg import inv
from numpy.core.arrayprint import dtype_is_implied
import NecessaryVariables as nv
import matplotlib.pyplot as plt

def CreateWire(Wire_Lenght, Wire_Diameter, Wire_N):
    Wire_X = []; 
    for k in range(0,Wire_N):
        xpos = -Wire_Lenght/2 + k*nv.Wire_dx
        Wire_X += [xpos]

    Wire_X = np.array(Wire_X)
    return Wire_X


def JuleHeating(dt,dx,Temp):
    V = nv.Wire_CrossSec*nv.Wire_Lenght
    dtemp = nv.Intensity**2 * nv.R / ( nv.Material.Cp*nv.Material.rho*V*1e6 ) 
    
    return dtemp * dt * Temp ** 0

def RadiationCooling(dt,dx,Temp):
    dV = nv.Wire_CrossSec*dx
    dS = np.pi*nv.Wire_Diameter*dx
    T0vec = nv.T0*Temp**0.0

    dene = dS * nv.Material.eps * nv.ST * ( Temp**4 - T0vec**4 ) *dt
    dtemp = - dene/( nv.Material.Cp*nv.Material.rho*dV*1e6 )

    return dtemp 


def ConductionCooling_FTCS(dt,dx, X_vec,Temp):

    dtemp = Temp**0.0

    alpha = nv.Material.con/(nv.Material.rho*nv.Material.Cp*1000)
    r = alpha*dt/dx**2.0

    if r > 1/2: print("Careful! Conduction Cooling might bring problems. Reduce dt or increase dx."); print(r); sys.exit()
    

    for j in range(0,len(X_vec)):
        Tj = Temp[j]
        if j == 0:
            Tjp1 = Temp[j+1]; Tjm1 = nv.Tleft
        elif j == len(X_vec)-1:
            Tjp1 = nv.Tright; Tjm1 = Temp[j-1]
        else:
            Tjp1 = Temp[j+1]; Tjm1 = Temp[j-1]

        dtemp[j] = alpha[j]*(Tjm1-2*Tj+Tjp1)/dx**2

    return dtemp * dt

def ConductionCooling_CrankNick(dt,dx, X_vec,Temp):

    alpha = nv.Material.con/(nv.Material.rho*nv.Material.Cp*1e+6)   # [m2/s]
    r = alpha*dt/(2.0*dx**2)
    A = np.array([]); D = np.array([])

    for j in range(0,len(X_vec)):
        if j == 0:
            b0 = 1; c0 = 0.0; d0 = nv.Tleft
            D = np.append(D,d0)
            
            v1 = np.array([b0,c0]); v2 = np.zeros(len(Temp)-len(v1))
            v = np.append(v1,v2)
            A = np.append(A,[v])
            

        elif j == len(X_vec)-1:
            an = 0; bn = 1; dn = nv.Tright

            D = np.append(D,dn)
            
            v2 = np.array([an,bn]); v1 = np.zeros(len(Temp)-len(v2))
            v = np.append(v1,v2)
            A = np.append(A,[v],axis=0)
        
        else: 
            aj = -r[j]; bj = (1+2*r[j]); cj = -r[j]
            dj = r[j]*Temp[j-1]+(1-2*r[j])*Temp[j]+r[j]*Temp[j+1]

            D = np.append(D,dj)
  
            v1 = np.zeros(j-1); v2 = np.array([aj,bj,cj]); v3 = np.zeros(len(Temp)-len(v1)-len(v2))
            v = np.concatenate((v1,v2,v3),axis=None)
            if j == 1:  A = np.append([A],[v],axis=0)
            else: A = np.append(A,[v],axis=0); 
            
    dtemp = np.subtract(np.dot(inv(A),D),Temp)    

    return dtemp


def TemperatureChange(dt,X_vec,Temp):
    
    dx = (X_vec[1]-X_vec[0])

    nv.Material.con = nv.Material.Getk(Temp)
    nv.Material.Cp = nv.Material.GetCp(Temp)

    heat = JuleHeating(dt,dx,Temp)
    cold1 = RadiationCooling(dt,dx,Temp)
    cold2 = ConductionCooling_CrankNick(dt,dx,X_vec,Temp)
    dtemp =  heat  + cold1 + cold2

    return dtemp

def PlotSteadyStateTemp(Temp):
    plt.plot(Temp)
    plt.show()


def PlotDiffMatrix(Diff):
    plt.plot(Diff)
    plt.show()


