from enum import Enum

class InterfazGPU(Enum):
    PCIE = "PCIe"
    MXM = "MXM"
    SOLDADA = "Soldada"
    INTEGRADA = "Integrada"