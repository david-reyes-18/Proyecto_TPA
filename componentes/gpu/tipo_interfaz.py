from enum import Enum


class InterfazGPU(Enum):
    
    """
    Clase que enumera los tipos de interfaces de una GPU
    """
    
    # PC de escritorio: tarjeta dedicada en slot PCIe x16
    PCIE = "PCIe" 
    
    # Laptop: módulo dedicado MXM (No reemplazable)
    MXM = "MXM"
    
    # Laptop gama alta: GPU soldada a la placa (no reemplazable)
    SOLDADA = "Soldada"
    
    # iGPU: comparte die con CPU (no reemplazable)
    INTEGRADA = "Integrada"