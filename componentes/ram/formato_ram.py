from enum import Enum

class FormatoRAM(Enum):
    DIMM = "DIMM" # PC de escritorio
    SO_DIMM = "SO-DIMM" # Laptops
    LPDDR = "LPDDR" # Laptops: soldada en placa (laptops ultradelgadas)