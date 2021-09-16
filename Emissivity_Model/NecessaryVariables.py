import MaterialClass as mc
import numpy as np

# 
Intensity = 0.4484                  # [A]
Voltage = 1.2732                    # [V]

Expected_Temp = 538                 # [K]

R = Voltage/Intensity

# --------------------------- Wire Properties --------------- #
Wire_Lenght = 5.0e-2                            # [m]
Wire_Diameter = 0.2e-3                          # [m]
Wire_N = 100                                    # [Number Wire Partitions]
Wire_dx = Wire_Lenght/Wire_N
Wire_CrossSec = np.pi*(Wire_Diameter/2.0)**2
# ------------------------------------------------------------ #

# ------------------ Simulation Properties ----------------- #
Min_Ems = 0.0; Max_Ems = 1.0

T0 = 300                         # [K]

dt = 1e-2                        # [s]
Ntime = 50000                     # Number of time steps
SSerror = 1e-3                      # Average of Diff(T_before - T_After). For knowing if SS reached.  

NEms = 10                        # Number Steps Emisiviti calculation. 
Emserror = 1e-3                  # Error For emissivity Calculation.

Tleft = 400                      # [K] Temperature Left side
Tright = 400                     # [K] Temperature Right Side

Material = mc.Material("MaterialFolder/Tungsten.txt")
# ------------------------------------------------------------ #




# ------------------------ Constants ------------------------- #  
ST = 5.6704E-8 		                # [J/s m2 K4] Stefan-Bolthman
# ------------------------------------------------------------ #