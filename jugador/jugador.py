"""
Refactorización de la clase Jugador con mejoras prácticas de SOLID.
Se centra en separar las responsabilidades sin sobreingeniería.
"""

import pygame
from typing import List
from core.rutas import Rutas
from core.config import FRAME_ANCHO, FRAME_ALTO, ESCALA_GLOB, ESCALA_JUGADOR
from core.manejador_sonidos import ManejadorSonidos
from sistema.inventario import Inventario
from jugador.stats import StatsJugador
from jugador.renderer import Renderizador


class ReproductorSonidosPasos:
    """Estrategia para la reproducción del sonido de pasos - extracción simple."""

    def __init__(self, intervalo_pasos: float = 0.35):
        self._timer_pasos = 0.0
        self._intervalo_pasos = intervalo_pasos

    def actualizar_y_reproducir(self, moviendose: bool, dt: float) -> bool:
        """
        Actualiza el temporizador de pasos y reproduce el sonido si es necesario.

        Devuelve:
            bool: True si se reprodujo un sonido de paso
        """
        if not moviendose:
            self._timer_pasos = 0
            return False

        self._timer_pasos -= dt
        if self._timer_pasos <= 0:
            ManejadorSonidos.reproducir("pasos.ogg")
            self._timer_pasos = self._intervalo_pasos
            return True
        return False


