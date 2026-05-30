from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from core.config import *
from core.manejador_musica import ManejadorMusica
from core.manejador_sonidos import ManejadorSonidos
from core.manejador_jsons import cargar_datos_json, guardar_datos_json, cargar_config_json
from ui.label import Label
from ui.boton import Boton
from ui.slider import Slider
from escenas.escena_base import EscenaBase
from escenas.menu_principal import MenuPrincipal

if TYPE_CHECKING:
    from core.juego import Juego


class EscenaConfig(EscenaBase):
    def __init__(self, juego: Juego):
        super().__init__(juego)

        self.resolucion_idx = 2
        for i, (width, height, _) in enumerate(RESOLUCIONES):
            if width == juego.pantalla.get_width() and height == juego.pantalla.get_height():
                self.resolucion_idx = i
                break

        self._msg_timer = 0.0
        self._msg_texto = ""

        # Labeles
        self.label_titulo = Label(
            text="CONFIGURACION",
            font_size=46, 
            color=(200, 180, 255),
            rel_x=0.5, 
            rel_y=0.12, 
            anchor="center",
        )
        self.label_audio = Label(
            text="AUDIO",
            font_size=20, 
            color=(160, 200, 255),
            rel_x=0.5, 
            rel_y=0.22, 
            anchor="center",
        )
        self.label_video = Label(
            text="RESOLUCIÓN DE PANTALLA",
            font_size=20, 
            color=(160, 200, 255),
            rel_x=0.5, 
            rel_y=0.57, 
            anchor="center",
        )
        
        self.label_res_nombre = Label(
            text=RESOLUCIONES[self.resolucion_idx][2],
            font_size=18, 
            color=(240, 240, 255),
            rel_x=0.5, 
            rel_y=0.625, 
            anchor="center",
        )
        
        self.label_msg = Label(
            text="",
            font_size=16, 
            color=(100, 255, 160),
            rel_x=0.5, 
            rel_y=0.80, 
            anchor="center",
        )
        
        # Conjunto de todos los labeles
        self.labels = [
            self.label_titulo,
            self.label_audio,
            self.label_video,
            self.label_res_nombre,
        ]
        
        # Cargar el volumen del json
        datos_volumen = cargar_config_json("volumen")
        volumen_musica = datos_volumen["musica"]
        volumen_sonidos = datos_volumen["sonidos"]
        
        # Sliders
        self.slider_musica = Slider(
            text="Musica",
            rel_x=0.5, 
            rel_y=0.30,
            valor_inicial=volumen_musica,
            color_fill=(100, 180, 255),
            on_change=self._on_musica_change,
        )
        self.slider_sonidos = Slider(
            text="Efectos",
            rel_x=0.5, 
            rel_y=0.44,
            valor_inicial=volumen_sonidos,
            color_fill=(180, 120, 255),
            on_change=self._on_efectos_change
        )

        #Conjunto de todos los sliders
        self.sliders = [
                self.slider_musica, 
                self.slider_sonidos
            ]

        # Botones
        self.boton_resolucion_anterior = Boton(
            text="<", 
            rel_x=0.34, 
            rel_y=0.62, 
            width=44, 
            height=44,
            command=self._resolucion_anterior, 
            font_size=26,
            bg_color=(60, 60, 90), 
            hover_color=(100, 100, 160),
        )
        self.boton_resolucion_sgte = Boton(
            text=">", 
            rel_x=0.66, 
            rel_y=0.62, 
            width=44, 
            height=44,
            command=self._resolucion_sgte, 
            font_size=26,
            bg_color=(60, 60, 90), 
            hover_color=(100, 100, 160),
        )
        self.boton_aplicar = Boton(
            text="APLICAR RESOLUCIÓN", 
            rel_x=0.5, 
            rel_y=0.72,
            width=0.4, 
            height=60,
            command=self._aplicar_resolucion, 
            font_size=18,
            bg_color=(50, 120, 80), 
            hover_color=(70, 180, 110),
        )
        self.boton_volver = Boton(
            text="VOLVER", 
            rel_x=0.5, 
            rel_y=0.87, 
            width=220, 
            height=52,
            command=self._volver,
            font_size=22,
            bg_color=(80, 40, 40), 
            hover_color=(140, 60, 60),
        )

        self.botones = [
            self.boton_resolucion_anterior,
            self.boton_resolucion_sgte,
            self.boton_aplicar,
            self.boton_volver,
        ]
    
    # Comandos de slider y botones
    def _on_musica_change(self, valor: float) -> None:
        ManejadorMusica.establecer_volumen(valor)
    
    def _on_efectos_change(self, valor: float) -> None:
        ManejadorSonidos.establecer_volumen(valor)


    def _resolucion_anterior(self) -> None:
        self.resolucion_idx = (self.resolucion_idx - 1) % len(RESOLUCIONES)
        self.label_res_nombre.text = RESOLUCIONES[self.resolucion_idx][2]

    def _resolucion_sgte(self) -> None:
        self.resolucion_idx = (self.resolucion_idx + 1) % len(RESOLUCIONES)
        self.label_res_nombre.text = RESOLUCIONES[self.resolucion_idx][2]

    def _aplicar_resolucion(self) -> None:
        ancho, alto, label = RESOLUCIONES[self.resolucion_idx]
        self.juego.pantalla = pygame.display.set_mode((ancho, alto))
        
        datos_config = cargar_datos_json("config.json")
        datos_config["resolucion"]["ancho"] = ancho
        datos_config["resolucion"]["alto"] = alto
        guardar_datos_json("config.json", datos_config)
        self._msg_texto = f"Resolucion aplicada: {label}"
        self._msg_timer = 2.5

    def _volver(self) -> None:
        self.juego.manejador_escenas.cambiar_escena(MenuPrincipal(self.juego))

    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        pantalla = self.juego.pantalla
        for slider in self.sliders:
            slider.actualizar(eventos, pantalla)
        for boton in self.botones:
            boton.actualizar(eventos, pantalla)

    def actualizar(self, dt: float) -> None:
        if self._msg_timer > 0:
            self._msg_timer -= dt

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pw, ph = pantalla.get_size()
        cx = pw // 2

        # Fondo degradado
        for y in range(ph):
            t = y / ph
            pygame.draw.line(
                pantalla,
                (int(18 + t * 10), int(18 + t * 8), int(40 + t * 20)),
                (0, y), (pw, y),
            )

        # Barras laterales decorativas
        bar = pygame.Surface((6, ph), pygame.SRCALPHA)
        bar.fill((120, 100, 220, 80))
        pantalla.blit(bar, (30, 0))
        pantalla.blit(bar, (pw - 36, 0))

        # Línea decorativa bajo el título
        pygame.draw.line(
            pantalla, (120, 100, 200),
            (cx - 160, int(ph * 0.19)), (cx + 160, int(ph * 0.19)), 2,
        )

        # Labels, sliders y botones
        for label in self.labels:
            label.dibujar(pantalla)
        for slider in self.sliders:
            slider.dibujar(pantalla)
        for boton in self.botones:
            boton.dibujar(pantalla)

        # Mensaje temporal (alpha variable, no puede ser Label normal)
        if self._msg_timer > 0:
            self.label_msg.text = self._msg_texto
            alpha = min(255, int(self._msg_timer * 200))
            try:
                from core.fuente import Fuente
                f = Fuente.obtener(16)
            except Exception:
                f = pygame.font.SysFont("consolas", 16)
            ms = f.render(self._msg_texto, False, (100, 255, 160))
            ms.set_alpha(alpha)
            pantalla.blit(ms, ms.get_rect(center=(cx, int(ph * 0.80))))