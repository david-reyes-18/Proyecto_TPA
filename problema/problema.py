from abc import ABC, abstractmethod

class Problema(ABC):
    def __init__(self, descripcion: str, pasos_de_reparacion: list):
        self._descripcion = descripcion
        self._pasos_de_reparacion = pasos_de_reparacion
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def pasos_de_reparacion(self) -> list:
        return self._pasos_de_reparacion