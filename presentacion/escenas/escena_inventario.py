from __future__ import annotations
from typing import TYPE_CHECKING, List
import pygame
from presentacion.escenas.escena_base import EscenaBase
from infraestructura.texto.fuente import Fuente
from presentacion.ui.componentes.frame import Frame
from presentacion.temas.colores import Paleta

if TYPE_CHECKING:
    from presentacion.juego import Juego


class EscenaInventario(EscenaBase):
    """Inventario estilo Pokémon."""

    def __init__(self, juego: Juego) -> None:
        super().__init__(juego)
        self._init()
        self._crear_frames()

    def _init(self) -> None:
        self.fuente_titulo = Fuente.obtener(24)
        self.fuente_seccion = Fuente.obtener(20)
        self.fuente_item = Fuente.obtener(18)
        self.fuente_detalle = Fuente.obtener(16)
        self.fuente_pista = Fuente.obtener(14)
        self.secciones: List[str] = ["Laptops", "Componentes"]
        self.sec_act = 0
        self.item_act = 0
        self.scroll = 0

    def _crear_frames(self) -> None:
        self.frame_sec: Frame | None = None
        self.frame_items: Frame | None = None
        self.frame_desc: Frame | None = None

    def _obtener_items(self, nombre: str) -> List:
        return getattr(self.juego.jugador.inventario, nombre.lower(), [])

    def _nombre_item(self, item) -> str:
        return getattr(item, 'modelo', getattr(item, 'nombre', item.get('nombre', str(item)) if isinstance(item, dict) else str(item)))

    def _descripcion_item(self, item) -> str:
        attrs = []
        for attr, etiqueta in [('modelo', 'Modelo'), ('marca', 'Marca'), ('tipo', 'Tipo'),
                               ('procesador', 'Procesador'), ('ram', 'RAM'), ('almacenamiento', 'Almacenamiento'),
                               ('grafica', 'Gráfica'), ('capacidad', 'Capacidad'), ('velocidad', 'Velocidad'),
                               ('tipo_componente', 'Tipo de componente')]:
            if hasattr(item, attr):
                attrs.append(f"{etiqueta}: {getattr(item, attr)}")
        return " | ".join(attrs) or str(item)

    def _env_texto(self, texto: str, fuente, ancho: int) -> List[str]:
        if not texto: return []
        pal, lin, act = texto.split(' '), [], []
        esp = fuente.render(" ", False, (255, 255, 255)).get_width()
        for p in pal:
            w = fuente.render(p, False, (255, 255, 255)).get_width()
            a = sum(fuente.render(w_, False, (255, 255, 255)).get_width() for w_ in act) + (esp * len(act) if act else 0)
            if a + w > ancho and act:
                lin.append(' '.join(act))
                act = [p]
            else:
                act.append(p)
        if act: lin.append(' '.join(act))
        return lin

    def manejar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                self._tecla(e.key)

    def _tecla(self, t: int):
        if t == pygame.K_ESCAPE:
            from presentacion.escenas.escena_juego import EscenaJuego
            self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))
        elif t == pygame.K_LEFT: self._camb_sec(-1)
        elif t == pygame.K_RIGHT: self._camb_sec(1)
        elif t == pygame.K_UP: self._mover(-1)
        elif t == pygame.K_DOWN: self._mover(1)
        elif t == pygame.K_a: pass

    def _camb_sec(self, d: int):
        self.sec_act = (self.sec_act + d) % len(self.secciones)
        self.item_act = 0
        self.scroll = 0

    def _mover(self, d: int):
        items = self._obtener_items(self.secciones[self.sec_act])
        if items:
            self.item_act = (self.item_act + d) % len(items)
            self._aj_scroll(items)

    def _aj_scroll(self, items: List):
        if self.item_act < self.scroll: self.scroll = self.item_act
        elif self.item_act >= self.scroll + 12: self.scroll = self.item_act - 11

    def actualizar(self, dt: float) -> None: pass

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill(Paleta.INVENTARIO_FONDO)
        w, h = pantalla.get_size()
        ws = int(w * 0.25)
        wi = w - ws
        hl = int(h * 0.70)
        hd = h - hl
        xs, ys = 0, 0
        xi, yi = ws, 0
        xd, yd = 0, hl
        self._act_frame(self.frame_sec, xs, ys, ws, hl, w, h)
        self._act_frame(self.frame_items, xi, yi, wi, hl, w, h)
        self._act_frame(self.frame_desc, xd, yd, w, hd, w, h)
        if self.frame_sec: self.frame_sec.dibujar(pantalla)
        if self.frame_items: self.frame_items.dibujar(pantalla)
        if self.frame_desc: self.frame_desc.dibujar(pantalla)
        self._dib_sec(pantalla, xs, ys, ws, hl)
        self._dib_items(pantalla, xi, yi, wi, hl)
        self._dib_desc(pantalla, xd, yd, w, hd)

    def _act_frame(self, f: Frame | None, x: int, y: int, w: int, h: int, pw: int, ph: int) -> None:
        if f is None:
            f = Frame(x/pw if pw>0 else 0, y/ph if ph>0 else 0, w, h, "topleft", Paleta.INVENTARIO_PANEL, 0)
            if f == self.frame_sec: self.frame_sec = f
            elif f == self.frame_items: self.frame_items = f
            else: self.frame_desc = f
        else:
            f.rel_x = x/pw if pw>0 else 0
            f.rel_y = y/ph if ph>0 else 0
            f.width = w
            f.height = h

    def _dib_sec(self, p: pygame.Surface, x: int, y: int, w: int, h: int) -> None:
        hp = 32
        for i, sec in enumerate(self.secciones):
            yp = y + i * hp
            if i == self.sec_act:
                s = pygame.Surface((w, hp))
                s.fill(Paleta.INVENTARIO_SELECCION)
                p.blit(s, (x, yp))
                c = Paleta.INVENTARIO_TEXTO_DESTACADO
            else:
                c = Paleta.INVENTARIO_TEXTO
            surf = self.fuente_seccion.render(sec, False, c)
            p.blit(surf, (x + 10, yp + hp//2 - surf.get_height()//2))
            if i < len(self.secciones) - 1:
                pygame.draw.line(p, Paleta.INVENTARIO_BORDE, (x, yp + hp), (x + w, yp + hp), 1)

    def _dib_items(self, p: pygame.Surface, x: int, y: int, w: int, h: int) -> None:
        sec = self.secciones[self.sec_act]
        items = self._obtener_items(sec)
        if not items:
            msg = f"No hay {sec.lower()} en el inventario"
            surf = self.fuente_item.render(msg, False, Paleta.INVENTARIO_TEXTO_PISTA)
            r = surf.get_rect(center=(x + w//2, y + h//2))
            p.blit(surf, r)
            return
        hi = 24
        ini = self.scroll
        fin = min(ini + 12, len(items))
        for idx, i in enumerate(range(ini, fin)):
            it = items[i]
            yi = y + idx * hi
            if i == self.item_act:
                s = pygame.Surface((w, hi))
                s.fill(Paleta.INVENTARIO_SELECCION)
                p.blit(s, (x, yi))
                c = Paleta.INVENTARIO_TEXTO_DESTACADO
                pts = [(x+4, yi+hi//2), (x+8, yi+hi//2-3), (x+8, yi+hi//2+3)]
                pygame.draw.polygon(p, Paleta.INVENTARIO_CURSOR, pts)
                dx = 16
            else:
                c = Paleta.INVENTARIO_TEXTO
                dx = 0
            img_x = x + 10 + dx
            img_y = yi + (hi - 20)//2
            pygame.draw.rect(p, (60, 60, 80), (img_x, img_y, 20, 20))
            pygame.draw.rect(p, (100, 100, 120), (img_x, img_y, 20, 20), 1)
            nom = self._nombre_item(it)
            surf = self.fuente_item.render(nom, False, c)
            p.blit(surf, (img_x + 20 + 10, yi + (hi - surf.get_height())//2))
        if len(items) > 12:
            if self.scroll > 0:
                pts = [(x+w-12, y+6), (x+w-4, y+14), (x+w-20, y+14)]
                pygame.draw.polygon(p, Paleta.INVENTARIO_SCROLL, pts)
            if self.scroll + 12 < len(items):
                pts = [(x+w-20, y+h-14), (x+w-4, y+h-6), (x+w-12, y+h-14)]
                pygame.draw.polygon(p, Paleta.INVENTARIO_SCROLL, pts)

    def _dib_desc(self, p: pygame.Surface, x: int, y: int, w: int, h: int) -> None:
        sec = self.secciones[self.sec_act]
        items = self._obtener_items(sec)
        xt = x + 10
        yt = y + 10
        maxw = w - 20
        inter = self.fuente_detalle.get_height() + 2
        if items and 0 <= self.item_act < len(items):
            it = items[self.item_act]
            desc = self._descripcion_item(it)
            lineas = self._env_texto(desc, self.fuente_detalle, maxw)
            for i, lin in enumerate(lineas[:4]):
                surf = self.fuente_detalle.render(lin, False, Paleta.INVENTARIO_TEXTO_DESCRIPCION)
                p.blit(surf, (xt, yt + i * inter))
            if len(lineas) > 4:
                surf = self.fuente_detalle.render("...", False, Paleta.INVENTARIO_TEXTO_PISTA)
                p.blit(surf, (xt, yt + 4 * inter))
        else:
            surf = self.fuente_detalle.render("Seleccione un ítem para ver los detalles", False, Paleta.INVENTARIO_TEXTO_PISTA)
            p.blit(surf, (xt, yt))