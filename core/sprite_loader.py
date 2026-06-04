"""
Utilidad de carga de sprites para el juego.
Maneja la carga y escalado de hojas de sprites para entidades.
"""


import pygame
from core.rutas import Rutas
from core.config import *


class CargadorSprites:
    """
    Responsable de cargar hojas de sprites y convertirlos en listas/diccionarios
    de superficies pygame utilizables. Mantiene separadas las preocupaciones
    de carga de activos y renderizado.
    """

    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto

    def _escalar(self, superficie: pygame.Surface) -> pygame.Surface:
        """Escala una superficie a las dimensiones de la entidad."""
        return pygame.transform.scale(superficie, (self.ancho, self.alto))

    def cargar_sprites_estatico(self, ruta_relativa: str, frames: int) -> list[pygame.Surface]:
        """
        Carga una hoja de sprites horizontal para animación estática.

        Args:
            ruta_relativa: Ruta relativa a assets/images/ (ej. "jugador/jugador_estatico.png")
            frames: Número de frames en la hoja

        Returns:
            Lista de objetos pygame.Surface escalados, uno por frame.
        """
        spritesheet = pygame.image.load(
            str(Rutas.imagen(ruta_relativa))
        ).convert_alpha()

        frames_lista = []
        for i in range(frames):
            frame = spritesheet.subsurface(
                (i * FRAME_ANCHO, 0, FRAME_ANCHO, FRAME_ALTO)
            )
            frames_lista.append(self._escalar(frame))
        return frames_lista

    def cargar_sprites_corriendo(self, ruta_relativa: str, direcciones: list[str], frames_por_direccion: int) -> dict[str, list[pygame.Surface]]:
        """
        Carga una hoja de sprites que contiene animaciones de carrera para múltiples direcciones.

        Espera que la hoja esté organizada como:
            [dir0_frame0, dir0_frame1, ..., dir0_frameN,
             dir1_frame0, dir1_frame1, ..., dir1_frameN,
             ...]

        Args:
            ruta_relativa: Ruta relativa a assets/images/
            direcciones: Lista de cadenas de dirección en el orden en que aparecen en la hoja
            frames_por_direccion: Número de frames por dirección

        Returns:
            Diccionario que asigna nombre de dirección -> lista de frames para esa dirección.
        """
        spritesheet = pygame.image.load(
            str(Rutas.imagen(ruta_relativa))
        ).convert_alpha()

        animaciones: dict[str, list[pygame.Surface]] = {}
        for indice_direccion, direccion in enumerate(direcciones):
            frames = []
            for i in range(frames_por_direccion):
                frame_index = indice_direccion * frames_por_direccion + i
                frame = spritesheet.subsurface(
                    (
                        frame_index * FRAME_ANCHO,
                        0,
                        FRAME_ANCHO,
                        FRAME_ALTO
                    )
                )
                frames.append(self._escalar(frame))
            animaciones[direccion] = frames
        return animaciones