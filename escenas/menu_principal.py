from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from core.rutas import Rutas
from core.paleta import Paleta
from core.manejador_musica import ManejadorMusica
from ui.label import Label
from ui.boton import Boton
from escenas.escena_base import EscenaBase

if TYPE_CHECKING:
    from core.juego import Juego


class MenuPrincipal(EscenaBase):
    
    """
    Escena que aparece al iniciar el juego muestra 
    tres botones, jugar, configuraciones y salir
    """
    
    def __init__(self, juego: Juego) -> None:
        
        super().__init__(juego)
        
        ManejadorMusica.reproducir("musica_menu.ogg")
        
        # Cargar imagen de fondo
        ancho, alto = juego.pantalla.get_size()
        imagen = pygame.image.load(str(Rutas.imagen("fondo_menu.png"))).convert()
        self.fondo = pygame.transform.scale(imagen, (ancho, alto))
        
        self.titulo = Label(
            text="INNOMATH",
            font_size=80,
            text_color=Paleta.TEXTO_TITULO,
            rel_x=0.5,
            rel_y=0.20,
            anchor="center"
        )
        
        # Estilo que debe tener cada botón
        estilo_boton = dict(
            width=0.4,
            height=0.065,
            font_size=25,
            bg_color=Paleta.BOTON_MENU_FONDO,
            hover_color=Paleta.BOTON_MENU_HOVER, 
            text_color=Paleta.BOTON_TEXTO,
            text_hover_color=Paleta.BOTON_TEXTO_HOVER,
            border_width=10,
            border_color=Paleta.BOTON_BORDER_COLOR,
            border_hover_color=Paleta.BOTON_BORDER_HOVER_COLOR,
            border_radius=10,
        )
        
        self.boton_juego = Boton(
            text="JUGAR",
            rel_x=0.5,
            rel_y=0.44,
            command=self.iniciar_juego,
            **estilo_boton
        )
        
        self.boton_config = Boton(
            text="CONFIGURACIÓN",
            rel_x=0.5,
            rel_y=0.57,
            command=self.abrir_config,
            **estilo_boton
        )
        
        self.boton_salir = Boton(
            text="SALIR",
            rel_x=0.5,
            rel_y=0.7,
            command=self.salir,
            **estilo_boton
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
        pantalla.blit(self.fondo, (0,0))
        self.titulo.dibujar(pantalla)
        for boton in self.botones:
            boton.dibujar(pantalla)