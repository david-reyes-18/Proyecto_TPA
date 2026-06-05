import pygame
from typing import List
from core.config import FRAME_ANCHO, FRAME_ALTO, ESCALA_GLOB, ESCALA_JUGADOR
from jugador.reproductor_sonido_pasos  import ReproductorSonidosPasos
from jugador.inventario import Inventario
from jugador.stats_jugador import StatsJugador
from jugador.renderizador import Renderizador
from jugador.direcciones import Direcciones


class Jugador:
    """
    Clase que modela al jugador con gestión de movimiento, renderizado y estadísticas.
    """
    def __init__(self, x: int, y: int):
        # Propiedades físicas
        self.ancho: int = FRAME_ANCHO * ESCALA_JUGADOR
        self.alto: int = FRAME_ALTO * ESCALA_JUGADOR
        
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
        self.velocidad = 100 * ESCALA_GLOB
        self.direccion = Direcciones.ABAJO
        self.moviendose = False
        
        # Componentes
        self.stats = StatsJugador()
        self.renderizador = Renderizador(self.ancho, self.alto)
        self.inventario = Inventario()
        
        # Estrategia de sonido (aplicando el patrón Strategy)
        self.reproductor_sonidos = ReproductorSonidosPasos()
        
    # Getters y Setters
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
    
    # Delegación de stats
    
    def agregar_dinero(self, cantidad: int) -> None:
        """Añade dinero al jugador."""
        self.stats.agregar_dinero(cantidad)
    
    def agregar_experiencia(self, cantidad: int) -> None:
        """Añade experiencia y sube de nivel si es necesario."""
        self.stats.agregar_experiencia(cantidad)
    
    # Delegación de inventario
    
    def agregar_portatil(self, portatil) -> None:
        """Añade un portátil al inventario del jugador."""
        self.inventario.agregar_laptop(portatil)
        
    def remover_portatil(self, indice: int):
        """Elimina y devuelve un portátil del inventario por índice."""
        return self.inventario.remover_laptop(indice)
    
    def obtener_portatil(self, indice: int):
        """Obtiene un portátil del inventario sin eliminarlo."""
        return self.inventario.obtener_laptop(indice)
    
    def actualizar(
        self,
        dt: float,
        dx: int,
        dy: int,
        obstaculos: List[pygame.Rect]
    ) -> None:
        """
        Actualiza el estado del jugador incluyendo movimiento, animación y sonido.
        """
        self.moviendose = dx != 0 or dy != 0
        
        # Calcular dirección de movimiento
        if dx < 0:
            self.direccion = Direcciones.IZQUIERDA
        elif dx > 0:
            self.direccion = Direcciones.DERECHA
        elif dy < 0:
            self.direccion = Direcciones.ARRIBA
        elif dy > 0:
            self.direccion = Direcciones.ABAJO
        
        # Actualizar animación en el renderizador
        self.renderizador.actualizar_animacion(dt, self.direccion.value, self.moviendose)
        
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
    
    def dibujar(
        self,
        pantalla: pygame.Surface,
        camara: pygame.Rect
    ) -> None:
        """Dibuja al jugador en la pantalla."""
        self.renderizador.dibujar(pantalla, self.rect, camara, self.direccion.value, self.moviendose)
    
    def obtener_estado_inventario(self) -> dict:
        """Obtiene el estado del inventario para guardar/cargar."""
        return self.inventario.obtener_estado()
    
    def cargar_estado_inventario(self, estado: dict) -> None:
        """Carga el estado del inventario."""
        self.inventario.cargar_estado(estado)
        
        # Sincroniza las estadísticas del jugador con las del inventario al cargar
        # Esto mantiene consistencia entre los dos sistemas
        self.stats.dinero = estado.get("dinero", 0)
        self.stats.experiencia = estado.get("experiencia", 0)
        self.stats.nivel = estado.get("nivel", 1)