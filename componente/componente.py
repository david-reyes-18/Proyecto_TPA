from abc import ABC, abstractmethod

class Componente(ABC):
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._esta_funcionando = True
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def esta_funcionando(self) -> bool:
        return self._esta_funcionando
    
    def reparar(self):
        self._esta_funcionando = True
    
    @abstractmethod
    def diagnosticar(self) -> str:
        pass