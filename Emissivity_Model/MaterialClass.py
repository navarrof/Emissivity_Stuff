import sys
import os
import numpy as np

class Material: 
    def __init__(self,MaterialFileName):
        h = open(MaterialFileName)
        d_MatInfo = {}
        cont = 0
        for l in h:
            if cont == 0:
                cont += 1
                continue
            else:
                if len(l.split()) == 0:
                    print("Error: There are blank spaces in Material Properties file.")
                d_MatInfo.update({l.split()[0] : l.split()[1]})

        self.name = d_MatInfo["Name:"]
        self.mpoint = float(d_MatInfo["MeltingPoint:"])             # [K]
        self.rho = float(d_MatInfo["Density:"])                     # [g/cm3] Density
        self.Z = float(d_MatInfo["Z:"])                             # Atomic Number
        self.Am = float(d_MatInfo["Am:"])                           # Atomic Mass
        self.wfun = float(d_MatInfo["WorkFunction:"])               # [eV] Work function
        self.eps = float(d_MatInfo["Emissivity:"])                  # [] Emissivity
        
        self.Resist = float(d_MatInfo["Resistivity:"])              # [10^-8 Ohm m] Resistivity

        # ---------------------- Specific Heat ------------------------ #
        CpInput = d_MatInfo["SpecificHeat:"]
        self.D_Cp = {"Temperature": [], "Parameter": []}
        try:
            cpT = float(CpInput)
            self.D_Cp["Temperature"] += [300.0]; self.D_Cp["Parameter"] += [cpT]

        except ValueError:
            pathtocp = os.getcwd()+"/MaterialFolder/ParametersWithTemperature/"+CpInput+".txt"
            f_cp = open(pathtocp,"r")
            for j,l in enumerate(f_cp,0):
                if j > 3:
                    self.D_Cp["Temperature"] += [float(l.split()[0])]
                    self.D_Cp["Parameter"] += [float(l.split()[1])]
            f_cp.close()

        self.Cp = self.GetCp(np.array([[300]]))            # [J/gK] Specific Heat

        # ---------------------- Conductivity ------------------------- #
        Kinput = d_MatInfo["Conductivity:"]
        self.D_k = {"Temperature":[], "Parameter": []}
        try: 
            kT = float(Kinput)
            self.D_k["Temperature"] += [300.0]; self.D_k["Parameter"] += [kT]

        except ValueError: 
            pathtok = os.getcwd()+"/MaterialFolder/ParametersWithTemperature/"+Kinput+".txt"
            f_k = open(pathtok,"r")
            for j,l in enumerate(f_k,0):
                if j > 3:
                    self.D_k["Temperature"] += [float(l.split()[0])]
                    self.D_k["Parameter"] += [float(l.split()[1])]
            f_k.close()

        self.con = self.Getk(np.array([300]))             # [W/mK] Conductivity
        
    def GetParameterValue(self,D_Par,T):
        # All the parameter search follows the same logic.                         #
        # ------------------------------------------------------------------------ #
        # If there is only one value, the parameter will be considered constant.   #
        # Otherwise, we will do a linear extrapolation of the parameter values.    #
        #       par(T<300) = par(T=300)                                            #
        #                                                                          #
        #       par(T) = a*T + b    Where a and b are calculated with the values   #
        #       of the parameter  and temperature that are the upper and lower     #
        #       values of T.                                                       #
        #                                                                          #
        #       par(T) with T > par["Temperature"][-1]. We calculate T as an       #
        #       extrapolation of the last two available values.                    #
        # ------------------------------------------------------------------------ #

   
        if len(D_Par["Temperature"]) == 1:
            Parameter = D_Par["Parameter"][0]
        else:
            for k in range(0,len(D_Par["Temperature"])):
          
                if (T <= D_Par["Temperature"][k]) and (k == 0):
                    Parameter = D_Par["Parameter"][0]

                    break

                elif (T <= D_Par["Temperature"][k]) and (T < D_Par["Temperature"][-1]):

                    a = (D_Par["Parameter"][k]-D_Par["Parameter"][k-1])/(D_Par["Temperature"][k]-D_Par["Temperature"][k-1])
                    b = D_Par["Parameter"][k]-a*D_Par["Temperature"][k]
                    Parameter = a*T + b
                    
                    break

                elif (T > D_Par["Temperature"][-1] ):

                    a = (D_Par["Parameter"][-1]-D_Par["Parameter"][-2])/(D_Par["Temperature"][-1]-D_Par["Temperature"][-2])
                    b = D_Par["Parameter"][-1]-a*D_Par["Temperature"][-1]
                    Parameter = a*T + b

                    break
        
        return Parameter

    def Getk(self, Temp):
        KK = Temp**0
        for i in range(0,len(KK)):
            if Temp[i] > self.D_k["Temperature"][-1]:
                KK[i] = self.D_k["Parameter"][-1]
            else:
                KK[i] = self.GetParameterValue(self.D_k,Temp[i])
        return KK
    
    def GetCp(self,Temp):
        Cp = Temp**0
        for i in range(0,len(Cp)):
            Cp[i] = self.GetParameterValue(self.D_Cp,Temp[i])
        return Cp