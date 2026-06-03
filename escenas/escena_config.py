from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from core.config import RESOLUCIONES
from core.manejador_musica import ManejadorMusica
from core.manejador_sonidos import ManejadorSonidos
from core.manejador_jsons import cargar_datos_json, guardar_datos_json, cargar_config_json
from core.paleta import Paleta
from ui.label import Label
from ui.boton import Boton
from ui.slider import Slider
from escenas.escena_base import EscenaBase
from escenas.menu_principal import MenuPrincipal
from escenas.escena_juego import EscenaJuego

if TYPE_CHECKING:
    from core.juego import Juego


class EscenaConfig(EscenaBase):
    
    """
    Escena de configuraciones del sistema, como lo es el volumen
    de la música y efectos de sonido, asi como el tamaño de la 
    ventana
    """
    
    def __init__(self, juego: Juego):
        
        super().__init__(juego)
        
        self.indice_resolucion = 0
        
        # Obtenemos el índice de la resolución actual
        for i, (ancho, alto, _) in enumerate(RESOLUCIONES):
            if ancho == juego.pantalla.get_width() and alto == juego.pantalla.get_height():
                self.indice_resolucion = i
                break
        
        # Mensaje y tiempo en el que aparecerá el mensaje
        self.tiempo_mensaje = 0.0
        self.mensaje = ""

        # Labeles
        self.label_titulo = Label(
            text="CONFIGURACIÓN",
            font_size=46, 
            text_color=Paleta.TEXTO_TITULO,
            rel_x=0.5, 
            rel_y=0.12, 
            anchor="center",
        )
        self.label_audio = Label(
            text="AUDIO",
            font_size=20, 
            text_color=Paleta.TEXTO_PRINCIPAL,
            rel_x=0.5, 
            rel_y=0.22, 
            anchor="center",
        )
        self.label_video = Label(
            text="RESOLUCIÓN DE PANTALLA",
            font_size=20, 
            text_color=Paleta.TEXTO_SUBTITULO,
            rel_x=0.5, 
            rel_y=0.55, 
            anchor="center",
        )
        
        self.label_resolucion = Label(
            text=RESOLUCIONES[self.indice_resolucion][2],
            font_size=18, 
            text_color=Paleta.TEXTO_PRINCIPAL,
            rel_x=0.5, 
            rel_y=0.625,
            anchor="center",
        )
        
        self.label_mensaje = Label(
            text="",
            font_size=16, 
            text_color=Paleta.TEXTO_VERDE,
            rel_x=0.5, 
            rel_y=0.80, 
            anchor="center",
        )
        
        # Conjunto de todos los labeles
        self.labels = [
            self.label_titulo,
            self.label_audio,
            self.label_video,
            self.label_resolucion,
        ]
        
        # Cargar el volumen del json
        datos_volumen = cargar_config_json("volumen")
        
        volumen_musica = datos_volumen["musica"]
        
        # Sliders
        
        estilo_slider = dict(
            rel_x=0.5,
            color_unfill=Paleta.SLIDER_FONDO,
            font_size=20,
            text_color=Paleta.TEXTO_SECUNDARIO,
            knob_border_color=Paleta.SLIDER_KNOB_BORDER_COLOR
        )
        
        self.slider_musica = Slider(
            text="Musica",
            rel_y=0.30,
            valor_inicial=volumen_musica,
            color_fill=Paleta.SLIDER_MUSICA_RELLENO,
            command=self._on_musica_change,
            knob_color=Paleta.SLIDER_MUSICA_KNOB_CENTRO,
            **estilo_slider
        )
        
        volumen_sonidos = datos_volumen["sonidos"]
        
        self.slider_sonidos = Slider(
            text="Efectos",
            rel_y=0.44,
            valor_inicial=volumen_sonidos,
            color_fill=Paleta.SLIDER_SONIDO_RELLENO,
            command=self._on_efectos_change,
            knob_color=Paleta.SLIDER_SONIDO_KNOB_CENTRO,
            **estilo_slider
        )
        
        #Conjunto de todos los sliders
        self.sliders = [
                self.slider_musica, 
                self.slider_sonidos
            ]
        
        # Botones
        
        boton_resolucion_estilo = dict(
            rel_y=0.62,
            width=44,
            height=44,
            font_size=26,
            bg_color=Paleta.BOTON_CONFIG_FONDO,
            hover_color=Paleta.BOTON_CONFIG_HOVER,
            text_color=Paleta.BOTON_TEXTO,
            text_hover_color=Paleta.BOTON_TEXTO_HOVER,
            border_width=4,
            border_color=Paleta.BOTON_BORDER_COLOR,
            border_hover_color=Paleta.BOTON_BORDER_HOVER_COLOR,
            border_radius=10
        )
        
        self.boton_resolucion_anterior = Boton(
            text="<", 
            rel_x=0.34, 
            command=self._resolucion_anterior,
            **boton_resolucion_estilo
        )
        self.boton_resolucion_sgte = Boton(
            text=">", 
            rel_x=0.66, 
            command=self._resolucion_sgte,
            **boton_resolucion_estilo
        )
        
        self.boton_aplicar = Boton(
            text="APLICAR RESOLUCIÓN", 
            rel_x=0.5, 
            rel_y=0.72,
            width=0.4, 
            height=60,
            command=self._aplicar_resolucion, 
            font_size=22,
            bg_color=Paleta.BOTON_OK_FONDO, 
            hover_color=Paleta.BOTON_OK_HOVER,
            text_color=Paleta.BOTON_OK_TEXTO,
            text_hover_color=Paleta.BOTON_TEXTO_HOVER,
            border_width=4,
            border_color=Paleta.BOTON_BORDER_COLOR,
            border_hover_color=Paleta.BOTON_BORDER_HOVER_COLOR,
            border_radius=10
        )
        self.boton_volver = Boton(
            text="VOLVER", 
            rel_x=0.5, 
            rel_y=0.87, 
            width=220, 
            height=52,
            command=self._volver,
            font_size=22,
            bg_color=Paleta.BOTON_PELIGRO_FONDO, 
            hover_color=Paleta.BOTON_PELIGRO_HOVER,
            text_color=Paleta.BOTON_PELIGRO_TEXTO,
            text_hover_color=Paleta.BOTON_TEXTO_HOVER,
            border_width=4,
            border_color=Paleta.BOTON_BORDER_COLOR,
            border_hover_color=Paleta.BOTON_BORDER_HOVER_COLOR,
            border_radius=10
        )
        
        self.botones = [
            self.boton_resolucion_anterior,
            self.boton_resolucion_sgte,
            self.boton_aplicar,
            self.boton_volver,
        ]
    
    # Comandos de os sliders
    def _on_musica_change(self, valor: float) -> None:
        ManejadorMusica.establecer_volumen(valor)
    
    def _on_efectos_change(self, valor: float) -> None:
        ManejadorSonidos.establecer_volumen(valor)
    
    # Comandos de los botones de resolucion
    def _resolucion_anterior(self) -> None:
        self.indice_resolucion = (self.indice_resolucion - 1) % len(RESOLUCIONES)
        self.label_resolucion.text = RESOLUCIONES[self.indice_resolucion][2]

    def _resolucion_sgte(self) -> None:
        self.indice_resolucion = (self.indice_resolucion + 1) % len(RESOLUCIONES)
        self.label_resolucion.text = RESOLUCIONES[self.indice_resolucion][2]

    # Boton de aplicar resolucion (Guarda la resolucion actual en config.json)
    def _aplicar_resolucion(self) -> None:
        
        ancho, alto, label = RESOLUCIONES[self.indice_resolucion]
        
        #Aplicando la resolucion a la pantalla
        self.juego.pantalla = pygame.display.set_mode((ancho, alto))
        
        #Guardando la resolucion en config.json
        datos_config = cargar_datos_json("config.json")
        datos_config["resolucion"]["ancho"] = ancho
        datos_config["resolucion"]["alto"] = alto
        guardar_datos_json("config.json", datos_config)
        
        # Mensaje de aplicacion de la resolucion
        self.mensaje = f"Resolucion aplicada: {label}"
        self.tiempo_mensaje = 2.5
    
    # Vuelve al menu
    def _volver(self) -> None:
        
        """
        Vuelve a la escena anterior a la de escena config,
        pudiendo ser escena menu principal o escena juego.
        """
        
        if isinstance(self.juego.manejador_escenas.escena_anterior, MenuPrincipal):
            self.juego.manejador_escenas.cambiar_escena(MenuPrincipal(self.juego))
        elif isinstance(self.juego.manejador_escenas.escena_anterior, EscenaJuego):
            self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))
        else:
            self.juego.manejador_escenas.cambiar_escena(MenuPrincipal(self.juego))
    
    
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        
        pantalla = self.juego.pantalla
        
        # Si se preciona el boton ESCAPE vuelve al menu principal o al juego
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self._volver()
                    return
        
        # Actualizar todos los sliders
        for slider in self.sliders:
            slider.actualizar(eventos, pantalla)
        
        # Actualizar todos los botones
        for boton in self.botones:
            boton.actualizar(eventos, pantalla)
    
    def actualizar(self, dt: float) -> None:
        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje -= dt
    
    def dibujar(self, pantalla: pygame.Surface) -> None:
        
        # Rellena la pantalla con un color
        pantalla.fill(Paleta.FONDO_PANTALLA)
        
        # Dibuja labels, sliders y botones
        for label in self.labels:
            label.dibujar(pantalla)
        for slider in self.sliders:
            slider.dibujar(pantalla)
        for boton in self.botones:
            boton.dibujar(pantalla)