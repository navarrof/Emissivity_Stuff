import MaterialClass as mc
import numpy as np

# ----- Constants ---- #  
BZ = 5.6704E-8 		    # [J/s m2 K4] Stefan-Bolthman constant for black-body radiation law
# --------------------- #

Intensity = 1.0714                  # [A]
Voltage = 2.5235                  # [V]

Wire_Lenght = 4e-2                        # [m]
Wire_Diameter = 0.2e-3                     # [m]
Wire_N = 1000                               # [Number Wire Partitions]
Wire_dx = Wire_Lenght/Wire_N
Wire_CrossSec = np.pi*(Wire_Diameter/2.0)**2

Min_Ems = 0.0; Max_Ems = 1.0

T0 = 300                         # [K]

dt = 1e-8                        # [s]
Ntime = 300000                     # Number of time steps
SSerror = 1e-5                  # Average of Diff(T_before - T_After). For knowing if SS reached.  

NEms = 10                        # Number Steps Emisiviti calculation. 
Emserror = 1e-3                  # Error For emissivity Calculation.

Tleft = 303                      # [K] Temperature Left side
Tright = 303                     # [K] Temperature Right Side

Material = mc.Material("MaterialFolder/Tungsten.txt")

R = Voltage/Intensity
