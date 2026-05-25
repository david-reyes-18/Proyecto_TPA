import pygame
from escenas.escena_base import EscenaBase
from escenas.menu_principal import MenuPrincipal


class EscenaJuego(EscenaBase):
    def __init__(self, juego):
        super().__init__(juego)
        self.jugador_x = 400
        self.jugador_y = 300
        self.velocidad_jugador = 220
        self.juego = juego
    
    def manejar_eventos(self, eventos: list[pygame.event.Event]):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.juego.cambiar_escena(
                        MenuPrincipal(self.juego)
                    )
    
    def actualizar(self, dt: float):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            self.jugador_y -= self.velocidad_jugador * dt
        
        if teclas[pygame.K_s]:
            self.jugador_y += self.velocidad_jugador * dt
        
        if teclas[pygame.K_a]:
            self.jugador_x -= self.velocidad_jugador * dt
        
        if teclas[pygame.K_d]:
            self.jugador_x += self.velocidad_jugador * dt
    
    def dibujar(self, pantalla):
        pantalla.fill((70, 170, 70))
        pygame.draw.rect(
            pantalla,
            (255, 0, 0),
            (
                self.jugador_x,
                self.jugador_y,
                32,
                32
            )
        )