from enum import Enum

"""
Clase que enumera los formatos que puede tener una RAM
"""

class FormatoRAM(Enum):
    DIMM = "DIMM" # PC de escritorio
    SO_DIMM = "SO-DIMM" # Laptops
    LPDDR = "LPDDR" # Laptops: soldada en placa (laptops ultradelgadas)