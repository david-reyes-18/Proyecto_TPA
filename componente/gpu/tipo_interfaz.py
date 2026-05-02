from enum import Enum

class InterfazGPU(Enum):
    PCIe = "PCIe"
    MXM = "MXM"
    SOLDADA = "Soldada"
    INTEGRADA = "Integrada"