from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from ui.label import Label
from ui.boton import Boton
from escenas.escena_base import EscenaBase

if TYPE_CHECKING:
    from core.juego import Juego


class MenuPrincipal(EscenaBase):
    def __init__(self, juego: Juego) -> None:
        super().__init__(juego)
        
        self.titulo = Label(
            text="INNOMATH",
            font_size=56,
            color=(255, 255, 255),
            rel_x=0.5,
            rel_y=0.20,
            anchor="center"
        )
        
        self.boton_juego = Boton(
            text="JUGAR",
            rel_x=0.5,
            rel_y=0.45,
            width=0.4,
            height=60,
            command=self.iniciar_juego
        )
        
        self.boton_config = Boton(
            text="CONFIGURACIÓN",
            rel_x=0.5,
            rel_y=0.57,
            width=0.4,
            height=60,
            command=self.abrir_config
        )
        
        self.boton_salir = Boton(
            text="SALIR",
            rel_x=0.5,
            rel_y=0.69,
            width=0.4,
            height=60,
            command=self.salir
        )
        
        self.botones = [
            self.boton_juego,
            self.boton_config,
            self.boton_salir
        ]
    
    
    def iniciar_juego(self) -> None:
        from escenas.escena_juego import EscenaJuego
        self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))
    
    def abrir_config(self) -> None:
        from escenas.escena_config import EscenaConfig
        self.juego.manejador_escenas.cambiar_escena(EscenaConfig(self.juego))
    
    def salir(self) -> None:
        self.juego.corriendo = False
    
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        for boton in self.botones:
            boton.actualizar(eventos, self.juego.pantalla)
    
    def actualizar(self, dt: float) -> None:
        pass

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((20, 20, 30))
        self.titulo.dibujar(pantalla)
        for boton in self.botones:
            boton.dibujar(pantalla)