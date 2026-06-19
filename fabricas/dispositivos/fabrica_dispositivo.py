import random
from abc import ABC, abstractmethod
from dominio.entidades.problemas.problema import Problema
from dominio.entidades.dispositivos.dispositivo import Dispositivo
from fabricas.dispositivos.catalogo_componentes import DatosPlacaBase, DatosCPU, DatosGPU
from dominio.entidades.componentes.cpu.cpu import CPU
from dominio.entidades.componentes.gpu.gpu import GPU

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