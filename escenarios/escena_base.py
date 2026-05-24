import pygame
from abc import ABC, abstractmethod

class EscenaBase(ABC):
    def __init__(self, gestor_juego) -> None:
        self.gestor_juego = gestor_juego
    
    @abstractmethod
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        pass
    
    @abstractmethod
    def actualizar(self, teclas) -> None:
        pass
    
    @abstractmethod
    def dibujar(self, pantalla: pygame.Surface) -> None:
        pass