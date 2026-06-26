from abc import ABC, abstractmethod
import random
from dominio.entidades.problemas.problema import Problema
from dominio.entidades.desafios.componente_tematico import ComponenteTematico


class RepositorioProblemas(ABC):
    """Contrato para acceder a problemas de reparación."""

    @abstractmethod
    def obtener_todos(self) -> list[Problema]:
        """Devuelve todos los problemas disponibles."""

    @abstractmethod
    def obtener_por_nivel(self, nivel: int) -> Problema | None:
        """
        Devuelve el problema asociado a un nivel concreto.
        Retorna None si el nivel no existe.
        """

    @abstractmethod
    def obtener_por_componente(self, componente: ComponenteTematico) -> list[Problema]:
        """Devuelve los problemas cuyo componente afectado coincide con el dado."""

    def obtener_aleatorio(self) -> Problema | None:
        """Devuelve un problema al azar del catálogo completo."""
        todos = self.obtener_todos()
        return random.choice(todos) if todos else None

    def obtener_aleatorio_por_componente(
        self, 
        componente: ComponenteTematico
    ) -> Problema | None:
        
        """Devuelve un problema al azar filtrado por componente."""
        filtrados = self.obtener_por_componente(componente)
        return random.choice(filtrados) if filtrados else None