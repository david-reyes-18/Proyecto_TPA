from __future__ import annotations
from typing import TYPE_CHECKING, List
from dispositivos.laptop import Laptop

if TYPE_CHECKING:
    from core.juego import Juego


class Inventario:
    """
    Gestiona el inventario del jugador (laptops reparadas, componentes, etc.)
    """

    def __init__(self):
        self.laptops: List[Laptop] = [] # Laptops en proceso de reparación o completadas
        self.componentes: List = [] # Componentes que el usuario posee
        self.dinero: int = 0 # Dinero del jugador
        self.experiencia: int = 0 # Experiencia del jugador
        self.nivel: int = 1              # Nivel del jugador

    def agregar_laptop(self, laptop: Laptop):
        """Agrega una laptop al inventario"""
        self.laptops.append(laptop)

    def remover_laptop(self, indice: int) -> Laptop | None:
        """Remueve y retorna una laptop del inventario por índice"""
        if 0 <= indice < len(self.laptops):
            return self.laptops.pop(indice)
        return None

    def get_laptop(self, indice: int) -> Laptop | None:
        """Obtiene una laptop sin removerla"""
        if 0 <= indice < len(self.laptops):
            return self.laptops[indice]
        return None

    def agregar_dinero(self, cantidad: int):
        """Agrega dinero al jugador"""
        self.dinero += cantidad

    def agregar_experiencia(self, cantidad: int):
        """Agrega experiencia y sube de nivel si es necesario"""
        self.experiencia += cantidad
        # Cada 100 puntos de experiencia sube un nivel
        while self.experiencia >= self.nivel * 100:
            self.experiencia -= self.nivel * 100
            self.nivel += 1

    def get_estado(self) -> dict:
        """Retorna el estado actual del inventario para guardar/cargar"""
        return {
            "dinero": self.dinero,
            "experiencia": self.experiencia,
            "nivel": self.nivel,
            "laptops_count": len(self.laptops)
        }

    def cargar_estado(self, estado: dict):
        """Carga el estado del inventario"""
        self.dinero = estado.get("dinero", 0)
        self.experiencia = estado.get("experiencia", 0)
        self.nivel = estado.get("nivel", 1)
        # Las laptops se gestionan por separado según el juego


class JugadorConInventario:
    """
    Extiende al jugador con capacidades de inventario
    En una implementación completa, esto se integraría con la clase Jugador existente
    """

    def __init__(self):
        self.inventario = Inventario()

    def aceptar_trabajo(self, trabajo) -> bool:
        """
        Intenta aceptar un trabajo y agregar la laptop al inventario
        Returns: True si se aceptó exitosamente
        """
        # Esto requeriría acceso al objeto juego para crear la laptop
        # Por ahora retornamos False como placeholder
        # La implementación real se haría desde la escena de correo
        return False