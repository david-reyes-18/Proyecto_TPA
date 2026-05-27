import pygame
from core.rutas import Rutas

ESCALA          = 4
FRAME_W         = 16
FRAME_H         = 32
FPS_IDLE        = 5
FPS_RUN         = 10
FRAMES_IDLE     = 4
FRAMES_POR_DIR  = 6

# Orden confirmado inspeccionando frame a frame el spritesheet
DIRS_RUN = {
    "right":  0,
    "up":    1,
    "left":  2,
    "down": 3,
}


class Jugador:
    def __init__(self, x: int, y: int):
        self.ancho = FRAME_W * ESCALA   # 48 px
        self.alto  = FRAME_H * ESCALA   # 96 px

        # Hitbox: franja inferior (pies) para colisiones con el mapa
        hb_h = self.alto // 4
        self.hitbox = pygame.Rect(x, y + self.alto - hb_h, self.ancho, hb_h)
        self.rect   = pygame.Rect(x, y, self.ancho, self.alto)

        self.velocidad = 100 * ESCALA

        # Sprites
        self.frames_idle = self._cortar_idle()
        self.frames_run  = self._cortar_run()

        # Estado
        self.direccion  = "down"
        self.moviendose = False

        # Animación — índice y acumulador de tiempo separados por estado
        self.idx_idle  = 0
        self.idx_run   = 0
        self.t_idle    = 0.0
        self.t_run     = 0.0

    # ------------------------------------------------------------------
    # Carga
    # ------------------------------------------------------------------

    def _escalar(self, surf: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(surf, (self.ancho, self.alto))

    def _cortar_idle(self) -> list[pygame.Surface]:
        sheet = pygame.image.load(
            str(Rutas.imagen("Adam_idle_16x16.png"))
        ).convert_alpha()
        return [
            self._escalar(sheet.subsurface((i * FRAME_W, 0, FRAME_W, FRAME_H)))
            for i in range(FRAMES_IDLE)
        ]

    def _cortar_run(self) -> dict[str, list[pygame.Surface]]:
        sheet = pygame.image.load(
            str(Rutas.imagen("Adam_run_16x16.png"))
        ).convert_alpha()
        resultado = {}
        for nombre, idx in DIRS_RUN.items():
            resultado[nombre] = [
                self._escalar(sheet.subsurface(
                    ((idx * FRAMES_POR_DIR + f) * FRAME_W, 0, FRAME_W, FRAME_H)
                ))
                for f in range(FRAMES_POR_DIR)
            ]
        return resultado

    # ------------------------------------------------------------------
    # Actualizar
    # ------------------------------------------------------------------

    def actualizar(self, dt: float, dx: int, dy: int,
                   obstaculos: list[pygame.Rect]):

        self.moviendose = dx != 0 or dy != 0

        # Dirección según input (horizontal tiene prioridad en diagonal)
        if   dx < 0: self.direccion = "left"
        elif dx > 0: self.direccion = "right"
        elif dy < 0: self.direccion = "up"
        elif dy > 0: self.direccion = "down"

        # Movimiento + colisiones eje X
        self.hitbox.x += dx
        for obs in obstaculos:
            if self.hitbox.colliderect(obs):
                if dx > 0: self.hitbox.right = obs.left
                else:      self.hitbox.left  = obs.right

        # Movimiento + colisiones eje Y
        self.hitbox.y += dy
        for obs in obstaculos:
            if self.hitbox.colliderect(obs):
                if dy > 0: self.hitbox.bottom = obs.top
                else:      self.hitbox.top    = obs.bottom

        # Rect visual alineado con hitbox (pies)
        self.rect.midbottom = self.hitbox.midbottom

        # Animación idle  (siempre avanza, independiente del run)
        self.t_idle += dt
        if self.t_idle >= 1.0 / FPS_IDLE:
            self.t_idle -= 1.0 / FPS_IDLE
            self.idx_idle = (self.idx_idle + 1) % FRAMES_IDLE

        # Animación run  (solo avanza si se está moviendo)
        if self.moviendose:
            self.t_run += dt
            if self.t_run >= 1.0 / FPS_RUN:
                self.t_run -= 1.0 / FPS_RUN
                self.idx_run = (self.idx_run + 1) % FRAMES_POR_DIR
        else:
            # Al detenerse, resetear run para que empiece desde frame 0
            self.idx_run = 0
            self.t_run   = 0.0

    # ------------------------------------------------------------------
    # Dibujar
    # ------------------------------------------------------------------

    def dibujar(self, pantalla: pygame.Surface, camara: pygame.Rect):
        if self.moviendose:
            frame = self.frames_run[self.direccion][self.idx_run]
        else:
            frame = self.frames_idle[self.idx_idle]
        pantalla.blit(frame, (self.rect.x - camara.x, self.rect.y - camara.y))