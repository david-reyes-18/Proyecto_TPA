from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from presentacion.escenas.escena_base import EscenaBase
from presentacion.ui.componentes.frame import Frame
from presentacion.ui.componentes.label import Label
from infraestructura.texto.fuente import Fuente
from infraestructura.recursos.rutas import Rutas
from sistema.trabajo import EmailUsuario, Trabajo
from dominio.entidades.jugador.inventario import Inventario
from dominio.entidades.dispositivos.laptop import Laptop


if TYPE_CHECKING:
    from presentacion.juego import Juego


class EscenaCorreo(EscenaBase):
    """Escada que muestra el correo electrónico del jugador."""

    def __init__(self, juego: Juego) -> None:
        super().__init__(juego)

        # Estado de la escena
        self.email_usuario = EmailUsuario()
        self.inventario = juego.jugador.inventario
        self.seleccionado = 0
        self.correo_abierto: dict | None = None

        # Mensajes y animaciones temporales
        self.mensaje_aceptacion = ""
        self.temporizador_mensaje = 0
        self.animacion_laptop = None
        self.temporizador_animacion = 0
        self.escala_animacion = 1.0

        # Cargar recursos visuales
        self._cargar_recursos()
        self._configurar_fondo()
        self._configurar_fuentes()
        self._construir_elementos_ui()

    def _cargar_recursos(self) -> None:
        """Carga iconos y sonidos necesarios."""
        try:
            self.icono_laptop = pygame.transform.scale(
                pygame.image.load(str(Rutas.imagen("tiles_escenario/computador-transparente.png"))).convert_alpha(),
                (64, 64)
            )
        except Exception:
            self.icono_laptop = None
            print("Advertencia: No se pudo cargar el icono de laptop")

        try:
            self.sonido_aceptar = pygame.mixer.Sound(str(Rutas.sonido("click.ogg")))
            self.sonido_aceptar.set_volume(0.5)
        except Exception:
            self.sonido_aceptar = None
            print("Advertencia: No se pudo cargar el sonido de aceptación")

    def _configurar_fondo(self) -> None:
        """Configura el fondo de la escena."""
        sw, sh = self.juego.pantalla.get_size()
        self.fondo = pygame.transform.scale(
            pygame.image.load(str(Rutas.imagen("fondo_email.png"))).convert(),
            (sw, sh)
        )

    def _configurar_fuentes(self) -> None:
        """Configura las fuentes utilizadas."""
        self.fuente_fila = Fuente.obtener(10)
        self.fuente_meta = Fuente.obtener(10)
        self.fuente_cuerpo = Fuente.obtener(10)
        self.fuente_titulo = Fuente.obtener(16)

    def _construir_elementos_ui(self) -> None:
        """Construye los elementos de la interfaz de usuario."""
        # Barra de título
        self.barra_titulo = Frame(0.05, 0.072, 0.9, 0.078)
        self.label_titulo = Label("", 16, (255, 255, 255), 0.02, 0.5, "midleft")
        self.barra_titulo.add(self.label_titulo)

        # Pistas de control
        self.pista_normal = Frame(
            0.155, 0.87, 0.7, 0.06, bg_color=(0,0,0), alpha=0
        ).add(Label(
            "[↑/↓] Navegar   [E] Abrir   [ESC] Salir",
            14, (80, 80, 120), 0.0, 0.5, "midleft"
        ))

        self.pista_correo = Frame(
            0.155, 0.87, 0.7, 0.06, bg_color=(0,0,0), alpha=0
        ).add(Label(
            "[ESC] Bandeja de entrada",
            15, (80, 80, 120), 0.0, 0.5, "midleft"
        ))

    # --- Navegación ---

    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        """Procesa los eventos de entrada."""
        for evento in eventos:
            if evento.type != pygame.KEYDOWN:
                continue

            if self.correo_abierto is None:
                self._manejar_eventos_bandeja(evento)
            else:
                self._manejar_eventos_correo(evento)

    def _manejar_eventos_bandeja(self, evento: pygame.event.Event) -> None:
        """Maneja eventos cuando se muestra la bandeja."""
        if evento.key == pygame.K_ESCAPE:
            self._volver_al_juego()
        elif evento.key in (pygame.K_s, pygame.K_DOWN):
            self.seleccionado = (self.seleccionado + 1) % len(self.email_usuario.bandeja_entrada)
        elif evento.key in (pygame.K_w, pygame.K_UP):
            self.seleccionado = (self.seleccionado - 1) % len(self.email_usuario.bandeja_entrada)
        elif evento.key == pygame.K_e:
            self._abrir_correo(self.seleccionado)

    def _manejar_eventos_correo(self, evento: pygame.event.Event) -> None:
        """Maneja eventos cuando se muestra un correo abierto."""
        if evento.key == pygame.K_ESCAPE:
            self.correo_abierto = None
        elif evento.key == pygame.K_e:
            self._procesar_aceptacion_trabajo()

    def _volver_al_juego(self) -> None:
        """Regresa a la escena del juego."""
        from presentacion.escenas.escena_juego import EscenaJuego
        self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))

    def _abrir_correo(self, indice: int) -> None:
        """Abre el correo en el índice especificado."""
        self.correo_abierto = self.email_usuario.bandeja_entrada[indice]
        self.email_usuario.marcar_como_leido(indice)
        self.label_titulo.texto = self.correo_abierto["asunto"]

    def _procesar_aceptacion_trabajo(self) -> None:
        """Procesa la aceptación de un trabajo desde el correo abierto."""
        trabajo = self.email_usuario.get_trabajo_por_indice(self.seleccionado)
        if not trabajo or trabajo.aceptado:
            return

        laptop = trabajo.aceptar(self.juego)
        if laptop:
            self.inventario.agregar_laptop(laptop)
            self.juego.jugador.dinero += trabajo.recompensa_dinero
            self.juego.jugador.agregar_experiencia(trabajo.recompensa_experiencia)
            trabajo.completar()

            # Iniciar efectos visuales y auditivos
            self._iniciar_animacion_aceptacion(laptop, trabajo.recompensa_dinero, trabajo.recompensa_experiencia)
            if self.sonido_aceptar:
                self.sonido_aceptar.play()

    def _iniciar_animacion_aceptacion(self, laptop: Laptop, dinero: int, xp: int) -> None:
        """Inicia la animación de aceptación y establece el mensaje."""
        self.animacion_laptop = laptop
        self.temporizador_animacion = 90  # 1.5 segundos a 60 FPS
        self.escala_animacion = 1.0
        self.mensaje_aceptacion = f"¡Trabajo aceptado! +${dinero} +{xp} XP"
        self.temporizador_mensaje = 180  # 3 segundos

    # --- Actualización y renderizado ---

    def actualizar(self, dt: float) -> None:
        """Actualiza el estado de la escena."""
        self._actualizar_animacion()
        self._actualizar_temporizadores()

    def _actualizar_animacion(self) -> None:
        """Actualiza la animación de pulsación."""
        if self.temporizador_animacion <= 0:
            return

        self.temporizador_animacion -= 1

        # Animación de pulso: escala de 1.0 a 1.2 y vuelta
        if self.escala_animacion < 1.2:
            self.escala_animacion += 0.02
        else:
            self.escala_animacion -= 0.02
            if self.escala_animacion <= 1.0:
                self.escala_animacion = 1.0

    def _actualizar_temporizadores(self) -> None:
        """Actualiza los temporizadores de mensaje y animación."""
        if self.temporizador_mensaje > 0:
            self.temporizador_mensaje -= 1

    def dibujar(self, pantalla: pygame.Surface) -> None:
        """Dibuja la escena en la pantalla."""
        pantalla.blit(self.fondo, (0, 0))

        if self.correo_abierto is None:
            self._dibujar_bandeja(pantalla)
            self.pista_normal.dibujar(pantalla)
            self._dibujar_mensaje_aceptacion(pantalla)
        else:
            self.barra_titulo.dibujar(pantalla)
            self._dibujar_correo_abierto(pantalla)
            self.pista_correo.dibujar(pantalla)
            self._dibujar_animacion_aceptacion(pantalla)
            self._dibujar_mensaje_aceptacion(pantalla)

    def _dibujar_bandeja(self, pantalla: pygame.Surface) -> None:
        """Dibuja la vista de la bandeja de entrada."""
        tabla = self._obtener_rectangulo_tabla(pantalla)
        altura_fila = tabla.height // max(len(self.email_usuario.bandeja_entrada) + 1, 5)
        padding = 8

        x_asunto = tabla.x + int(tabla.width * 0.2)
        x_fecha = tabla.x + int(tabla.width * 0.87)

        for indice, correo in enumerate(self.email_usuario.bandeja_entrada):
            y = tabla.y + indice * altura_fila

            # Resaltar selección
            if indice == self.seleccionado:
                Frame(
                    tabla.x / pantalla.get_width(),
                    y / pantalla.get_height(),
                    tabla.width / pantalla.get_width(),
                    altura_fila / pantalla.get_height(),
                    bg_color=(100, 160, 255),
                    alpha=90
                ).dibujar(pantalla)

            # Índice de no leído
            color_texto = (0, 0, 120) if not correo["leido"] else (30, 30, 70)
            if not correo["leido"]:
                pygame.draw.circle(
                    pantalla, (0, 80, 200),
                    (tabla.x + padding + 4, y + altura_fila // 2), 4
                )

            # Texto del correo
            self._dibujar_texto(pantalla, correo["de"], self.fuente_fila, color_texto,
                                tabla.x + padding + 12, y, altura_fila)
            self._dibujar_texto(pantalla, correo["asunto"], self.fuente_fila, color_texto,
                                x_asunto + padding, y, altura_fila)
            self._dibujar_texto(pantalla, correo["fecha"], self.fuente_meta, (60, 60, 110),
                                x_fecha + padding, y, altura_fila)

            # Línea separadora
            pygame.draw.line(pantalla, (180, 185, 205),
                            (tabla.x, y + altura_fila - 1),
                            (tabla.right, y + altura_fila - 1), 1)

    def _dibujar_correo_abierto(self, pantalla: pygame.Surface) -> None:
        """Dibuja el cuerpo del correo abierto."""
        correo = self.correo_abierto
        tabla = self._obtener_rectangulo_tabla(pantalla)

        x = tabla.x + 10
        y = tabla.y + 6
        altura_linea = self.fuente_cuerpo.get_height() + 5

        # Información meta
        for texto, color in [
            (f"De:    {correo['de']}", (60, 60, 130)),
            (f"Fecha: {correo['fecha']}", (60, 60, 130))
        ]:
            superficie = self.fuente_meta.render(texto, False, color)
            pantalla.blit(superficie, (x, y))
            y += superficie.get_height() + 3

        # Separador
        pygame.draw.line(pantalla, (160, 165, 200),
                        (tabla.x, y + 2), (tabla.right, y + 2), 1)
        y += 12

        # Cuerpo del mensaje
        for linea in correo["cuerpo"]:
            if y + altura_linea > tabla.bottom:
                break

            if linea == "":
                y += altura_linea // 2
                continue

            superficie = self.fuente_cuerpo.render(linea, False, (20, 20, 60))
            pantalla.blit(superficie, (x, y))
            y += altura_linea

        # Botón de aceptar
        self._dibujar_boton_aceptar(pantalla, tabla)

    def _dibujar_boton_aceptar(self, pantalla: pygame.Surface, tabla: pygame.Rect) -> None:
        """Dibuja el prompt para aceptar el trabajo."""
        texto = "[E] Aceptar Trabajo"
        superficie = self.fuente_titulo.render(texto, False, (255, 255, 255))

        x = tabla.x + (tabla.width - superficie.get_width()) // 2
        y = tabla.bottom - superficie.get_height() - 10

        # Fondo para legibilidad
        fondo = pygame.Surface((superficie.get_width() + 20, superficie.get_height() + 10), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))
        pantalla.blit(fondo, (x - 10, y - 5))
        pantalla.blit(superficie, (x, y))

    def _dibujar_animacion_aceptacion(self, pantalla: pygame.Surface) -> None:
        """Dibuja la animación de la laptop aceptada."""
        if not self.icono_laptop or not self.animacion_laptop or self.temporizador_animacion <= 0:
            return

        # Escalar icono
        escala = self.escala_animacion
        ancho = int(self.icono_laptop.get_width() * escala)
        alto = int(self.icono_laptop.get_height() * escala)
        laptop_escalado = pygame.transform.scale(self.icono_laptop, (ancho, alto))

        # Posicionar en el centro
        x = pantalla.get_width() // 2 - ancho // 2
        y = pantalla.get_height() // 2 - alto // 2

        # Fondo sutil
        radio = max(ancho, alto) // 2 + 10
        pygame.draw.circle(pantalla, (20, 20, 40, 180),
                         (pantalla.get_width() // 2, pantalla.get_height() // 2), radio)

        # Dibujar laptop
        pantalla.blit(laptop_escalado, (x, y))

        # Nombre del modelo
        texto_modelo = self.animacion_laptop.modelo
        superficie_modelo = self.fuente_meta.render(texto_modelo, False, (255, 255, 255))
        x_modelo = pantalla.get_width() // 2 - superficie_modelo.get_width() // 2
        y_modelo = y + alto + 10
        pantalla.blit(superficie_modelo, (x_modelo, y_modelo))

    def _dibujar_mensaje_aceptacion(self, pantalla: pygame.Surface) -> None:
        """Dibuja el mensaje temporal de aceptación."""
        if not self.mensaje_aceptacion or self.temporizador_mensaje <= 0:
            return

        superficie = self.fuente_meta.render(self.mensaje_aceptacion, False, (255, 255, 0))
        x = pantalla.get_width() // 2 - superficie.get_width() // 2
        y = pantalla.get_height() - 50

        # Fondo para legibilidad
        fondo = pygame.Surface((superficie.get_width() + 20, superficie.get_height() + 10), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))
        pantalla.blit(fondo, (x - 10, y - 5))
        pantalla.blit(superficie, (x, y))

    # --- Métodos auxiliares ---

    def _obtener_rectangulo_tabla(self, pantalla: pygame.Surface) -> pygame.Rect:
        """Obtiene el rectángulo donde se muestra la tabla de correos."""
        return Frame(0.05, 0.254, 0.9, 0.4).get_rect(pantalla)

    def _dibujar_texto(self, pantalla: pygame.Surface, texto: str, fuente: pygame.font.Font,
                        color: tuple, x: int, y: int, altura_fila: int) -> None:
        """Dibuja texto centrado verticalmente en una fila."""
        superficie = fuente.render(texto, False, color)
        pantalla.blit(superficie, (x, y + (altura_fila - superficie.get_height()) // 2))