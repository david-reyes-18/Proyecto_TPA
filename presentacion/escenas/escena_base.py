from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from presentacion.juego import Juego


class EscenaBase(ABC):
    
    """
    Interfaz que todas las escenas del juego tendrán que seguir
    """
    
    def __init__(self, juego: Juego) -> None:
        self.juego = juego
    
    # Recibe los eventos del usuario, como clicks o teclas del teclado
    @abstractmethod
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        pass
    
    # Actualiza movimientos del jugador o sprites de todo tipo
    @abstractmethod
    def actualizar(self, dt: float) -> None:
        pass
    
    # Toma la pantalla principal y dibuja en ella, ya sea botones, texto o personajes
    @abstractmethod
    def dibujar(self, pantalla: pygame.Surface) -> None:
        pass