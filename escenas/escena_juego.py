from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import pytmx
from core.rutas import Rutas
from core.fuente import Fuente
from core.paleta import Paleta
from core.config import ESCALA_GLOB, DISTANCIA_INTERACCION, FRAME_ALTO, FRAME_ANCHO
from core.manejador_jsons import cargar_config_json, cargar_datos_json, guardar_datos_json
from core.manejador_musica import ManejadorMusica
from escenas.escena_base import EscenaBase
from escenas.escena_inventario import EscenaInventario
from escenas.escena_confirmar_salida import EscenaConfirmarSalida
from ui.frame import Frame
from ui.label import Label
from jugador.jugador import Jugador

if TYPE_CHECKING:
    from core.juego import Juego


class EscenaJuego(EscenaBase):
    """
    Escena principal, donde el jugador se moverá en su habitación
    y podrá interactuar con su laptop y el taller.
    """
    
    def __init__(self, juego: Juego):
        super().__init__(juego)
        
        self.juego = juego
        
        # Cargar el mapa de la habitacion del jugador
        ruta_mapa = str(Rutas.mapa("mapa.tmx"))
        self.datos_tmx = pytmx.load_pygame(ruta_mapa, pixelalpha=True)
        
        # Ancho y alto de un tile escalado (baldosa / fragmento de cuadrado)
        self.ancho_tile = self.datos_tmx.tilewidth * ESCALA_GLOB
        self.altura_tile = self.datos_tmx.tileheight * ESCALA_GLOB
        
        # Tamaño total del mapa en píxeles de pantalla
        self.ancho_mapa = self.datos_tmx.width * self.ancho_tile
        self.alto_mapa = self.datos_tmx.height * self.altura_tile
        
        # Carga todo el mapa
        self.superficie_mapa = self._renderizar_mapa()
        
        # Colisiones
        self.colisiones_paredes = self._cargar_colisiones("colisiones_paredes")
        self.colisiones_laptop = self._cargar_colisiones_por_tipo("Laptop")
        self.colisiones_taller = self._cargar_colisiones_por_tipo("Taller")
        
        self.todos_obstaculos = (
            self.colisiones_paredes
            + self.colisiones_laptop
            + self.colisiones_taller
        )
        
        # Objetos decorativos
        self.objetos_decorativos = self._cargar_objetos_decorativos()
        
        # Jugador
        posicion = cargar_config_json("posicion_jugador")
        
        self.jugador = Jugador(
            x=posicion["x"] if posicion["x"] != 0 else self.ancho_tile * 7,
            y=posicion["y"] if posicion["y"] != 0 else self.altura_tile * 10,
        )
        
        # Cámara
        ancho, alto = juego.pantalla.get_size()
        self.camara = pygame.Rect(0, 0, ancho, alto)
        
        # UI
        self.fuente_prompt = Fuente.obtener(18)
        self.objeto_cercano = None
        
        # Sprite del icono del jugador
        spritesheet = pygame.image.load(
            str(Rutas.imagen("jugador/jugador_estatico.png"))
        ).convert_alpha()
        
        self.jugador_icono = spritesheet.subsurface(
            (3 * FRAME_ANCHO, 0, FRAME_ANCHO, FRAME_ALTO)
        )
        
        self.jugador_icono = pygame.transform.scale(self.jugador_icono, (38, 48))
        
        # Barra del frame
        self.barra_superior = Frame(
            rel_x=0.5,
            rel_y=0.0,
            width=1.2,
            height=0.17,
            anchor="center",
            bg_color=(0, 0, 0),
            alpha=220,
            border_width=3,
            border_color=Paleta.TEXTO_PRINCIPAL
        )
        
        estilo_labeles = dict(
            font_size=16,
            rel_y=0.04,
            anchor="center"
        )
        
        # Labeles
        self.label_nombre = Label(
            text=self.juego.player_name,
            text_color=Paleta.TEXTO_PRINCIPAL,
            rel_x=0.1,
            **estilo_labeles
        )
        self.label_dinero = Label(
            text=f"${self.juego.jugador.dinero}",
            text_color=Paleta.TEXTO_DORADO,
            rel_x=0.5,
            **estilo_labeles
        )
        self.label_xp = Label(
            text=f"XP: {self.juego.jugador.experiencia}",
            text_color=Paleta.TEXTO_MORADO,
            rel_x=0.65,
            **estilo_labeles
        )
        
        self.label_nivel = Label(
            text=f"NIVEL: {self.juego.jugador.nivel}",
            text_color=Paleta.TEXTO_VERDE,
            rel_x=0.87,
            **estilo_labeles
        )
        
        self.labeles = [
            self.label_dinero,
            self.label_nombre,
            self.label_xp,
            self.label_nivel
        ]
        
        ManejadorMusica.reproducir("littleroot_town.ogg")
    
    
    def _guardar_posicion_jugador(self) -> None:
        """
        Guarda la posición actual del jugador en el
        json de config
        """
        datos = cargar_datos_json("config.json")
        datos["posicion_jugador"]["x"] = self.jugador.hitbox.x
        datos["posicion_jugador"]["y"] = self.jugador.hitbox.y
        guardar_datos_json("config.json", datos)
    
    def _renderizar_mapa(self) -> pygame.Surface:
        """
        Transforma los datos de mapa.tmx a un lienzo visible
        en el juego
        """
        # Crea un lienzo trasparente de todo el mapa
        superficie = pygame.Surface((self.ancho_mapa, self.alto_mapa), pygame.SRCALPHA)
        superficie.fill((0, 0, 0, 0))
        
        # Recorre cada capa del mapa
        for capa in self.datos_tmx.layers:
            # Descartamos capas que contengan coliciones o objetos
            if not isinstance(capa, pytmx.TiledTileLayer):
                continue
            
            # Recorremos todos los tiles del mapa (baldosas), junto con sus cordenadas x, y
            for x, y, imagen in capa.tiles():
                # Si no hay imagen continua al siguiente tile
                if imagen is None:
                    continue
                # Escalamos el mapa tile por tile en la superficie
                superficie.blit(
                    pygame.transform.scale(imagen, (self.ancho_tile, self.altura_tile)),
                    (x * self.ancho_tile, y * self.altura_tile),
                )
        # Retornamos la superficie
        return superficie
    
    def _cargar_colisiones(self, nombre_grupo: str) -> list[pygame.Rect]:
        """
        Función encargada de las colisiones del mapa
        """
        rects = []
        for capa in self.datos_tmx.layers:
            if isinstance(capa, pytmx.TiledObjectGroup) and capa.name == nombre_grupo:
                for obj in capa:
                    rects.append(pygame.Rect(
                        int(obj.x * ESCALA_GLOB), int(obj.y * ESCALA_GLOB),
                        int(obj.width * ESCALA_GLOB), int(obj.height * ESCALA_GLOB),
                    ))
        return rects
    
    def _cargar_colisiones_por_tipo(self, tipo: str) -> list[pygame.Rect]:
        rects = []
        for capa in self.datos_tmx.layers:
            if isinstance(capa, pytmx.TiledObjectGroup):
                for obj in capa:
                    if getattr(obj, "type", None) == tipo:
                        rects.append(pygame.Rect(
                            int(obj.x * ESCALA_GLOB), int(obj.y * ESCALA_GLOB),
                            int(obj.width * ESCALA_GLOB), int(obj.height * ESCALA_GLOB),
                        ))
        return rects
    
    def _cargar_objetos_decorativos(self) -> list[dict]:
        CONFIGS = {
            "Laptop": {
                "imagen": "tiles_escenario/computador-transparente.png",
                "escena": "laptop",
                "label": "Laptop"
            },
            "Taller": {
                "imagen": "tiles_escenario/taller.png",
                "escena": "taller",
                "label": "Taller"
            },
        }
        
        objetos = []
        
        # Recorremos cada capa del mapa
        for capa in self.datos_tmx.layers:
            # Si no es una capa de objetos la saltamos
            if not isinstance(capa, pytmx.TiledObjectGroup):
                continue
            
            #  Buscamos solo la capa de decoraciones_colisiones
            if capa.name != "decoraciones_colisiones":
                continue
            
            # Por cada objeto en la capa
            for objeto in capa:
                #Obtenemos el nombre del objeto
                nombre = getattr(objeto, "name", "")
                
                #Si el objeto no está en el config lo saltamos
                if nombre not in CONFIGS:
                    continue
                
                cfg = CONFIGS[nombre]
                imagen_orig = pygame.image.load(str(Rutas.imagen(cfg["imagen"]))).convert_alpha()
                ancho_dest = int(objeto.width * ESCALA_GLOB)
                alto_dest = int(objeto.height * ESCALA_GLOB)
                
                objetos.append({
                    "superficie": pygame.transform.scale(imagen_orig, (ancho_dest, alto_dest)),
                    "rect": pygame.Rect(int(objeto.x * ESCALA_GLOB), int(objeto.y * ESCALA_GLOB), ancho_dest, alto_dest),
                    "nombre": nombre,
                    "label": cfg["label"],
                    "escena": cfg["escena"],
                })
        return objetos
    
    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        """
        Revisa las teclas precionadas y verifica para abrir las escenas correspondientes
        """
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                # Si se preciona el botón ESC entonces llamará a la escena de confirmación para salir al menú principal
                if evento.key == pygame.K_ESCAPE:
                    self.juego.manejador_escenas.cambiar_escena(EscenaConfirmarSalida(self.juego))
                    
                # Si se preciona la tecla E cerca de un objeto interactuable se abre su escena
                elif evento.key == pygame.K_e and self.objeto_cercano:
                    self._abrir_escena(self.objeto_cercano["escena"])
                    
                # Si se preciona la I abrirá el inventario
                elif evento.key == pygame.K_i:
                    self.juego.manejador_escenas.cambiar_escena(EscenaInventario(self.juego))
                    
                # Si preciona C se abrirá la configuración
                elif evento.key == pygame.K_c:
                    from escenas.escena_config import EscenaConfig
                    self.juego.manejador_escenas.cambiar_escena(EscenaConfig(self.juego))
    
    def _abrir_escena(self, tipo: str):
        """
        Según el tipo de objeto con el que se interactue
        se abrirá una escena distinta
        """
        self._guardar_posicion_jugador()
        
        # Si es una laptop se abré la escena del correo
        if tipo == "laptop":
            from escenas.escena_correo import EscenaCorreo
            self.juego.manejador_escenas.cambiar_escena(EscenaCorreo(self.juego))
            
        # Si es el taller se abré la escena del taller
        elif tipo == "taller":
            from escenas.escena_taller import EscenaTaller
            self.juego.manejador_escenas.cambiar_escena(EscenaTaller(self.juego))
    
    def actualizar(self, dt: float):
        """
        Actualiza la posición del jugador
        """
        teclas = pygame.key.get_pressed()
        
        # Direcciones en x, y
        dx = dy = 0
        
        # desplazamiento = velocidad * tiempo transcurrido
        desplazamiento_por_frame = int(self.jugador.velocidad * dt)
        
        # Se verifica el movimiento horizontal y vertical
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dy -= desplazamiento_por_frame
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy += desplazamiento_por_frame
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= desplazamiento_por_frame
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += desplazamiento_por_frame
            
        # Se actualiza la posición del jugador
        self.jugador.actualizar(dt, dx, dy, self.todos_obstaculos)
        
        # Mantener dentro del mapa
        self.jugador.hitbox.clamp_ip(pygame.Rect(0, 0, self.ancho_mapa, self.alto_mapa))
        self.jugador.rect.midbottom = self.jugador.hitbox.midbottom
        
        # Cámara centrada en el jugador
        self.camara.center = self.jugador.rect.center
        self.camara.clamp_ip(pygame.Rect(0, 0, self.ancho_mapa, self.alto_mapa))
        
        # Proximidad a objetos (distancia al borde del rect)
        self.objeto_cercano = None
        
        # Cordenadas de la hitbox del jugador
        jugador_x = self.jugador.hitbox.centerx
        jugador_y = self.jugador.hitbox.centery
        
        for objeto in self.objetos_decorativos:
            rect = objeto["rect"]
            
            # Coordenadas del punto del objeto que está más cerca del jugador
            punto_cercano_x = max(rect.left, min(jugador_x, rect.right))
            punto_cercano_y = max(rect.top, min(jugador_y, rect.bottom))
            
            # Usando la formula de la distancia de dos puntos sacamos la distancia
            distancia = ((jugador_x - punto_cercano_x) ** 2 +
                         (jugador_y - punto_cercano_y) ** 2) ** 0.5
            
            # Si la distancia es menor o igual a la distancia de interaccion entonces hay un objeto cerca
            if distancia <= DISTANCIA_INTERACCION:
                self.objeto_cercano = objeto
                break
        
        # Actualizar textos de los labels de la barra superior
        self.label_nombre.text = self.juego.player_name
        self.label_dinero.text = f"${self.juego.jugador.dinero}"
        self.label_xp.text = f"XP: {self.juego.jugador.experiencia}"
    
    def dibujar(self, pantalla: pygame.Surface):
        pantalla.fill((0, 0, 0))
        pantalla.blit(self.superficie_mapa, (-self.camara.x, -self.camara.y))
        
        for obj in self.objetos_decorativos:
            pantalla.blit(obj["superficie"], (obj["rect"].x - self.camara.x, obj["rect"].y - self.camara.y))
            
        self.jugador.dibujar(pantalla, self.camara)
        
        if self.objeto_cercano:
            self._dibujar_prompt(pantalla, self.objeto_cercano["label"])
        
        self.barra_superior.dibujar(pantalla)
        
        # Icono del jugador (posición fija dentro de la barra)
        icon_x = 10
        icon_y = 10
        pantalla.blit(self.jugador_icono, (icon_x, icon_y))
        
        for label in self.labeles:
            label.dibujar(pantalla)

    def _dibujar_prompt(self, pantalla: pygame.Surface, label: str):
        texto = f"[E]  Interactuar con {label}"
        superficie = self.fuente_prompt.render(texto, False, (255, 255, 255))
        padding = 10
        ancho_caja = superficie.get_width() + padding * 2
        alto_caja = superficie.get_height() + padding * 2
        jugador_pant = self.jugador.rect.move(-self.camara.x, -self.camara.y)
        cx = jugador_pant.centerx
        cy = jugador_pant.top - alto_caja - 8
        fondo = pygame.Surface((ancho_caja, alto_caja), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 170))
        pygame.draw.rect(fondo, (255, 255, 255, 60), fondo.get_rect(), border_radius=6)
        pantalla.blit(fondo, (cx - ancho_caja // 2, cy))
        pantalla.blit(superficie, (cx - superficie.get_width() // 2, cy + padding))