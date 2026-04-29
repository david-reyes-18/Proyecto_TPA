from abc import ABC, abstractmethod

class Componente(ABC):
    def __init__(self, nombre: str, es_reemplazable: bool, es_reparable: bool):
        self._nombre = nombre
        self._es_reemplazable = es_reemplazable
        self._reparable = es_reparable
        self._esta_funcionando = True
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def es_reemplazable(self) -> bool:
        return self._es_reemplazable
    
    @property
    def es_reparable(self) -> bool:
        return self._reparable
    
    @property
    def esta_funcionando(self) -> bool:
        return self._esta_funcionando
    
    @abstractmethod
    def reparar(self):
        pass
    
    @abstractmethod
    def reemplazar(self):
        pass
    
    @abstractmethod
    def diagnosticar(self) -> str:
        pass