from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from escenas.escena_base import EscenaBase
from ui.frame import Frame
from ui.label import Label
from core.fuente import Fuente
from core.rutas import Rutas
from sistema.trabajo import EmailUsuario, Trabajo
from sistema.inventario import Inventario
import os
from dispositivos.laptop import Laptop

if TYPE_CHECKING:
    from core.juego import Juego

# Posiciones relativas medidas sobre la imagen fondo_email.png (1408x768)
# Todas en rango 0.0-1.0 para que escalen a cualquier resolución
_BARRA_TITULO = dict(rel_x=0.05, rel_y=0.072, width=0.9, height=0.078)
_TABLA = dict(rel_x=0.05, rel_y=0.254, width=0.9, height=0.4)
_COL_X = dict(remitente=0.0, asunto=0.2, fecha=0.87, fin=1.0)

# Constants for accept button position (relative to fondo_email.png)
_ACCEPT_BUTTON = dict(rel_x=0.155, rel_y=0.78, width=0.700, height=0.08)


class EscenaCorreo(EscenaBase):

    def __init__(self, juego: Juego) -> None:
        super().__init__(juego)
        
        self.email_usuario = EmailUsuario()
        self.inventario = juego.jugador.inventario  # Use the player's inventory
        self.seleccionado = 0
        self.correo_abierto: dict | None = None
        self.last_accept_message = ""
        self.accept_message_timer = 0
        
        # Animation state for accepted work
        self.accept_animation_timer = 0
        self.accept_animation_laptop = None
        self.accept_animation_scale = 1.0
        self.accept_animation_direction = 1  # 1 for growing, -1 for shrinking
        
        sw, sh = juego.pantalla.get_size()
        raw = pygame.image.load(str(Rutas.imagen("fondo_email.png"))).convert()
        self.fondo = pygame.transform.scale(raw, (sw, sh))
        
        self._fuente_fila = Fuente.obtener(10)
        self._fuente_meta = Fuente.obtener(10)
        self._fuente_cuerpo = Fuente.obtener(10)
        self._fuente_titulo = Fuente.obtener(16)  # for accept button label
        
        # Load assets for animation
        self._load_assets()
        
        self._construir_ui()
    
    
    def _load_assets(self):
        """Load assets for laptop icon and sound."""
        try:
            # Load laptop icon (use the transparent computer image)
            icon_path = str(Rutas.imagen("tiles_escenario/computador-transparente.png"))
            self.laptop_icon_orig = pygame.image.load(icon_path).convert_alpha()
            # Scale to a reasonable size for icon (e.g., 64x64)
            self.laptop_icon = pygame.transform.scale(self.laptop_icon_orig, (64, 64))
        except Exception as e:
            print(f"Warning: Could not load laptop icon: {e}")
            self.laptop_icon_orig = None
            self.laptop_icon = None

        try:
            # Load accept sound
            sound_path = str(Rutas.sonido("click.ogg"))  # Assuming we have an audio folder
            self.accept_sound = pygame.mixer.Sound(sound_path)
            self.accept_sound.set_volume(0.5)
        except Exception as e:
            print(f"Warning: Could not load accept sound: {e}")
            self.accept_sound = None

    def _construir_ui(self) -> None:
        # Barra de título azul (muestra asunto del correo abierto)
        self.barra_titulo = Frame(
            **_BARRA_TITULO,
            bg_color=(0, 0, 0),
            alpha=0,
        )
        self._label_titulo = Label(
            text="", font_size=16, text_color=(255, 255, 255),
            rel_x=0.02, rel_y=0.5, anchor="midleft",
        )
        self.barra_titulo.add(self._label_titulo)

        # Hint de controles (parte inferior)
        self.frame_hint = Frame(
            rel_x=0.155, rel_y=0.87,
            width=0.700, height=0.06,
            bg_color=(0, 0, 0), alpha=0,
        ).add(Label(
            text="[UP/DOWN] Navegar   [E] Abrir Correo   [ESC] Volver al juego",
            font_size=14, text_color=(80, 80, 120),
            rel_x=0.0, rel_y=0.5, anchor="midleft",
        ))

        self.frame_hint_correo = Frame(
            rel_x=0.155, rel_y=0.87,
            width=0.700, height=0.06,
            bg_color=(0, 0, 0), alpha=0,
        ).add(Label(
            text="[ESC] Volver a bandeja",
            font_size=15, text_color=(80, 80, 120),
            rel_x=0.0, rel_y=0.5, anchor="midleft",
        ))

    # ── Helpers ──────────────────────────────────────────────────────────

    def _ir_a_juego(self) -> None:
        from escenas.escena_juego import EscenaJuego
        self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))

    def _abrir_correo(self, idx: int) -> None:
        self.correo_abierto = self.email_usuario.bandeja_entrada[idx]
        self.email_usuario.marcar_como_leido(idx)
        self._label_titulo.text = self.correo_abierto["asunto"]

    def _tabla_rect(self, pantalla: pygame.Surface) -> pygame.Rect:
        return self.frame_tabla_proxy.get_rect(pantalla) if hasattr(self, "frame_tabla_proxy") \
               else Frame(**_TABLA, bg_color=(0,0,0), alpha=0).get_rect(pantalla)

    # ── Ciclo de vida ────────────────────────────────────────────────────

    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        for evento in eventos:
            if evento.type != pygame.KEYDOWN:
                continue
            if self.correo_abierto is None:
                if evento.key == pygame.K_ESCAPE:
                    self._ir_a_juego()
                elif evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                    self.seleccionado = (self.seleccionado + 1) % len(self.email_usuario.bandeja_entrada)
                elif evento.key == pygame.K_w or evento.key == pygame.K_UP:
                    self.seleccionado = (self.seleccionado - 1) % len(self.email_usuario.bandeja_entrada)
                elif evento.key == pygame.K_e:
                    self._abrir_correo(self.seleccionado)
            else:
                if evento.key == pygame.K_ESCAPE:
                    self.correo_abierto = None
                elif evento.key == pygame.K_e:
                    # Aceptar el trabajo del correo abierto
                    trabajo = self.email_usuario.get_trabajo_por_indice(self.seleccionado)
                    if trabajo and not trabajo.aceptado:
                        laptop_trabajo = trabajo.aceptar(self.juego)
                        if laptop_trabajo:
                            self.inventario.agregar_laptop(laptop_trabajo)
                            self.juego.jugador.dinero += trabajo.recompensa_dinero
                            self.juego.jugador.agregar_experiencia(trabajo.recompensa_experiencia)
                            trabajo.completar()
                            # Trigger animation and sound
                            self._trigger_accept_animation(laptop_trabajo, trabajo.recompensa_dinero, trabajo.recompensa_experiencia)
                            print(f"Trabajo aceptado! Recibiste: ${trabajo.recompensa_dinero} y {trabajo.recompensa_experiencia} XP")
                            print(f"Laptop agregada al inventario: {laptop_trabajo.modelo}")

    def _trigger_accept_animation(self, laptop: Laptop, dinero: int, xp: int) -> None:
        """Start the acceptance animation and set message."""
        self.accept_animation_laptop = laptop
        self.accept_animation_timer = 90  # 1.5 seconds at 60 FPS
        self.accept_animation_scale = 1.0
        self.accept_animation_direction = 1
        # Set message
        self.last_accept_message = f"Trabajo aceptado! +${dinero} +{xp} XP"
        self.accept_message_timer = 180  # 3 seconds for message
        # Play sound
        if self.accept_sound:
            self.accept_sound.play()

    def actualizar(self, dt: float) -> None:
        # Update animation
        if self.accept_animation_timer > 0:
            self.accept_animation_timer -= 1
            # Pulse animation: scale from 1.0 to 1.2 and back
            if self.accept_animation_direction == 1:
                self.accept_animation_scale += 0.02
                if self.accept_animation_scale >= 1.2:
                    self.accept_animation_direction = -1
            else:
                self.accept_animation_scale -= 0.02
                if self.accept_animation_scale <= 1.0:
                    self.accept_animation_direction = 1
                    # Optionally reset when shrinking back to 1.0
        # Update message timer
        if self.accept_message_timer > 0:
            self.accept_message_timer -= 1

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.blit(self.fondo, (0, 0))

        # Frame proxy para calcular el rect de la tabla
        frame_tabla = Frame(**_TABLA, bg_color=(0, 0, 0), alpha=0)
        tabla_rect = frame_tabla.get_rect(pantalla)

        if self.correo_abierto is None:
            self._dibujar_bandeja(pantalla, tabla_rect)
            self.frame_hint.dibujar(pantalla)
            # Draw acceptance message if active (shown in bandeja view)
            if self.accept_message_timer > 0:
                self._dibujar_mensaje_aceptacion(pantalla)
        else:
            self.barra_titulo.dibujar(pantalla)
            self._dibujar_cuerpo(pantalla, tabla_rect)
            self.frame_hint_correo.dibujar(pantalla)
            # Draw acceptance animation if active (shown when email is open)
            if self.accept_animation_timer > 0 and self.accept_animation_laptop:
                self._dibujar_animacion_aceptacion(pantalla)
            # Draw acceptance message if active (shown when email is open)
            if self.accept_message_timer > 0:
                self._dibujar_mensaje_aceptacion(pantalla)

    # ── Vista: Bandeja ───────────────────────────────────────────────────

    def _dibujar_bandeja(self, pantalla: pygame.Surface, tabla: pygame.Rect) -> None:
        fila_h = tabla.height // max(len(self.email_usuario.bandeja_entrada) + 1, 5)
        pad = 8

        # Anchos de columna en px (proporcional al ancho de tabla)
        x_asu = tabla.x + int(tabla.width * _COL_X["asunto"])
        x_fec = tabla.x + int(tabla.width * _COL_X["fecha"])

        for i, correo in enumerate(self.email_usuario.bandeja_entrada):
            fy = tabla.y + i * fila_h

            # Selección semitransparente usando Frame
            if i == self.seleccionado:
                sel = Frame(
                    rel_x=tabla.x / pantalla.get_width(),
                    rel_y=fy / pantalla.get_height(),
                    width=tabla.width / pantalla.get_width(),
                    height=fila_h / pantalla.get_height(),
                    bg_color=(100, 160, 255),
                    alpha=90,
                )
                sel.dibujar(pantalla)

            # Punto de no leído
            color_texto = (0, 0, 120) if not correo["leido"] else (30, 30, 70)
            if not correo["leido"]:
                pygame.draw.circle(
                    pantalla, (0, 80, 200),
                    (tabla.x + pad + 4, fy + fila_h // 2), 4
                )

            # Remitente — usando Label posicionado manualmente sobre pantalla
            self._blit_texto(pantalla, correo["de"], self._fuente_fila, color_texto, tabla.x + pad + 12, fy, fila_h)
            self._blit_texto(pantalla, correo["asunto"], self._fuente_fila, color_texto, x_asu + pad, fy, fila_h)
            self._blit_texto(pantalla, correo["fecha"], self._fuente_meta, (60, 60, 110), x_fec + pad, fy, fila_h)

            # Línea separadora
            pygame.draw.line(pantalla, (180, 185, 205),
                             (tabla.x, fy + fila_h - 1),
                             (tabla.right, fy + fila_h - 1), 1)

    # ── Vista: Correo abierto ────────────────────────────────────────────

    def _dibujar_cuerpo(self, pantalla: pygame.Surface, tabla: pygame.Rect) -> None:
        c = self.correo_abierto
        px = tabla.x + 10
        py = tabla.y + 6
        lh = self._fuente_cuerpo.get_height() + 5

        # Meta con Labels posicionados en la zona de la tabla
        for texto, color in [
            (f"De:    {c['de']}", (60, 60, 130)),
            (f"Fecha: {c['fecha']}", (60, 60, 130)),
        ]:
            s = self._fuente_meta.render(texto, False, color)
            pantalla.blit(s, (px, py))
            py += s.get_height() + 3

        pygame.draw.line(pantalla, (160, 165, 200),
                         (tabla.x, py + 2), (tabla.right, py + 2), 1)
        py += 12

        # Cuerpo del mensaje
        for linea in c["cuerpo"]:
            if py + lh > tabla.bottom:
                break
            if linea == "":
                py += lh // 2
                continue
            s = self._fuente_cuerpo.render(linea, False, (20, 20, 60))
            pantalla.blit(s, (px, py))
            py += lh

        # Draw accept button prompt at bottom of email view
        self._dibujar_prompt_aceptar(pantalla, tabla)

    # ── Vista: Correo abierto - Prompt de aceptar ───────────────────────

    def _dibujar_prompt_aceptar(self, pantalla: pygame.Surface, tabla: pygame.Rect) -> None:
        """Draws the accept button prompt at the bottom of the email view."""
        texto = "[A] Aceptar Trabajo"
        surf = self._fuente_titulo.render(texto, False, (255, 255, 255))
        # Position at bottom center of the email body area
        x = tabla.x + (tabla.width - surf.get_width()) // 2
        y = tabla.bottom - surf.get_height() - 10
        # Background for readability
        bg_surf = pygame.Surface((surf.get_width() + 20, surf.get_height() + 10), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))
        pantalla.blit(bg_surf, (x - 10, y - 5))
        pantalla.blit(surf, (x, y))

    # ── Animación de aceptación ────────────────────────────────────────

    def _dibujar_animacion_aceptacion(self, pantalla: pygame.Surface) -> None:
        """Draws the laptop icon with pulsating animation."""
        if not self.laptop_icon or not self.accept_animation_laptop:
            return

        # Calculate current scale
        scale = self.accept_animation_scale
        # Scale the icon
        width = int(self.laptop_icon.get_width() * scale)
        height = int(self.laptop_icon.get_height() * scale)
        laptop_surf = pygame.transform.scale(self.laptop_icon, (width, height))

        # Position at center of screen
        x = pantalla.get_width() // 2 - width // 2
        y = pantalla.get_height() // 2 - height // 2

        # Draw a subtle background circle
        radius = max(width, height) // 2 + 10
        pygame.draw.circle(pantalla, (20, 20, 40, 180),
                           (pantalla.get_width() // 2, pantalla.get_height() // 2), radius)

        # Draw the laptop icon
        pantalla.blit(laptop_surf, (x, y))

        # Draw laptop model name below icon
        modelo_texto = self.accept_animation_laptop.modelo
        surf_modelo = self._fuente_meta.render(modelo_texto, False, (255, 255, 255))
        modelo_x = pantalla.get_width() // 2 - surf_modelo.get_width() // 2
        modelo_y = y + height + 10
        pantalla.blit(surf_modelo, (modelo_x, modelo_y))

    # ── Util ─────────────────────────────────────────────────────────────

    def _blit_texto(
        self, pantalla: pygame.Surface, texto: str,
        fuente: pygame.font.Font, color: tuple,
        x: int, fila_y: int, fila_h: int,
    ) -> None:
        surf = fuente.render(texto, False, color)
        pantalla.blit(surf, (x, fila_y + (fila_h - surf.get_height()) // 2))

    def _dibujar_mensaje_aceptacion(self, pantalla: pygame.Surface) -> None:
        """Muestra un mensaje temporal cuando se acepta un trabajo."""
        if not self.last_accept_message:
            return

        surf = self._fuente_meta.render(self.last_accept_message, False, (255, 255, 0))
        # Position at bottom center
        x = pantalla.get_width() // 2 - surf.get_width() // 2
        y = pantalla.get_height() - 50
        # Background for readability
        bg_surf = pygame.Surface((surf.get_width() + 20, surf.get_height() + 10), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))
        pantalla.blit(bg_surf, (x - 10, y - 5))
        pantalla.blit(surf, (x, y))