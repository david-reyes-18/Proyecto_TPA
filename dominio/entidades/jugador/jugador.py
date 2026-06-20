import pygame
from typing import List
from infraestructura.renderizador.renderizador import Renderizador
from infraestructura.audio.reproductor_sonido_pasos import ReproductorSonidosPasos
from dominio.entidades.jugador.inventario import Inventario
from dominio.entidades.jugador.stats_jugador import StatsJugador
from dominio.entidades.jugador.direcciones import Direcciones


class Jugador:
    """
    Clase que modela al jugador con gestión de movimiento, renderizado y estadísticas.
    """
    def __init__(self, x: int, y: int, ancho: int, alto: int):
        # Propiedades físicas — recibidas desde la capa de presentación
        self.ancho: int = ancho
        self.alto: int = alto

        # Hitbox para los pies (efecto 2D retro)
        hitbox_pies = self.alto // 4
        self.hitbox = pygame.Rect(
            x,
            y + self.alto - hitbox_pies,
            self.ancho,
            hitbox_pies
        )

        # Rectángulo principal para el renderizado
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)

        # Propiedades de movimiento
        self.velocidad: int = 0  # Asignada desde presentación al construir
        self.direccion = Direcciones.ABAJO
        self.moviendose = False

        # Componentes de dominio
        self.stats = StatsJugador()
        self.inventario = Inventario()

        # Infraestructura inyectada
        self.renderizador = Renderizador(self.ancho, self.alto)
        self.reproductor_sonidos = ReproductorSonidosPasos()

    # --- Getters / Setters delegados a StatsJugador ---

    @property
    def dinero(self) -> int:
        return self.stats.dinero

    @dinero.setter
    def dinero(self, valor: int) -> None:
        self.stats.dinero = valor

    @property
    def experiencia(self) -> int:
        return self.stats.experiencia

    @experiencia.setter
    def experiencia(self, valor: int) -> None:
        self.stats.experiencia = valor

    @property
    def nivel(self) -> int:
        return self.stats.nivel

    @nivel.setter
    def nivel(self, valor: int) -> None:
        self.stats.nivel = valor

    def agregar_dinero(self, cantidad: int) -> None:
        self.stats.agregar_dinero(cantidad)

    def agregar_experiencia(self, cantidad: int) -> None:
        self.stats.agregar_experiencia(cantidad)

    # --- Delegación de inventario ---

    def agregar_portatil(self, portatil) -> None:
        self.inventario.agregar_laptop(portatil)

    def remover_portatil(self, indice: int):
        return self.inventario.remover_laptop(indice)

    def obtener_portatil(self, indice: int):
        return self.inventario.obtener_laptop(indice)

    # --- Lógica de juego ---

    def actualizar(
        self,
        dt: float,
        dx: int,
        dy: int,
        obstaculos: List[pygame.Rect]
    ) -> None:
        """
        Actualiza el estado del jugador: movimiento, colisiones, animación y sonido.
        """
        self.moviendose = dx != 0 or dy != 0

        if dx < 0:
            self.direccion = Direcciones.IZQUIERDA
        elif dx > 0:
            self.direccion = Direcciones.DERECHA
        elif dy < 0:
            self.direccion = Direcciones.ARRIBA
        elif dy > 0:
            self.direccion = Direcciones.ABAJO

        self.renderizador.actualizar_animacion(dt, self.direccion.value, self.moviendose)

        self.hitbox.x += dx
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo):
                if dx > 0:
                    self.hitbox.right = obstaculo.left
                elif dx < 0:
                    self.hitbox.left = obstaculo.right

        self.hitbox.y += dy
        for obstaculo in obstaculos:
            if self.hitbox.colliderect(obstaculo):
                if dy > 0:
                    self.hitbox.bottom = obstaculo.top
                elif dy < 0:
                    self.hitbox.top = obstaculo.bottom

        self.rect.midbottom = self.hitbox.midbottom
        self.reproductor_sonidos.actualizar_y_reproducir(self.moviendose, dt)

    def dibujar(self, pantalla: pygame.Surface, camara: pygame.Rect) -> None:
        """Dibuja al jugador en la pantalla."""
        self.renderizador.dibujar(pantalla, self.rect, camara, self.direccion.value, self.moviendose)

    def obtener_estado_inventario(self) -> dict:
        return self.inventario.obtener_estado()

    def cargar_estado_inventario(self, estado: dict) -> None:
        self.inventario.cargar_estado(estado)
        self.stats.dinero = estado.get("dinero", 0)
        self.stats.experiencia = estado.get("experiencia", 0)
        self.stats.nivel = estado.get("nivel", 1)