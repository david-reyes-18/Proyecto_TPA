import pygame
from core.rutas import Rutas

ESCALA = 4

FRAME_W = 16
FRAME_H = 32

FPS_IDLE = 4
FPS_RUN = 24

FRAMES_IDLE = 4
FRAMES_POR_DIR = 6

# filas del spritesheet run
DIRS_RUN = {
    "right": 0,
    "up":    1,
    "left":  2,
    "down":  3,
}


class Jugador:
    def __init__(self, x: int, y: int):

        self.ancho = FRAME_W * ESCALA
        self.alto = FRAME_H * ESCALA

        # hitbox solo pies
        hb_h = self.alto // 4

        self.hitbox = pygame.Rect(
            x,
            y + self.alto - hb_h,
            self.ancho,
            hb_h
        )

        self.rect = pygame.Rect(
            x,
            y,
            self.ancho,
            self.alto
        )

        self.velocidad = 100 * ESCALA

        # sprites
        self.frames_idle = self._cortar_idle()
        self.frames_run = self._cortar_run()

        # estado
        self.direccion = "down"
        self.moviendose = False

        # animación
        self.idx_idle = 0
        self.idx_run = 0

        self.t_idle = 0.0
        self.t_run = 0.0

    # ----------------------------------------
    # CARGA SPRITES
    # ----------------------------------------

    def _escalar(self, surf: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(
            surf,
            (self.ancho, self.alto)
        )

    def _cortar_idle(self) -> list[pygame.Surface]:

        sheet = pygame.image.load(
            str(Rutas.imagen("Adam_idle_16x16.png"))
        ).convert_alpha()

        frames = []

        for i in range(FRAMES_IDLE):
            frame = sheet.subsurface(
                (i * FRAME_W, 0, FRAME_W, FRAME_H)
            )

            frames.append(
                self._escalar(frame)
            )

        return frames

    def _cortar_run(self) -> dict[str, list[pygame.Surface]]:

        sheet = pygame.image.load(
            str(Rutas.imagen("Adam_run_16x16.png"))
        ).convert_alpha()

        animaciones = {}

        for idx_dir, direccion in enumerate(DIRS_RUN):

            frames = []

            for i in range(FRAMES_POR_DIR):

                frame_index = idx_dir * FRAMES_POR_DIR + i

                frame = sheet.subsurface(
                    (
                        frame_index * FRAME_W,
                        0,
                        FRAME_W,
                        FRAME_H
                    )
                )

                frames.append(
                    self._escalar(frame)
                )

            animaciones[direccion] = frames

        return animaciones

    # ----------------------------------------
    # UPDATE
    # ----------------------------------------

    def actualizar(
        self,
        dt: float,
        dx: int,
        dy: int,
        obstaculos: list[pygame.Rect]
    ):

        self.moviendose = dx != 0 or dy != 0

        # dirección visual
        if dx < 0:
            self.direccion = "left"
        elif dx > 0:
            self.direccion = "right"
        elif dy < 0:
            self.direccion = "up"
        elif dy > 0:
            self.direccion = "down"

        # movimiento eje x
        self.hitbox.x += dx

        for obs in obstaculos:
            if self.hitbox.colliderect(obs):
                if dx > 0:
                    self.hitbox.right = obs.left
                elif dx < 0:
                    self.hitbox.left = obs.right

        # movimiento eje y
        self.hitbox.y += dy

        for obs in obstaculos:
            if self.hitbox.colliderect(obs):
                if dy > 0:
                    self.hitbox.bottom = obs.top
                elif dy < 0:
                    self.hitbox.top = obs.bottom

        # sincronizar sprite con hitbox
        self.rect.midbottom = self.hitbox.midbottom

        # idle
        self.t_idle += dt

        if self.t_idle >= 1 / FPS_IDLE:
            self.t_idle = 0
            self.idx_idle = (
                self.idx_idle + 1
            ) % FRAMES_IDLE

        # run
        if self.moviendose:

            self.t_run += dt

            if self.t_run >= 1 / FPS_RUN:
                self.t_run = 0
                self.idx_run = (
                    self.idx_run + 1
                ) % FRAMES_POR_DIR
        else:
            self.idx_run = 0
            self.t_run = 0

    # ----------------------------------------
    # DIBUJAR
    # ----------------------------------------

    def dibujar(
        self,
        pantalla: pygame.Surface,
        camara: pygame.Rect
    ):

        if self.moviendose:
            frame = self.frames_run[
                self.direccion
            ][self.idx_run]
        else:
            frame = self.frames_idle[
                self.idx_idle
            ]

        pantalla.blit(
            frame,
            (
                self.rect.x - camara.x,
                self.rect.y - camara.y
            )
        )