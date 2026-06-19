import pygame
from infraestructura.config import FPS
from aplicacion.casos_de_uso.manejador_escenas import ManejadorEscenas
from infraestructura.recursos.manejador_jsons import cargar_config_json
from presentacion.escenas.escena_menu import MenuPrincipal
from dominio.entidades.jugador.jugador import Jugador


class Juego:

    """
    Aquí se ejecuta el mainloop principal del juego y el
    manejo  de escenas, asi como sus actualizaciones, dibujos
    y manejo de eventos
    """
    
    def __init__(self):
        
        datos_resolucion = cargar_config_json("resolucion")
        
        self.ancho = datos_resolucion["ancho"]
        self.alto = datos_resolucion["alto"]
        
        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )
        
        pygame.display.set_caption("Innomath")

        self.reloj = pygame.time.Clock()
        self.corriendo = True
        
        #Objeto que manejará las diferentes escenas
        self.manejador_escenas = ManejadorEscenas()
        
        # Crear el jugador (en posición inicial será establecida más tarde)
        self.jugador = Jugador(0, 0)  # Position will be set from config

        # Nombre del jugador (será cambiado más tarde)
        self.player_name = "Jugador"
        
                # Se inicializa en la escena del menú principal
        self.manejador_escenas.cambiar_escena(
            MenuPrincipal(self)
        )
    
    
    def run(self) -> None:
        
        """Bucle principal del juegos"""
        
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