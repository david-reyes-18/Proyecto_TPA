from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from core.config import *
from ui.label import Label
from ui.boton import Boton
from escenas.escena_base import EscenaBase
from escenas.menu_principal import MenuPrincipal

if TYPE_CHECKING:
    from core.juego import Juego


class EscenaConfig(EscenaBase):
    def __init__(self, juego: Juego):
        super().__init__(juego)

        self.volumen_musica  = 0.5
        self.volumen_efectos = 0.7
        self.resolucion_idx  = 2

        for i, (w, h, _) in enumerate(RESOLUCIONES):
            if w == juego.pantalla.get_width() and h == juego.pantalla.get_height():
                self.resolucion_idx = i
                break

        self._drag_musica  = False
        self._drag_efectos = False
        self.slider_ancho  = 320
        self.slider_alto   = 12
        self.knob_r        = 10

        self.boton_res_prev = Boton(
            text="<", rel_x=0.34, rel_y=0.62, width=44, height=44,
            command=self._res_ant, font_size=26,
            bg_color=(60,60,90), hover_color=(100,100,160)
        )
        self.boton_res_next = Boton(
            text=">", rel_x=0.66, rel_y=0.62, width=44, height=44,
            command=self._res_sig, font_size=26,
            bg_color=(60,60,90), hover_color=(100,100,160)
        )
        self.boton_aplicar = Boton(
            text="APLICAR RESOLUCION", rel_x=0.5, rel_y=0.72, width=280, height=46,
            command=self._aplicar_res, font_size=18,
            bg_color=(50,120,80), hover_color=(70,180,110)
        )
        self.boton_volver = Boton(
            text="VOLVER", rel_x=0.5, rel_y=0.87, width=220, height=52,
            command=self._volver, font_size=22,
            bg_color=(80,40,40), hover_color=(140,60,60)
        )
        self.botones = [self.boton_res_prev, self.boton_res_next,
                        self.boton_aplicar, self.boton_volver]

        self._msg_timer = 0.0
        self._msg_texto = ""

    def _res_ant(self):
        self.resolucion_idx = (self.resolucion_idx - 1) % len(RESOLUCIONES)

    def _res_sig(self):
        self.resolucion_idx = (self.resolucion_idx + 1) % len(RESOLUCIONES)

    def _aplicar_res(self):
        w, h, label = RESOLUCIONES[self.resolucion_idx]
        self.juego.pantalla = pygame.display.set_mode((w, h))
        import core.config as cfg
        cfg.ANCHO = w
        cfg.ALTO  = h
        self._msg_texto = f"Resolucion aplicada: {label}"
        self._msg_timer = 2.5

    def _volver(self):
        self.juego.manejador_escenas.cambiar_escena(MenuPrincipal(self.juego))

    def _slider_rect(self, cx, cy):
        return pygame.Rect(cx - self.slider_ancho // 2,
                           cy - self.slider_alto // 2,
                        self.slider_ancho, self.slider_alto)

    def _valor_desde_x(self, mx, cx):
        left = cx - self.slider_ancho // 2
        return max(0.0, min(1.0, (mx - left) / self.slider_ancho))

    def _knob_x(self, valor, cx):
        return int(cx - self.slider_ancho // 2 + valor * self.slider_ancho)

    def manejar_eventos(self, eventos):
        pantalla = self.juego.pantalla
        pw, ph   = pantalla.get_size()
        cx       = pw // 2
        cy_mus   = int(ph * 0.40)
        cy_efx   = int(ph * 0.54)

        for b in self.botones:
            b.actualizar(eventos, pantalla)

        for ev in eventos:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                if self._slider_rect(cx, cy_mus).inflate(0, 28).collidepoint(mx, my):
                    self._drag_musica  = True
                    self.volumen_musica = self._valor_desde_x(mx, cx)
                if self._slider_rect(cx, cy_efx).inflate(0, 28).collidepoint(mx, my):
                    self._drag_efectos  = True
                    self.volumen_efectos = self._valor_desde_x(mx, cx)

            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self._drag_musica  = False
                self._drag_efectos = False

            elif ev.type == pygame.MOUSEMOTION:
                mx, my = ev.pos
                if self._drag_musica:
                    self.volumen_musica  = self._valor_desde_x(mx, cx)
                if self._drag_efectos:
                    self.volumen_efectos = self._valor_desde_x(mx, cx)

        if pygame.mixer and pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self.volumen_musica)

    def actualizar(self, dt):
        if self._msg_timer > 0:
            self._msg_timer -= dt

    def dibujar(self, pantalla):
        pw, ph = pantalla.get_size()
        cx     = pw // 2

        # Fondo degradado
        for y in range(ph):
            t = y / ph
            pygame.draw.line(pantalla,
                             (int(18+t*10), int(18+t*8), int(40+t*20)),
                             (0, y), (pw, y))

        # Barras laterales decorativas
        bar = pygame.Surface((6, ph), pygame.SRCALPHA)
        bar.fill((120, 100, 220, 80))
        pantalla.blit(bar, (30, 0))
        pantalla.blit(bar, (pw - 36, 0))

        def font(size):
            try:
                from core.fuente import Fuente
                return Fuente.obtener(size)
            except Exception:
                return pygame.font.SysFont("consolas", size)

        # Título
        t_surf = font(46).render("CONFIGURACION", False, (200, 180, 255))
        pantalla.blit(t_surf, t_surf.get_rect(center=(cx, int(ph * 0.12))))
        pygame.draw.line(pantalla, (120, 100, 200),
                         (cx-160, int(ph*0.19)), (cx+160, int(ph*0.19)), 2)

        # Audio
        a_surf = font(20).render("AUDIO", False, (160, 200, 255))
        pantalla.blit(a_surf, a_surf.get_rect(center=(cx, int(ph * 0.28))))

        self._dibujar_slider(pantalla, cx, int(ph*0.40),
                             self.volumen_musica, "Musica",
                             font(18), (100, 180, 255))
        self._dibujar_slider(pantalla, cx, int(ph*0.54),
                             self.volumen_efectos, "Efectos",
                             font(18), (180, 120, 255))

        # Resolución
        r_surf = font(20).render("RESOLUCION DE PANTALLA", False, (160, 200, 255))
        pantalla.blit(r_surf, r_surf.get_rect(center=(cx, int(ph * 0.57))))

        _, _, nombre_res = RESOLUCIONES[self.resolucion_idx]
        n_surf = font(18).render(nombre_res, False, (240, 240, 255))
        pantalla.blit(n_surf, n_surf.get_rect(center=(cx, int(ph * 0.625))))

        for b in self.botones:
            b.dibujar(pantalla)

        if self._msg_timer > 0:
            alpha = min(255, int(self._msg_timer * 200))
            ms = font(16).render(self._msg_texto, False, (100, 255, 160))
            ms.set_alpha(alpha)
            pantalla.blit(ms, ms.get_rect(center=(cx, int(ph * 0.80))))

    def _dibujar_slider(self, pantalla, cx, cy, valor, etiqueta, font, color_fill):
        lbl = font.render(etiqueta, False, (200, 200, 220))
        pantalla.blit(lbl, lbl.get_rect(midright=(cx - self.slider_ancho//2 - 14, cy)))

        track = self._slider_rect(cx, cy)
        pygame.draw.rect(pantalla, (50, 50, 70), track, border_radius=6)

        fill = pygame.Rect(track.x, track.y, int(valor * self.slider_ancho), self.slider_alto)
        pygame.draw.rect(pantalla, color_fill, fill, border_radius=6)

        kx = self._knob_x(valor, cx)
        pygame.draw.circle(pantalla, (255, 255, 255), (kx, cy), self.knob_r)
        pygame.draw.circle(pantalla, color_fill,      (kx, cy), self.knob_r - 3)

        pct = font.render(f"{int(valor*100)}%", False, (200, 200, 220))
        pantalla.blit(pct, pct.get_rect(midleft=(cx + self.slider_ancho//2 + 14, cy)))