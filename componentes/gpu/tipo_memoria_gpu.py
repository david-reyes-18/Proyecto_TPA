from enum import Enum

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
    HBM2 = "HBM2"
    HBM3 = "HBM3"