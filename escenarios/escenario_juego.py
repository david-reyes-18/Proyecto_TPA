import pygame
from escenarios.escena_base import EscenaBase
from jugador.jugador import Jugador
from sistema.camara import GrupoCamara
# Asumimos que guardaste la clase Obstaculo en nucleo/entidades/obstaculo.py
from sistema.obstaculo import Obstaculo 

class EscenarioJuego(EscenaBase):
    def __init__(self, gestor_juego):
        super().__init__(gestor_juego)
        
        # Inicializamos los grupos
        self.sprites_visibles = GrupoCamara()
        self.grupo_colisiones = pygame.sprite.Group()
        
        # Creamos al jugador y lo añadimos a la cámara
        self.jugador = Jugador(400, 300)
        self.sprites_visibles.add(self.jugador)
        
        # Creamos un par de obstáculos de prueba y los añadimos a AMBOS grupos
        # (A la cámara para verlos, y a colisiones para la matemática)
        obs1 = Obstaculo(464, 300, 32) # Justo a la derecha del jugador
        obs2 = Obstaculo(400, 236, 32) # Justo arriba del jugador
        
        self.grupo_colisiones.add(obs1, obs2)
        self.sprites_visibles.add(obs1, obs2)

    def procesar_eventos(self, eventos):
        pass

    def actualizar(self, teclas):
        # ¡IMPORTANTE! Pasamos el grupo de colisiones al jugador
        self.jugador.actualizar(teclas, self.grupo_colisiones)

    def dibujar(self, pantalla):
        pantalla.fill((30, 150, 50)) # Un color verde tipo césped de fondo
        self.sprites_visibles.dibujar_centrado(self.jugador)