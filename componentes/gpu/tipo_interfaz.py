from enum import Enum

class InterfazGPU(Enum):
    PCIE = "PCIe" # PC de escritorio: tarjeta dedicada en slot PCIe x16
    MXM = "MXM" # Laptop: módulo dedicado MXM (No reemplazable)
    SOLDADA = "Soldada" # Laptop gama alta: GPU soldada a la placa (no reemplazable)
    INTEGRADA = "Integrada" # iGPU: comparte die con CPU (no reemplazable)