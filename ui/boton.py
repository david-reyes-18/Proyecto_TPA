import pygame
from ui.widget import Widget
from core.fuente import Fuente
from core.manejador_sonidos import ManejadorSonidos


class Boton(Widget):
    def __init__(
        self,
        text: str,
        rel_x: float,
        rel_y: float,
        width: int | float,
        height: int | float,
        command,
        font_size=24,
        bg_color=(50, 50, 50),
        hover_color=(90, 90, 90),
        text_color=(255, 255, 255),
        anchor="center"
    ):
        super().__init__(rel_x, rel_y, anchor)
        
        self.text = text
        self.width = width
        self.height = height
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = Fuente.obtener(font_size)
        self.hovered = False
        self.rect = pygame.Rect(0, 0, width, height)
    
    
    def _calcular_width(self, superficie: pygame.Surface) -> int:
        if isinstance(self.width, float):
            return int(superficie.get_width() * self.width)
        return self.width
    
    def _calcular_height(self, superficie: pygame.Surface) -> int:
        if isinstance(self.height, float):
            return int(superficie.get_width() * self.height)
        return self.height
    
    def actualizar(self, eventos: list[pygame.event.Event], superficie: pygame.Surface) -> None:
        x, y = self.obtener_posicion(superficie)
        width = self._calcular_width(superficie)
        height = self._calcular_height(superficie)
        
        self.rect = pygame.Rect(
            0,
            0,
            width,
            height
        )
        self.rect = self.aplicar_anchor(self.rect, x, y)
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    ManejadorSonidos.reproducir("click.ogg")
                    self.command()

    def dibujar(self, superficie: pygame.Surface) -> None:
        color = (
            self.hover_color
            if self.hovered
            else self.bg_color
        )
        pygame.draw.rect(
            superficie,
            color,
            self.rect,
            border_radius=8
        )
        texto_superficie = self.font.render(
            self.text,
            False,
            self.text_color
        )
        texto_rect = texto_superficie.get_rect(
            center=self.rect.center
        )
        superficie.blit(
            texto_superficie,
            texto_rect
        )