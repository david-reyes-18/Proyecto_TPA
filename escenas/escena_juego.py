import pygame
import pytmx
from escenas.escena_base import EscenaBase
from escenas.menu_principal import MenuPrincipal
from jugador.jugador import Jugador
from core.rutas import Rutas
from core.fuente import Fuente

ESCALA = 3
DIST_INTERACCION = 60


class EscenaJuego(EscenaBase):
    def __init__(self, juego):
        super().__init__(juego)
        self.juego = juego
        
        # Cargar el mapa
        ruta_mapa = str(Rutas.mapa("mapa.tmx"))
        self.tmx_data = pytmx.load_pygame(ruta_mapa, pixelalpha=True)
        self.tile_w = self.tmx_data.tilewidth  * ESCALA
        self.tile_h = self.tmx_data.tileheight * ESCALA
        self.mapa_pixel_w = self.tmx_data.width  * self.tile_w
        self.mapa_pixel_h = self.tmx_data.height * self.tile_h
        self.superficie_mapa = self._renderizar_mapa()
        
        # --- Colisiones ---
        self.colisiones_paredes = self._cargar_colisiones("colisiones_paredes")
        self.colisiones_laptop  = self._cargar_colisiones_por_tipo("Laptop")
        self.colisiones_taller  = self._cargar_colisiones_por_tipo("Taller")
        self.todos_obstaculos   = (
            self.colisiones_paredes
            + self.colisiones_laptop
            + self.colisiones_taller
        )
 
        # --- Objetos decorativos ---
        self.objetos_decorativos = self._cargar_objetos_decorativos()
 
        # --- Jugador ---
        self.jugador = Jugador(
            x=self.tile_w * 7,
            y=self.tile_h * 10,
        )
 
        # --- Cámara ---
        ancho, alto = juego.pantalla.get_size()
        self.camara = pygame.Rect(0, 0, ancho, alto)
 
        # --- UI ---
        self.fuente_prompt  = Fuente.obtener(18)
        self.objeto_cercano = None
 
    # ------------------------------------------------------------------
    # Helpers carga
    # ------------------------------------------------------------------
 
    def _renderizar_mapa(self) -> pygame.Surface:
        sup = pygame.Surface((self.mapa_pixel_w, self.mapa_pixel_h), pygame.SRCALPHA)
        sup.fill((0, 0, 0, 0))
        for capa in self.tmx_data.layers:
            if not isinstance(capa, pytmx.TiledTileLayer):
                continue
            for x, y, imagen in capa.tiles():
                if imagen is None:
                    continue
                sup.blit(
                    pygame.transform.scale(imagen, (self.tile_w, self.tile_h)),
                    (x * self.tile_w, y * self.tile_h),
                )
        return sup
 
    def _cargar_colisiones(self, nombre_grupo: str) -> list[pygame.Rect]:
        rects = []
        for capa in self.tmx_data.layers:
            if isinstance(capa, pytmx.TiledObjectGroup) and capa.name == nombre_grupo:
                for obj in capa:
                    rects.append(pygame.Rect(
                        int(obj.x * ESCALA), int(obj.y * ESCALA),
                        int(obj.width * ESCALA), int(obj.height * ESCALA),
                    ))
        return rects
 
    def _cargar_colisiones_por_tipo(self, tipo: str) -> list[pygame.Rect]:
        rects = []
        for capa in self.tmx_data.layers:
            if isinstance(capa, pytmx.TiledObjectGroup):
                for obj in capa:
                    if getattr(obj, "type", None) == tipo:
                        rects.append(pygame.Rect(
                            int(obj.x * ESCALA), int(obj.y * ESCALA),
                            int(obj.width * ESCALA), int(obj.height * ESCALA),
                        ))
        return rects
 
    def _cargar_objetos_decorativos(self) -> list[dict]:
        CONFIGS = {
            "Laptop": {"imagen": "tiles_escenario/computador-transparente.png", "escena": "laptop", "label": "Laptop"},
            "Taller": {"imagen": "tiles_escenario/taller.png",                  "escena": "taller", "label": "Taller"},
        }
        objetos = []
        for capa in self.tmx_data.layers:
            if not isinstance(capa, pytmx.TiledObjectGroup):
                continue
            if capa.name != "decoraciones_colisiones":
                continue
            for obj in capa:
                nombre = getattr(obj, "name", "")
                if nombre not in CONFIGS:
                    continue
                cfg = CONFIGS[nombre]
                imagen_orig = pygame.image.load(str(Rutas.imagen(cfg["imagen"]))).convert_alpha()
                ancho_dest  = int(obj.width  * ESCALA)
                alto_dest   = int(obj.height * ESCALA)
                objetos.append({
                    "superficie": pygame.transform.scale(imagen_orig, (ancho_dest, alto_dest)),
                    "rect":       pygame.Rect(int(obj.x * ESCALA), int(obj.y * ESCALA), ancho_dest, alto_dest),
                    "nombre":     nombre,
                    "label":      cfg["label"],
                    "escena":     cfg["escena"],
                })
        return objetos
 
    # ------------------------------------------------------------------
    # Ciclo
    # ------------------------------------------------------------------
 
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.juego.manejador_escenas.cambiar_escena(MenuPrincipal(self.juego))
                elif evento.key == pygame.K_e and self.objeto_cercano:
                    self._abrir_escena(self.objeto_cercano["escena"])
 
    def _abrir_escena(self, tipo: str):
        if tipo == "laptop":
            from escenas.escena_laptop import EscenaLaptop
            self.juego.manejador_escenas.cambiar_escena(EscenaLaptop(self.juego))
        elif tipo == "taller":
            from escenas.escena_taller import EscenaTaller
            self.juego.manejador_escenas.cambiar_escena(EscenaTaller(self.juego))
 
    def actualizar(self, dt: float):
        teclas = pygame.key.get_pressed()
        dx = dy = 0
        if teclas[pygame.K_w]:    dy -= int(self.jugador.velocidad * dt)
        if teclas[pygame.K_s]:  dy += int(self.jugador.velocidad * dt)
        if teclas[pygame.K_a]:  dx -= int(self.jugador.velocidad * dt)
        if teclas[pygame.K_d]: dx += int(self.jugador.velocidad * dt)
        
        self.jugador.actualizar(dt, dx, dy, self.todos_obstaculos)
 
        # Mantener dentro del mapa
        self.jugador.hitbox.clamp_ip(pygame.Rect(0, 0, self.mapa_pixel_w, self.mapa_pixel_h))
        self.jugador.rect.midbottom = self.jugador.hitbox.midbottom
 
        # Cámara centrada en el jugador
        self.camara.center = self.jugador.rect.center
        self.camara.clamp_ip(pygame.Rect(0, 0, self.mapa_pixel_w, self.mapa_pixel_h))
 
        # Proximidad a objetos (distancia al borde del rect)
        self.objeto_cercano = None
        jx, jy = self.jugador.hitbox.centerx, self.jugador.hitbox.centery
        for obj in self.objetos_decorativos:
            r = obj["rect"]
            cx = max(r.left, min(jx, r.right))
            cy = max(r.top,  min(jy, r.bottom))
            if ((jx - cx) ** 2 + (jy - cy) ** 2) ** 0.5 <= DIST_INTERACCION:
                self.objeto_cercano = obj
                break
 
    def dibujar(self, pantalla: pygame.Surface):
        pantalla.fill((0, 0, 0))
        pantalla.blit(self.superficie_mapa, (-self.camara.x, -self.camara.y))
 
        for obj in self.objetos_decorativos:
            pantalla.blit(obj["superficie"], (obj["rect"].x - self.camara.x, obj["rect"].y - self.camara.y))
 
        self.jugador.dibujar(pantalla, self.camara)
 
        if self.objeto_cercano:
            self._dibujar_prompt(pantalla, self.objeto_cercano["label"])
 
    def _dibujar_prompt(self, pantalla: pygame.Surface, label: str):
        texto   = f"[E]  Interactuar con {label}"
        surf    = self.fuente_prompt.render(texto, False, (255, 255, 255))
        padding = 10
        ancho_caja = surf.get_width()  + padding * 2
        alto_caja  = surf.get_height() + padding * 2
        jugador_pant = self.jugador.rect.move(-self.camara.x, -self.camara.y)
        cx = jugador_pant.centerx
        cy = jugador_pant.top - alto_caja - 8
        fondo = pygame.Surface((ancho_caja, alto_caja), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 170))
        pygame.draw.rect(fondo, (255, 255, 255, 60), fondo.get_rect(), border_radius=6)
        pantalla.blit(fondo, (cx - ancho_caja // 2, cy))
        pantalla.blit(surf,  (cx - surf.get_width() // 2, cy + padding))