import pygame
from ui.widget import Widget
from core.fuente import Fuente
from core.manejador_sonidos import ManejadorSonidos
from typing import Callable


class Boton(Widget):
    
    """
    Permite crear un botón precionable, el cual puede llamar
    a una función, donde sus parámetros son:
    
    - text: texto que tendrá el botón por dentro
    - rel_x: posición relativa en x, donde x ∈ [0, 1].
    - rel_y: posición relativa en y, donde y ∈ [0, 1].
    - width: ancho del botón, dependiendo si es int o float puede ser absoluto o relativo.
    - height: alto del botón, dependiendo si es int o float puede ser absoluto o relativo.
    - command: función que se llamará al presionar el botón.
    - font_size: tamaño de la letra.
    - bg_color: color del fondo del botón.
    - hover_color: color del fondo del botón al tener el mouse por encima.
    - text_color: color del texto.
    - text_hover_color: color del texto si el mouse se encuentra seleccionando el botón
    - border_width: ancho del borde del botón.
    - border_color: color del borde del botón.
    - border_hover_color: color del borde del botón cuando el mouse está encima
    - border_radius: indica que tan circular tiene las esquinas del botón.
    - anchor: punto de referencia de cada widget que se va a alinear.
    """
    
    def __init__(
        self,
        text: str,
        rel_x: float,
        rel_y: float,
        width: int | float,
        height: int | float,
        command: Callable,
        font_size: int = 24,
        bg_color: tuple = (50, 50, 50),
        hover_color: tuple = (90, 90, 90),
        text_color: tuple = (255, 255, 255),
        text_hover_color: tuple = (220, 220, 220),
        border_width: int = 3,
        border_color: tuple = (200, 200, 200),
        border_hover_color: tuple = (255, 255, 255),
        border_radius: int = 8,
        anchor: str = "center"
    ) -> None:
        
        super().__init__(rel_x, rel_y, anchor)
        
        self.text = text
        self.width = width
        self.height = height
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text_hover_color = text_hover_color
        self.border_width = border_width
        self.border_color = border_color
        self.border_hover_color = border_hover_color
        self.border_radius = border_radius
        self.font = Fuente.obtener(font_size)
        self.hovered = False
        self.rect = pygame.Rect(0, 0, width, height)
    
    
    def _calcular_width(self, superficie: pygame.Surface) -> int:
        
        """
        Calcula en ancho del botón dependiendo si es
        un float o un int, si es un float significa que
        es un ancho relativo a la superficie, sino es
        un ancho fijo.
        """
        
        if isinstance(self.width, float):
            return int(superficie.get_width() * self.width)
        return self.width
    
    def _calcular_height(self, superficie: pygame.Surface) -> int:
        
        """
        Calcula la altura del botón dependiendo si es
        un float o un int, si es un float significa que
        es una altura relativa a la superficie, sino es
        una altura fija.
        """
        
        if isinstance(self.height, float):
            return int(superficie.get_width() * self.height)
        return self.height
    
    def actualizar(self, eventos: list[pygame.event.Event], superficie: pygame.Surface) -> None:
        
        """Actualiza el botón y revisa los eventos que le ocurren"""
        
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
        
        """Dibuja el botón en la superficie"""
        
        # Color de fondo del botón
        color = self.hover_color if self.hovered else self.bg_color
        
        # Color del texto del botón
        text_color = self.text_hover_color if self.hovered else self.text_color
        
        # Color del borde del botón
        border_color = self.border_hover_color if  self.hovered else self.border_color
        
        # Dibujar el fondo del botón (Relleno completo)
        pygame.draw.rect(
            superficie,
            color,
            self.rect,
            border_radius=self.border_radius
        )
        
        # Dibujar el borde
        if self.border_width > 0:
            pygame.draw.rect(
                superficie,
                border_color,
                self.rect,
                width=self.border_width,
                border_radius=self.border_radius
            )
        
        # Dibujar el texto encima de todo
        texto_superficie = self.font.render(
            self.text,
            False,
            text_color
        )
        texto_rect = texto_superficie.get_rect(
            center=self.rect.center
        )
        superficie.blit(
            texto_superficie,
            texto_rect
        )