from enum import Enum

"""
Clase que enumera los tipos de interfaz de un SSD
"""

class InterfazSSD(Enum):
    SATA = "SATA"
    M2_NVME = "M.2 NVMe"
    M2_SATA = "M.2 SATA"