import pygame
from escenas.escena_base import EscenaBase

class ManejadorEscenas:
    def __init__(self):
        self.escena_actual: None | EscenaBase = None
    
    def cambiar_escena(self, nueva_escena: EscenaBase) -> None:
        self.escena_actual = nueva_escena
    
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        if self.escena_actual is not None:
            self.escena_actual.manejar_eventos(eventos)
    
    def actualizar(self, dt: float) -> None:
        if self.escena_actual is not None:
            self.escena_actual.actualizar(dt)
    
    def dibujar(self, pantalla: pygame.Surface) -> None:
        if self.escena_actual is not None:
            self.escena_actual.dibujar(pantalla)