import pygame
from escenarios.escena_base import EscenaBase
from escenarios.escenario_juego import EscenarioJuego # Importamos el nivel para poder activarlo

class MenuPrincipal(EscenaBase):
    def __init__(self, gestor_juego):
        super().__init__(gestor_juego)
        self.fuente = pygame.font.Font(None, 50)

    def procesar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                # 🔄 Si el usuario presiona ENTER, hacemos el cambio de estado
                if evento.key == pygame.K_RETURN:
                    nuevo_nivel = EscenarioJuego(self.gestor_juego)
                    self.gestor_juego.cambiar_escena(nuevo_nivel)

            # Si quieres que funcione con clic de ratón en un botón,
            # aquí procesarías el evento pygame.MOUSEBUTTONDOWN

    def actualizar(self, teclas):
        pass

    def dibujar(self, pantalla):
        # Limpiamos la pantalla con un fondo azul oscuro para el menú
        pantalla.fill((20, 20, 40)) 
        
        # Dibujamos un texto indicativo en el centro
        texto = self.fuente.render("PRESIONA ENTER PARA JUGAR", True, (255, 255, 255))
        rect_texto = texto.get_rect(center=(400, 300))
        pantalla.blit(texto, rect_texto)