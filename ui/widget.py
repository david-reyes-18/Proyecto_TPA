import pygame
from abc import ABC, abstractmethod

class Widget(ABC):
    
    """
    Clase abstracta que permite crear nuevas subclases, donde
    sus parámetros son:
    
    rel_x: posición relativa en x, donde x ∈ [0, 1].
    rel_y: posición relativa en y, donde y ∈ [0, 1].
    anchor: punto de referencia de cada widget que se va a alinear.
    """
    
    def __init__(
        self,
        rel_x: float = 0.0,
        rel_y: float = 0.0,
        anchor: str = "topleft"
    ) -> None:
        
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.anchor = anchor
    
    #   Métodos
    
    def obtener_posicion(self, superficie: pygame.Surface) -> tuple:
        
        """
        Obtiene la posición actual del widget 
        en relación a una superficie.
        """
        
        ancho = superficie.get_width()
        alto = superficie.get_height()
        x = ancho * self.rel_x
        y = alto * self.rel_y
        
        return x, y
    
    def aplicar_anchor(self, rect: pygame.Rect, x: float, y: float) -> pygame.Rect:
        
        """Alinea el Rect utilizando el 'anchor' definido convertido a enteros."""
        
        setattr(rect, self.anchor, (x, y))
        return rect
    
    @abstractmethod
    def actualizar(self, eventos: list[pygame.event.Event], superficie: pygame.Surface) -> None:
        """Método obligatorio para procesar la lógica y eventos del widget."""
        pass
    
    @abstractmethod
    def dibujar(self, superficie: pygame.Surface) -> None:
        """Método obligatorio para renderizar el widget en la pantalla."""
        pass