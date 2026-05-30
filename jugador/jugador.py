import pygame
from core.rutas import Rutas
from core.config import *
from core.manejador_sonidos import ManejadorSonidos


class Jugador:
    
    """
    Modela al jugador
    """
    
    def __init__(self, x: int, y: int):
        
        self.ancho: int = FRAME_ANCHO * ESCALA_JUGADOR
        self.alto: int = FRAME_ALTO * ESCALA_JUGADOR
        
        self._timer_pasos = 0.0
        self._intervalo_pasos = 0.35  # segundos entre cada paso
        
        # Hitbox de los pies
        hitbox_pies: int = self.alto // 4
        
        # Hitbox personaje (solo de los pies para efecto 2d retro)
        self.hitbox = pygame.Rect(
            x,
            y + self.alto - hitbox_pies,
            self.ancho,
            hitbox_pies
        )
        
        # Rect para el personaje
        self.rect = pygame.Rect(
            x,
            y,
            self.ancho,
            self.alto
        )
        
        # Velocidad personaje
        self.velocidad: int = 100 * ESCALA_GLOB
        
        # Sprites jugador para modo estatico y corriendo
        self.sprites_jugador_estatico: list = self._cargar_sprites_estatico()
        self.sprites_jugador_corriendo: dict = self._cargar_sprites_corriendo()
        
        # Estados
        self.direccion: str = "ABAJO" #Dirección actual
        self.moviendose: bool = False
        
        # Índices de los sprites actuales
        self.indice_estatico = 0
        self.indice_corriendo = 0
        
        self.t_run = 0.0
    
    # Cargar Sprites
    
    def _escalar(self, superficie: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(
            superficie,
            (self.ancho, self.alto)
        )
    
    def _cargar_sprites_estatico(self) -> list[pygame.Surface]:
        spritesheet = pygame.image.load(
            str(Rutas.imagen("jugador/jugador_estatico.png"))
        ).convert_alpha()
        
        frames = []
        
        for i in range(FRAMES_ESTATICO):
            frame = spritesheet.subsurface(
                (i * FRAME_ANCHO, 0, FRAME_ANCHO, FRAME_ALTO)
            )
            
            frames.append(
                self._escalar(frame)
            )
        return frames
    
    
    def _cargar_sprites_corriendo(self) -> dict[str, list[pygame.Surface]]:
        spritesheet = pygame.image.load(
            str(Rutas.imagen("jugador/jugador_corriendo.png"))
        ).convert_alpha()
        
        animaciones = {}
        
        for indice_direccion, direccion in enumerate(DIRECCIONES):
            frames = []
            for i in range(FRAMES_POR_DIRECCION):
                frame_index = indice_direccion * FRAMES_POR_DIRECCION + i
                frame = spritesheet.subsurface(
                    (
                        frame_index * FRAME_ANCHO,
                        0,
                        FRAME_ANCHO,
                        FRAME_ALTO
                    )
                )
                frames.append(
                    self._escalar(frame)
                )
            animaciones[direccion] = frames
        return animaciones
    
    
    def actualizar(
        self,
        dt: float,
        dx: int,
        dy: int,
        obstaculos: list[pygame.Rect]
    ):
        
        self.moviendose: bool = dx != 0 or dy != 0

        # Calcular en que dirección se está moviendo
        if dx < 0:
            self.direccion = "IZQUIERDA"
        
        elif dx > 0:
            self.direccion = "DERECHA"
        
        elif dy < 0:
            self.direccion = "ARRIBA"
        
        elif dy > 0:
            self.direccion = "ABAJO"
        
        # Calcular el indice del frame estático por cada tipo de dirección
        if self.direccion == "IZQUIERDA":
            self.indice_estatico = 2
        elif self.direccion == "DERECHA":
            self.indice_estatico = 0
        elif self.direccion == "ARRIBA":
            self.indice_estatico = 1
        elif self.direccion == "ABAJO":
            self.indice_estatico = 3
        
        # Movimiento en x
        self.hitbox.x += dx
        
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo):
                if dx > 0:
                    self.hitbox.right = obstaculo.left
                elif dx < 0:
                    self.hitbox.left = obstaculo.right
        
        # Movimiento eje y
        self.hitbox.y += dy
        
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo):
                if dy > 0:
                    self.hitbox.bottom = obstaculo.top
                elif dy < 0:
                    self.hitbox.top = obstaculo.bottom

        # Sincronizar sprite con hitbox
        self.rect.midbottom = self.hitbox.midbottom
        
        # run
        if self.moviendose:
            self.t_run += dt
            if self.t_run >= 1 / FPS_CORRIENDO:
                self.t_run = 0
                self.indice_corriendo = (
                    self.indice_corriendo + 1
                ) % FRAMES_POR_DIRECCION
        else:
            self.indice_corriendo = 0
            self.t_run = 0
        
        if self.moviendose:
            self._timer_pasos -= dt
            if self._timer_pasos <= 0:
                ManejadorSonidos.reproducir("pasos.ogg")
                self._timer_pasos = self._intervalo_pasos
        else:
            self._timer_pasos = 0
    
    
    def dibujar(
        self,
        pantalla: pygame.Surface,
        camara: pygame.Rect
    ):
        
        if self.moviendose:
            frame = self.sprites_jugador_corriendo[
                self.direccion
            ][self.indice_corriendo]
        else:
            frame = self.sprites_jugador_estatico[
                self.indice_estatico
            ]
        
        pantalla.blit(
            frame,
            (
                self.rect.x - camara.x,
                self.rect.y - camara.y
            )
        )