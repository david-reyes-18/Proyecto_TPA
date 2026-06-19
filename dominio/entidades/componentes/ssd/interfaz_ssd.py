from enum import Enum


class InterfazSSD(Enum):
    
    """
    Clase que enumera los tipos de interfaz de un SSD
    """
    
    SATA = "SATA"
    M2_NVME = "M.2 NVMe"
    M2_SATA = "M.2 SATA"