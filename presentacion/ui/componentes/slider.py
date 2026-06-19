import pygame
from presentacion.ui.widget import Widget
from infraestructura.texto.fuente import Fuente
from typing import Callable


class Slider(Widget):
    
    """
    Clase que crea un slider de forma horizontal, donde sus parámetros
    son:
    
    text: texto que aparece a la izquierda de la barra.
    rel_x: posición relativa X del centro (0.0 – 1.0).
    rel_y: posición relativa Y del centro (0.0 – 1.0).
    width: ancho de la barra en píxeles.
    heigth: altura de la barra en píxeles.
    valor_inicial: valor de arranque (0.0 – 1.0).
    color_fill: color RGB de la parte rellena.
    color_unfill: color RGB de la parte que no esta rellena.
    command: callback opcional que recibe el nuevo valor (float).
    font_size: tamaño de la letra.
    text_color: color del texto
    knob_color: color del indicador 
    knob_border_color: color del borde del indicador
    """

    def __init__(
        self,
        text: str,
        rel_x: float,
        rel_y: float,
        width: int = 320,
        heigth: int = 12,
        valor_inicial: float = 0.5,
        color_fill: tuple = (100, 180, 255),
        color_unfill: tuple = (50, 50, 70),
        command: Callable[[float], None] | None = None,
        font_size: int = 18,
        text_color: tuple = (200, 200, 220),
        knob_color: tuple = (100, 180, 255),
        knob_border_color: tuple = (255, 255, 255)
    ):
        super().__init__(rel_x, rel_y, anchor="center")
        
        self.text = text
        self.width = width
        self.heigth = heigth
        self.valor = max(0.0, min(1.0, valor_inicial)) # Evita valores fuera del intervalo [0, 1]
        self.color_fill = color_fill
        self.color_unfill = color_unfill
        self.command = command
        self.font = Fuente.obtener(font_size)
        self.text_color = text_color
        self.knob_color = knob_color
        self.knob_border_color = knob_border_color
        
        # Radio del botón circular
        self.knob_radious = 10
        
        self._arrastrando = False
        
        # Rect de la pista, se recalcula en actualizar()
        self._barra_rect = pygame.Rect(0, 0, width, heigth)
    
    #   Métodos
    
    
    def _calcular_barra(self, superficie: pygame.Surface) -> pygame.Rect:
        
        """Devuelve el Rect de la pista centrado en la posición relativa."""
        
        pos_x, pos_y = self.obtener_posicion(superficie)
        return pygame.Rect(
            int(pos_x) - self.width // 2,
            int(pos_y) - self.heigth // 2,
            self.width,
            self.heigth,
        )
    
    def _valor_desde_x(self, mouse_x: int) -> float:
        left = self._barra_rect.x
        return max(0.0, min(1.0, (mouse_x - left) / self.width))
    
    def _knob_x(self) -> int:
        return self._barra_rect.x + int(self.valor * self.width)
    
    def _knob_pos_y(self) -> int:
        return self._barra_rect.centery
    
    def set_valor(self, valor: float) -> None:
        self.valor = max(0.0, min(1.0, valor))
        
    def get_valor(self) -> float:        
        return self.valor
    
    def actualizar(self, eventos: list[pygame.event.Event], superficie: pygame.Surface) -> None:
        
        """Actualiza todo el widget mediante los eventos que ocurran, como
        lo son el deslizamiento del knob y su actualizacion en el valor"""
        
        self._barra_rect = self._calcular_barra(superficie)
        zona_click = self._barra_rect.inflate(0, 28)
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if zona_click.collidepoint(evento.pos):
                    self._arrastrando = True
                    self._actualizar_valor(evento.pos[0])
            
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self._arrastrando = False
            
            elif evento.type == pygame.MOUSEMOTION:
                if self._arrastrando:
                    self._actualizar_valor(evento.pos[0])
    
    def _actualizar_valor(self, mouse_x: int) -> None:
        
        """Actualiza el valor del slider"""
        
        nuevo = self._valor_desde_x(mouse_x)
        if nuevo != self.valor:
            self.valor = nuevo
            if self.command:
                self.command(self.valor)
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        
        """Se encargar de dibujar el slider"""
        
        barra = self._barra_rect
        pos_x = barra.centerx
        pos_y = barra.centery
        
        # Etiqueta (a la izquierda)
        superficie_label = self.font.render(self.text, False, self.text_color)
        superficie.blit(superficie_label, superficie_label.get_rect(midright=(barra.x - 14, pos_y)))
        
        # Pista (fondo)
        pygame.draw.rect(superficie, self.color_unfill, barra, border_radius=6)
        
        # Pista (relleno)
        fill = pygame.Rect(barra.x, barra.y, int(self.valor * self.width), self.heigth)
        if fill.width > 0:
            pygame.draw.rect(superficie, self.color_fill, fill, border_radius=6)
        
        # Knob
        knob_x = self._knob_x()
        
        # knob borde
        pygame.draw.circle(superficie, self.knob_border_color, (knob_x, pos_y), self.knob_radious)
        # knob relleno
        pygame.draw.circle(superficie, self.color_fill,  (knob_x, pos_y), self.knob_radious - 3)
        
        # Porcentaje (a la derecha)
        pct_surf = self.font.render(f"{int(self.valor * 100)}%", False, self.text_color)
        superficie.blit(pct_surf, pct_surf.get_rect(midleft=(barra.right + 14, pos_y)))