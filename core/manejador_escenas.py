import pygame
from escenas.escena_base import EscenaBase


class ManejadorEscenas:
    
    """
    Clase que se encarga de manejar escenas y recibir toda la información del juego
    para posteriormente dibujar todo en pantalla
    """
    
    def __init__(self) -> None:
        self.escena_actual: None | EscenaBase = None
        self.escena_anterior: None | EscenaBase = None
    
    # Cambio de escena a una nueva
    def cambiar_escena(self, nueva_escena: EscenaBase) -> None:
        self.escena_anterior = self.escena_actual
        self.escena_actual = nueva_escena
    
    # Recibe los eventos del usuario, como clicks o teclas del teclado
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        if self.escena_actual is not None:
            self.escena_actual.manejar_eventos(eventos)
    
    # Actualiza movimientos del jugador o sprites de todo tipo
    def actualizar(self, dt: float) -> None:
        if self.escena_actual is not None:
            self.escena_actual.actualizar(dt)
    
    # Toma la pantalla principal y dibuja en ella, ya sea botones, texto o personajes
    def dibujar(self, pantalla: pygame.Surface) -> None:
        if self.escena_actual is not None:
            self.escena_actual.dibujar(pantalla)