class Jugador:
    """
    Clase del jugador con mejora en la separación de responsabilidades.

    Mejoras realizadas:
    1. Se extrajo la lógica del sonido de pasos a una clase estrategia
    2. Se limpió la delegación de estadísticas para reducir duplicación
    3. Mejor organización de la lógica de movimiento y colisión
    4. Se mantuvo la compatibilidad hacia atrás
    5. Se aplicó SRP separando la estrategia de sonido
    """

    def __init__(self, x: int, y: int):
        # Propiedades físicas
        self.ancho: int = FRAME_ANCHO * ESCALA_JUGADOR
        self.alto: int = FRAME_ALTO * ESCALA_JUGADOR

        # Hitbox para los pies (efecto 2D retro)
        hitbox_pies: int = self.alto // 4
        self.hitbox = pygame.Rect(
            x,
            y + self.alto - hitbox_pies,
            self.ancho,
            hitbox_pies
        )

        # Rectángulo principal para el renderizado
        self.rect = pygame.Rect(
            x,
            y,
            self.ancho,
            self.alto
        )

        # Propiedades de movimiento
        self.velocidad: int = 100 * ESCALA_GLOB
        self.direccion: str = "ABAJO"
        self.moviendose: bool = False

        # Componentes (inyección de dependencias por composición)
        self.estadisticas = StatsJugador()
        self.renderizador = Renderizador(self.ancho, self.alto)
        self.inventario = Inventario()

        # Estrategia de sonido (aplicando el patrón Strategy)
        self.reproductor_sonidos = ReproductorSonidosPasos()

        # Seguimiento de cambios en estadísticas (para notificaciones si se necesita)
        self._ultimo_dinero = 0
        self._ultima_experiencia = 0
        self._ultimo_nivel = 0

    # ==================== DELEGACIÓN DE ESTADÍSTICAS (reducción de duplicación) ====================

    @property
    def dinero(self) -> int:
        return self.estadisticas.dinero

    @property
    def experiencia(self) -> int:
        return self.estadisticas.experiencia

    @property
    def nivel(self) -> int:
        return self.estadisticas.nivel

    def agregar_dinero(self, cantidad: int) -> None:
        """Añade dinero al jugador."""
        valor_antiguo = self.dinero
        self.estadisticas.agregar_dinero(cantidad)
        valor_nuevo = self.dinero

        # Seguimiento de cambios (podría usarse para eventos/notificaciones)
        if valor_antiguo != valor_nuevo:
            self._ultimo_dinero = valor_antiguo
            # En una implementación completa, aquí se dispararía un evento

    def agregar_experiencia(self, cantidad: int) -> None:
        """Añade experiencia y sube de nivel si es necesario."""
        valores_antiguos = {
            "experiencia": self.experiencia,
            "nivel": self.nivel
        }
        self.estadisticas.agregar_experiencia(cantidad)
        valores_nuevos = {
            "experiencia": self.experiencia,
            "nivel": self.nivel
        }

        # Seguimiento de cambios
        if valores_antiguos["experiencia"] != valores_nuevos["experiencia"]:
            self._ultima_experiencia = valores_antiguos["experiencia"]
        if valores_antiguos["nivel"] != valores_nuevos["nivel"]:
            self._ultimo_nivel = valores_antiguos["nivel"]

    # ==================== DELEGACIÓN DE INVENTARIO (limpiado) ====================

    def agregar_portatil(self, portatil) -> None:
        """Añade un portátil al inventario del jugador."""
        self.inventario.agregar_laptop(portatil)

    def remover_portatil(self, indice: int):
        """Elimina y devuelve un portátil del inventario por índice."""
        return self.inventario.remover_laptop(indice)

    def obtener_portatil(self, indice: int):
        """Obtiene un portátil del inventario sin eliminarlo."""
        return self.inventario.obtener_laptop(indice)

    # Nota: Se eliminaron los métodos duplicados de dinero/experiencia del inventario
    # para evitar confusiones - use los métodos directos del jugador en su lugar
    # El inventario mantiene sus propias estadísticas para guardado/carga

    # ==================== MOVIMIENTO Y ACTUALIZACIÓN ====================

    def actualizar(
        self,
        dt: float,
        dx: int,
        dy: int,
        obstaculos: List[pygame.Rect]
    ) -> None:
        """
        Actualiza el estado del jugador incluyendo movimiento, animación y sonido.

        Responsabilidades separadas:
        - Cálculo de la dirección de movimiento
        - Actualización de la animación
        - Manejo del movimiento y colisión
        - Gestión del sonido (delegada a la estrategia)
        """
        estaba_moviendose = self.moviendose
        self.moviendose = dx != 0 or dy != 0

        # Calcular dirección de movimiento
        if dx < 0:
            self.direccion = "IZQUIERDA"
        elif dx > 0:
            self.direccion = "DERECHA"
        elif dy < 0:
            self.direccion = "ARRIBA"
        elif dy > 0:
            self.direccion = "ABAJO"

        # Actualizar animación en el renderizador
        self.renderizador.actualizar_animacion(dt, self.direccion, self.moviendose)

        # Manejar movimiento y colisión en eje X
        self.hitbox.x += dx
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo):
                if dx > 0:
                    self.hitbox.right = obstaculo.left
                elif dx < 0:
                    self.hitbox.left = obstaculo.right

        # Manejar movimiento y colisión en eje Y
        self.hitbox.y += dy
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo):
                if dy > 0:
                    self.hitbox.bottom = obstaculo.top
                elif dy < 0:
                    self.hitbox.top = obstaculo.bottom

        # Sincronizar sprite con hitbox
        self.rect.midbottom = self.hitbox.midbottom

        # Gestionar sonido de pasos usando el patrón Strategy
        self.reproductor_sonidos.actualizar_y_reproducir(self.moviendose, dt)

    # ==================== RENDERIZADO ====================

    def dibujar(
        self,
        pantalla: pygame.Surface,
        camara: pygame.Rect
    ) -> None:
        """Dibuja al jugador en la pantalla."""
        self.renderizador.dibujar(pantalla, self.rect, camara, self.direccion, self.moviendose)

    # ==================== MÉTODOS DE ESTADO DE INVENTARIO (para guardado/carga) ====================

    def obtener_estado_inventario(self) -> dict:
        """Obtiene el estado del inventario para guardar/cargar."""
        return self.inventario.obtener_estado()

    def cargar_estado_inventario(self, estado: dict) -> None:
        """Carga el estado del inventario."""
        self.inventario.cargar_estado(estado)

        # Sincroniza las estadísticas del jugador con las del inventario al cargar
        # Esto mantiene consistencia entre los dos sistemas
        self.estadisticas.dinero = estado.get("dinero", 0)
        self.estadisticas.experiencia = estado.get("experiencia", 0)
        self.estadisticas.nivel = estado.get("nivel", 1)