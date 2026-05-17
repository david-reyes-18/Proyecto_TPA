from abc import ABC, abstractmethod
from componentes.componente import Componente
from problemas.paso_de_reparacion import PasoDeReparacion

class Problema(ABC):
    def __init__(
        self, 
        nombre: str, 
        descripcion_email: str, 
        componente_afectado: Componente, 
        pasos_reparacion: list[PasoDeReparacion],
    ):
        
        self._nombre = nombre
        self._descripcion_email = descripcion_email
        self._componente_afectado = componente_afectado
        self._pasos_de_reparacion = pasos_reparacion
        
        self._cantidad_pasos = len(self._pasos_de_reparacion)
        self._indice_actual = 0
    
    
    #   Propiedades
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def descripcion_email(self) -> str:
        return self._descripcion_email
    
    @property
    def componente_afectado(self) -> Componente:
        return self._componente_afectado
    
    @property
    def pasos_de_reparacion(self) -> list:
        return self._pasos_de_reparacion
    
    @property
    def cantidad_pasos(self) -> int:
        return self._cantidad_pasos
    
    @property
    def indice_actual(self) -> int:
        return self._indice_actual
    