import pygame

class Widget:
    def __init__(
        self,
        rel_x: float = 0.0,
        rel_y: float = 0.0,
        anchor: str = "topleft"
    ):
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.anchor = anchor
    
    def obtener_posicion(self, superficie: pygame.Surface) -> tuple:
        ancho = superficie.get_width()
        alto = superficie.get_height()
        x = ancho * self.rel_x
        y = alto * self.rel_y
        return x, y
    
    def aplicar_anchor(self, rect: pygame.Rect, x: float, y: float):
        setattr(rect, self.anchor, (x, y))
        return rect
    
    def actualizar(self, eventos):
        pass
    
    def dibujar(self, superficie: pygame.Surface):
        pass