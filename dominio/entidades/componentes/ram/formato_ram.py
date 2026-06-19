from enum import Enum


class FormatoRAM(Enum):
    
    """
    Clase que enumera los formatos que puede tener una RAM
    """
    
    # PC de escritorio
    DIMM = "DIMM" 
    
    # Laptops
    SO_DIMM = "SO-DIMM"
    
    # Laptops: soldada en placa (laptops ultradelgadas)
    LPDDR = "LPDDR" 