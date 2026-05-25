import pygame
from ui.widget import Widget
from core.fuente import Fuente


class Label(Widget):
    def __init__(
        self,
        text: str,
        font_size: int,
        color: tuple,
        rel_x: float,
        rel_y: float,
        anchor: str = "topleft"
    ):
        super().__init__(rel_x, rel_y, anchor)
        
        self.text = text
        self.color = color
        self.fuente = Fuente.obtener(font_size)

    def dibujar(self, superficie: pygame.Surface) -> None:
        texto_superficie = self.fuente.render(
            self.text,
            False,
            self.color
        )
        rect = texto_superficie.get_rect()
        x, y = self.obtener_posicion(superficie)
        rect = self.aplicar_anchor(rect, x, y)
        superficie.blit(texto_superficie, rect)