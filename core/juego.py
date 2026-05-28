import pygame
from core.config import ANCHO, ALTO, FPS
from core.manejador_escenas import ManejadorEscenas
from escenas.menu_principal import MenuPrincipal


class Juego:
    
    """
    Aquí se ejecuta el mainloop principal del juego y el
    manejo  de escenas, asi como sus actualizaciones, dibujos
    y maenejo de eventos
    """
    
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode(
            (ANCHO, ALTO)
        )
        
        pygame.display.set_caption("Innomath")
        
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        
        #Objeto que manejará las diferentes escenas
        self.manejador_escenas = ManejadorEscenas()
        
        #Se inicializa en la escena del menú principal
        self.manejador_escenas.cambiar_escena(
            MenuPrincipal(self)
        )
    
    def run(self) -> None:
        
        #Bucle principal del juegos
        while self.corriendo:
            
            #El tiempo que tardó el frame anterior en aparecer
            dt = self.reloj.tick(FPS) / 1000
            eventos = pygame.event.get()
            
            #Si se presionó el botón de salir entonces se detiene el bucle
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.corriendo = False
            
            #Manejo de eventos, actualización y dibujo de escenas
            self.manejador_escenas.manejar_eventos(eventos)
            self.manejador_escenas.actualizar(dt)
            self.manejador_escenas.dibujar(self.pantalla)
            
            #Actualiza la ventana
            pygame.display.flip()
            
        pygame.quit()