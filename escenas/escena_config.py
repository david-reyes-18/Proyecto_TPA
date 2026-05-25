import pygame
from ui.label import Label
from ui.boton import Boton
from escenas.escena_base import EscenaBase
from escenas.menu_principal import MenuPrincipal

class EscenaConfig(EscenaBase):
    def __init__(self, juego):
        super().__init__(juego)
        self.titulo = Label(
            text="CONFIGURACIÓN",
            font_size=42,
            color=(255,255,255),
            rel_x=0.5,
            rel_y=0.18,
            anchor="center"
        )

        self.boton_volver = Boton(
            text="VOLVER",
            rel_x=0.5,
            rel_y=0.80,
            width=220,
            height=60,
            command=self.volver
        )

        self.botones = [
            self.boton_volver
        ]

    def volver(self) -> None:
        self.juego.cambiar_escena(MenuPrincipal(self.juego))

    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        for boton in self.botones:
            boton.actualizar(eventos, self.juego.pantalla)

    def actualizar(self, dt: float) -> None:
        pass

    def dibujar(self, pantalla) -> None:
        pantalla.fill((35, 35, 50))
        self.titulo.dibujar(pantalla)
        for boton in self.botones:
            boton.dibujar(pantalla)