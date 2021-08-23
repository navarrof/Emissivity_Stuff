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
        self.Cp = float(d_MatInfo["SpecificHeat:"])                 # [J/gK] Specific Heat
        self.con = float(d_MatInfo["Conductivity:"])                # [W/mK] Conductivity
        self.Resist = float(d_MatInfo["Resistivity:"])              # [10^-8 Ohm m] Resistivity
        