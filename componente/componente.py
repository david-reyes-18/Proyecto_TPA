from abc import ABC, abstractmethod

class Componente(ABC):
    def __init__(self, nombre: str, esta_funcionando: bool = True):
        self._nombre = nombre
        self._esta_funcionando = esta_funcionando
    
    @abstractmethod
    def reparar(self):
        pass
    
    @abstractmethod
    def reemplazar(self):
        pass