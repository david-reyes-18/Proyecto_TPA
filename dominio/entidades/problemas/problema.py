from abc import ABC, abstractmethod
from dominio.entidades.componentes.base.componente import Componente
from dominio.entidades.problemas.paso_de_reparacion import PasoDeReparacion
from dominio.entidades.problemas.perfil_dispositivo import (
    PerfilDispositivo,
    inferir_perfil_desde_nombre,
)

class Problema(ABC):
    def __init__(
        self, 
        nombre: str, 
        descripcion_email: str, 
        componente_afectado: Componente, 
        pasos_reparacion: list[PasoDeReparacion],
        perfil_dispositivo: PerfilDispositivo | None = None,
    ):
        
        self._nombre = nombre
        self._descripcion_email = descripcion_email
        self._componente_afectado = componente_afectado
        self._pasos_de_reparacion = pasos_reparacion

        # Si el problema concreto no declara su perfil explícitamente,
        # se infiere a partir del nombre (compatibilidad con catálogos
        # que todavía no lo declaran de forma explícita).
        self._perfil_dispositivo = perfil_dispositivo or inferir_perfil_desde_nombre(nombre)

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

    @property
    def perfil_dispositivo(self) -> PerfilDispositivo:
        return self._perfil_dispositivo
    
    def reiniciar_pasos(self) -> None:
        """Reinicia todos los pasos para que puedan volver a responderse."""
        for paso in self._pasos_de_reparacion:
            paso._completado = False
        self._indice_actual = 0