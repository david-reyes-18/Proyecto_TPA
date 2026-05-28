import pygame
from ui.widget import Widget
from core.fuente import Fuente
from typing import Callable


class Slider(Widget):
    """
    Clase que crea un slider de forma horizontal, donde sus parámetros
    son:
    
    text: texto que aparece a la izquierda de la barra.
    rel_x: posición relativa X del centro (0.0 – 1.0).
    rel_y: posición relativa Y del centro (0.0 – 1.0).
    width: width de la barra en píxeles.
    heigth:.heigth de la barra en píxeles.
    valor_inicial: valor de arranque (0.0 – 1.0).
    color_fill: color RGB de la parte rellena.
    on_change: callback opcional que recibe el nuevo valor (float).
    font_size: tamaño de fuente para la etiqueta y el porcentaje.
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
        on_change: Callable[[float], None] | None = None,
        font_size: int = 18,
    ):
        super().__init__(rel_x, rel_y, anchor="center")

        self.text = text
        self.width = width
        self.heigth = heigth
        self.valor = max(0.0, min(1.0, valor_inicial))
        self.color_fill = color_fill
        self.on_change = on_change
        self.font = Fuente.obtener(font_size)
        # Radio del botón circular
        self.knob_r = 10

        self._arrastrando = False
        # Rect de la pista, se recalcula en actualizar()
        self._track_rect = pygame.Rect(0, 0, width, heigth)


    def _calcular_track(self, superficie: pygame.Surface) -> pygame.Rect:
        """Devuelve el Rect de la pista centrado en la posición relativa."""
        cx, cy = self.obtener_posicion(superficie)
        return pygame.Rect(
            int(cx) - self.width // 2,
            int(cy) - self.heigth // 2,
            self.width,
            self.heigth,
        )

    def _valor_desde_x(self, mx: int) -> float:
        left = self._track_rect.x
        return max(0.0, min(1.0, (mx - left) / self.width))

    def _knob_x(self) -> int:
        return self._track_rect.x + int(self.valor * self.width)

    def _knob_cy(self) -> int:
        return self._track_rect.centery

    def set_valor(self, valor: float) -> None:
        self.valor = max(0.0, min(1.0, valor))

    def get_valor(self) -> float:
        return self.valor

    def actualizar(self, eventos: list[pygame.event.Event], superficie: pygame.Surface) -> None:
        self._track_rect = self._calcular_track(superficie)
        zona_clic = self._track_rect.inflate(0, 28)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if zona_clic.collidepoint(evento.pos):
                    self._arrastrando = True
                    self._actualizar_valor(evento.pos[0])

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self._arrastrando = False

            elif evento.type == pygame.MOUSEMOTION:
                if self._arrastrando:
                    self._actualizar_valor(evento.pos[0])

    def _actualizar_valor(self, mx: int) -> None:
        nuevo = self._valor_desde_x(mx)
        if nuevo != self.valor:
            self.valor = nuevo
            if self.on_change:
                self.on_change(self.valor)

    def dibujar(self, superficie: pygame.Surface) -> None:
        track = self._track_rect
        cx = track.centerx
        cy = track.centery

        # Etiqueta (a la izquierda)
        lbl_surf = self.font.render(self.text, False, (200, 200, 220))
        superficie.blit(lbl_surf, lbl_surf.get_rect(midright=(track.x - 14, cy)))

        # Pista (fondo)
        pygame.draw.rect(superficie, (50, 50, 70), track, border_radius=6)

        # Pista (relleno)
        fill = pygame.Rect(track.x, track.y, int(self.valor * self.width), self.heigth)
        if fill.width > 0:
            pygame.draw.rect(superficie, self.color_fill, fill, border_radius=6)

        # Knob
        kx = self._knob_x()
        pygame.draw.circle(superficie, (255, 255, 255), (kx, cy), self.knob_r)
        pygame.draw.circle(superficie, self.color_fill,  (kx, cy), self.knob_r - 3)

        # Porcentaje (a la derecha)
        pct_surf = self.font.render(f"{int(self.valor * 100)}%", False, (200, 200, 220))
        superficie.blit(pct_surf, pct_surf.get_rect(midleft=(track.right + 14, cy)))