from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from presentacion.ui.widget import Widget

if TYPE_CHECKING:
    from presentacion.ui.componentes.frame import Frame


class Frame(Widget):
    """
    Contenedor rectangular con posición y tamaño relativos a la superficie padre.
    Soporta widgets hijos cuyas coordenadas rel_x/rel_y son relativas al frame.
    Sus parámetros son:
    
    - rel_x: posición relativa en x, donde x ∈ [0, 1].
    - rel_y: posición relativa en y, donde y ∈ [0, 1].
    - width: ancho del botón, dependiendo si es int o float puede ser absoluto o relativo.
    - height: alto del botón, dependiendo si es int o float puede ser absoluto o relativo.
    - anchor: punto de referencia de cada widget que se va a alinear.
    - bg_color: color del fondo
    - alpha: transparencia 0-255
    - border_radius: esquinas redondeadas
    - border_color : color del borde
    - border_width: ancho del borde
    - clip_children   : bool       — si True recorta los hijos al área del frame
    - visible: visibilidad
    """
    
    def __init__(
        self,
        rel_x: float,
        rel_y: float,
        width: int | float,
        height: int | float,
        anchor: str = "topleft",
        bg_color: tuple = (30, 30, 30),
        alpha: int = 255,
        border_radius: int = 0,
        border_color: tuple | None = None,
        border_width: int = 2,
        clip_children: bool = False,
        visible: bool = True,
    ) -> None:
        
        super().__init__(rel_x, rel_y, anchor)
        
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        self.clip_children = clip_children
        self.visible = visible
        
        # Normalizar bg_color a RGBA
        if len(bg_color) == 3:
            self.bg_color = (*bg_color, alpha)
        else:
            self.bg_color = bg_color
        
        # Rect interno (calculado en cada dibujar)
        self.rect = pygame.Rect(0, 0, 0, 0)
        
        # Lista de widgets hijos
        self._hijos: list[Widget] = []
    
    def add(self, widget: Widget) -> Frame:
        """
        Agrega un widget hijo al frame.
        Los rel_x/rel_y del hijo son relativos al tamaño del frame.
        """
        self._hijos.append(widget)
        return self
    
    def remove(self, widget: Widget) -> None:
        """Elimina un widget hijo del frame."""
        if widget in self._hijos:
            self._hijos.remove(widget)
    
    def clear(self) -> None:
        """Elimina todos los widgets hijos."""
        self._hijos.clear()
    
    def _calcular_ancho(self, superficie: pygame.Surface) -> int:
        if isinstance(self.width, float):
            return int(superficie.get_width() * self.width)
        return int(self.width)
    
    def _calcular_alto(self, superficie: pygame.Surface) -> int:
        if isinstance(self.height, float):
            return int(superficie.get_height() * self.height)
        return int(self.height)
    
    
    def get_rect(self, superficie: pygame.Surface) -> pygame.Rect:
        """Devuelve el pygame.Rect actual del frame en coordenadas de la pantalla."""
        ancho = self._calcular_ancho(superficie)
        alto = self._calcular_alto(superficie)
        x, y = self.obtener_posicion(superficie)
        rect = pygame.Rect(0, 0, ancho, alto)
        return self.aplicar_anchor(rect, x, y)
    
    def set_alpha(self, alpha: int) -> None:
        """Cambia la transparencia del fondo (0-255)."""
        r, g, b, _ = self.bg_color
        self.bg_color = (r, g, b, max(0, min(255, alpha)))
    
    def set_color(self, color: tuple) -> None:
        """Cambia el color de fondo conservando el alpha actual."""
        _, _, _, a = self.bg_color
        if len(color) == 3:
            self.bg_color = (*color, a)
        else:
            self.bg_color = color
    
    def actualizar(self, eventos, superficie: pygame.Surface | None = None) -> None:
        """Propaga eventos a los hijos que tengan método actualizar con superficie."""
        if not self.visible or superficie is None:
            return
        
        ancho = self._calcular_ancho(superficie)
        alto = self._calcular_alto(superficie)
        surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        
        for hijo in self._hijos:
            hijo.actualizar(eventos, surface)
    
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        if not self.visible:
            return
        
        ancho = self._calcular_ancho(superficie)
        alto = self._calcular_alto(superficie)
        x, y = self.obtener_posicion(superficie)
        
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect = self.aplicar_anchor(self.rect, x, y)
        
        alpha = self.bg_color[3]
        
        # Dibujar fondo del frame
        if alpha == 255:
            pygame.draw.rect(
                superficie,
                self.bg_color[:3],
                self.rect,
                border_radius=self.border_radius,
            )
        else:
            fondo_surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            pygame.draw.rect(
                fondo_surf,
                self.bg_color,
                fondo_surf.get_rect(),
                border_radius=self.border_radius,
            )
            superficie.blit(fondo_surf, self.rect.topleft)

        # Dibujar hijos
        if self._hijos:
            
            superficie_hijos = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            
            for hijo in self._hijos:
                hijo.dibujar(superficie_hijos)
            
            # Si está activo clip_children entonces si los widgets sobresalen tienen que ser recortados
            if self.clip_children:
                
                mask_surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
                pygame.draw.rect(
                    mask_surf,
                    (255, 255, 255, 255),
                    mask_surf.get_rect(),
                    border_radius=self.border_radius,
                )
                superficie_hijos.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            
            superficie.blit(superficie_hijos, self.rect.topleft)
        
        # Borde (encima de todo)
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(
                superficie,
                self.border_color,
                self.rect,
                width=self.border_width,
                border_radius=self.border_radius,
            )