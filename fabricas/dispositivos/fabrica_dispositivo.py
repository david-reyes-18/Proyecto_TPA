from abc import ABC, abstractmethod
from problemas.problema import Problema
from dispositivos.dispositivo import Dispositivo

class FabricaDispositivo(ABC):
    
    @abstractmethod
    def crear_dispositivo_basico(self, problema: Problema) -> Dispositivo:
        pass
    
    @abstractmethod
    def crear_dispositivo_intermedio(self, problema: Problema) -> Dispositivo:
        pass
    
    @abstractmethod
    def crear_dispositivo_gamer(self, problema: Problema) -> Dispositivo:
        pass