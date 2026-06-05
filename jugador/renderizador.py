import pygame
from core.config import *
from jugador.direcciones import Direcciones
from core.cargador_sprites import CargadorSprites


class Renderizador:
    """
    Maneja el renderizado del jugador, dibuja al jugador en pantalla.
    """
    
    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        
        # Delegamos la carga de sprites al CargadorSprites
        cargador_sprites = CargadorSprites(ancho, alto)
        self.sprites_jugador_estatico = cargador_sprites.cargar_sprites_estatico(
            "jugador/jugador_estatico.png", FRAMES_ESTATICO
        )
        self.sprites_jugador_corriendo = cargador_sprites.cargar_sprites_corriendo(
            "jugador/jugador_corriendo.png", DIRECCIONES, FRAMES_POR_DIRECCION
        )
        
        # Estado de animación
        self.indice_estatico = 0
        self.indice_corriendo = 0
        self.t_run = 0.0

    def _escalar(self, superficie: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(
            superficie,
            (self.ancho, self.alto)
        )

    def actualizar_animacion(
        self,
        dt: float,
        direccion: str,
        moviendose: bool
    ):
        """
        Actualiza el estado de la animación basado en la dirección y movimiento.
        Debe llamarse cada frame.
        """
        # Actualizar índice de sprite estático basado en dirección
        if direccion == Direcciones.IZQUIERDA:
            self.indice_estatico = 2
        elif direccion == Direcciones.DERECHA:
            self.indice_estatico = 0
        elif direccion == Direcciones.ARRIBA:
            self.indice_estatico = 1
        elif direccion == Direcciones.ABAJO:
            self.indice_estatico = 3

        # Actualizar animación de carrera
        if moviendose:
            self.t_run += dt
            if self.t_run >= 1 / FPS_CORRIENDO:
                self.t_run = 0
                self.indice_corriendo = (
                    self.indice_corriendo + 1
                ) % FRAMES_POR_DIRECCION
        else:
            self.indice_corriendo = 0
            self.t_run = 0

    def dibujar(
        self,
        pantalla: pygame.Surface,
        rect: pygame.Rect,
        camara: pygame.Rect,
        direccion: str,
        moviendose: bool
    ):
        """
        Dibuja al jugador en la pantalla.
        """
        if moviendose:
            frame = self.sprites_jugador_corriendo[
                direccion
            ][self.indice_corriendo]
        else:
            frame = self.sprites_jugador_estatico[
                self.indice_estatico
            ]

        pantalla.blit(
            frame,
            (
                rect.x - camara.x,
                rect.y - camara.y
            )
        )