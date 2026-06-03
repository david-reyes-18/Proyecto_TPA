from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from escenas.escena_base import EscenaBase
from ui.label import Label
from ui.boton import Boton
from core.paleta import Paleta

if TYPE_CHECKING:
    from core.juego import Juego


class EscenaConfirmarSalida(EscenaBase):
    
    """Escena que pregunta al jugador si en verdad
    desea salir al menu principal
    """
    
    def __init__(self, juego: Juego) -> None:
        
        super().__init__(juego)
        
        self.juego = juego
        
        # Label de pregunta
        self.label_salida = Label(
            text="¿Salir al menu principal?",
            font_size=30,
            text_color=Paleta.TEXTO_PRINCIPAL,
            rel_x=0.5,
            rel_y=0.4,
            anchor="center"
        )
        
        estilo_botones = dict(
            rel_y=0.6,
            width=220,
            height=52,
            font_size=22,
            text_hover_color=Paleta.BOTON_TEXTO_HOVER,
            border_width=4,
            border_color=Paleta.BOTON_BORDER_COLOR,
            border_hover_color=Paleta.BOTON_BORDER_HOVER_COLOR,
            border_radius=10
        )
        
        self.boton_si = Boton(
            text="SI",
            rel_x=0.35,
            command=self._volver_menu_principal,
            bg_color=Paleta.BOTON_PELIGRO_FONDO,
            hover_color=Paleta.BOTON_PELIGRO_HOVER,
            text_color=Paleta.BOTON_PELIGRO_TEXTO,
            **estilo_botones
        )
        
        self.boton_no = Boton(
            text="NO",
            rel_x=0.65,
            command=self._volver_juego,
            bg_color=Paleta.BOTON_OK_FONDO,
            hover_color=Paleta.BOTON_OK_HOVER,
            text_color=Paleta.BOTON_OK_TEXTO,
            **estilo_botones
        )
        
        self.botones = [
            self.boton_si,
            self.boton_no,
        ]
        
        
    def _volver_menu_principal(self) -> None:
        from escenas.menu_principal import MenuPrincipal
        self.juego.manejador_escenas.cambiar_escena(MenuPrincipal(self.juego))
    
    def _volver_juego(self) -> None:
        from escenas.escena_juego import EscenaJuego
        self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))
        
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        for boton in self.botones:
            boton.actualizar(eventos, self.juego.pantalla)
        
    def actualizar(self, dt: float) -> None:
        pass
    
    def dibujar(self, pantalla: pygame.Surface):
        pantalla.fill(Paleta.FONDO_PANTALLA)
        self.label_salida.dibujar(pantalla)
        
        for boton in self.botones:
            boton.dibujar(pantalla)