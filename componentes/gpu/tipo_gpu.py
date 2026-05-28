from enum import Enum


class TipoGPU(Enum):
    
    """
    Clase que enumera los tipos de GPU que hay
    """
    
    INTEGRADA = "Integrada"
    DEDICADA = "Dedicada"