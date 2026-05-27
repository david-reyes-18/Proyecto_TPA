from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from escenas.escena_base import EscenaBase
from core.fuente import Fuente
 
if TYPE_CHECKING:
    from core.juego import Juego
 
 
class EscenaTaller(EscenaBase):
    def __init__(self, juego: Juego) -> None:
        super().__init__(juego)
        self.fuente_titulo = Fuente.obtener(36)
        self.fuente_info   = Fuente.obtener(20)
 
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    from escenas.escena_juego import EscenaJuego
                    self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))
 
    def actualizar(self, dt: float):
        pass
 
    def dibujar(self, pantalla: pygame.Surface):
        pantalla.fill((30, 18, 10))
 
        # Título
        surf_titulo = self.fuente_titulo.render("🔧  TALLER", False, (255, 180, 60))
        pantalla.blit(surf_titulo, surf_titulo.get_rect(centerx=pantalla.get_width()//2, y=80))
 
        # Contenido placeholder
        lineas = [
            "Aquí irá el desafío del Taller.",
            "",
            "[ ESC ] → volver al mapa",
        ]
        for i, linea in enumerate(lineas):
            surf = self.fuente_info.render(linea, False, (255, 220, 160))
            pantalla.blit(surf, (pantalla.get_width()//2 - surf.get_width()//2, 200 + i * 40))