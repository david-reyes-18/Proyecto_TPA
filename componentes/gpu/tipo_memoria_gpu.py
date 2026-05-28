from enum import Enum

"""
Clase que enumera los tipos de memoria que tiene la GPU
"""

class TipoMemoriaGPU(Enum):
    
    # Memoria compartida (iGPU)
    DDR4 = "DDR4"
    DDR5 = "DDR5"
    LPDDR4X = "LPDDR4X"
    LPDDR5 = "LPDDR5"
    
    # Memoria dedicada (dGPU)
    GDDR5 = "GDDR5"
    GDDR6 = "GDDR6"
    GDDR6X = "GDDR6X"
    GDDR7 = "GDDR7"
    HBM2 = "HBM2"
    HBM3 = "HBM3"