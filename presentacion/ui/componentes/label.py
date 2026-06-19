import pygame
from presentacion.ui.widget import Widget
from infraestructura.texto.fuente import Fuente


class Label(Widget):
    
    """
    Permite crear un botón precionable, el cual puede llamar
    a una función, donde sus parámetros son:
    
    - text: texto que tendrá el botón por dentro
    - font_size: tamaño de la letra.
    - text_color: color del texto.
    - rel_x: posición relativa en x, donde x ∈ [0, 1].
    - rel_y: posición relativa en y, donde y ∈ [0, 1].
    - anchor: punto de referencia de cada widget que se va a alinear.
    """
    
    def __init__(
        self,
        text: str,
        font_size: int = 15,
        text_color: tuple = (255, 255, 255),
        rel_x: float = 0.5,
        rel_y: float = 0.5,
        anchor: str = "topleft"
    ):
        super().__init__(rel_x, rel_y, anchor)
        
        self.text = text
        self.text_color = text_color
        self.fuente = Fuente.obtener(font_size)

    def actualizar(self, eventos: list[pygame.event.Event], superficie: pygame.Surface) -> None:
        return super().actualizar(eventos, superficie)
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        texto_superficie = self.fuente.render(
            self.text,
            False,
            self.text_color
        )
        rect = texto_superficie.get_rect()
        x, y = self.obtener_posicion(superficie)
        rect = self.aplicar_anchor(rect, x, y)
        superficie.blit(texto_superficie, rect)