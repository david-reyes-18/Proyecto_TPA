import pygame
from core.config import *
from core.manejador_escenas import ManejadorEscenas
from escenas.menu_principal import MenuPrincipal


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(
            (ANCHO, ALTO)
        )
        
        pygame.display.set_caption("Innomath")
        
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        self.manejador_escenas = ManejadorEscenas()
        
        self.manejador_escenas.cambiar_escena(
            MenuPrincipal(self)
        )
    
    def run(self):
        while self.corriendo:
            
            dt = self.reloj.tick(60) / 1000
            eventos = pygame.event.get()
            
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.running = False
                    
            self.manejador_escenas.manejar_eventos(eventos)
            self.manejador_escenas.actualizar(dt)
            self.manejador_escenas.dibujar(self.pantalla)
            pygame.display.flip()
            
        pygame.quit()