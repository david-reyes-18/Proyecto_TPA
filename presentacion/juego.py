import pygame
from typing import TYPE_CHECKING
from infraestructura.config import FPS, FRAME_ANCHO, FRAME_ALTO, ESCALA_JUGADOR
from presentacion.manejador_escenas import ManejadorEscenas
from infraestructura.recursos.manejador_jsons import cargar_config_json
from presentacion.escenas.escena_menu import MenuPrincipal
from dominio.entidades.jugador.jugador import Jugador

if TYPE_CHECKING:
    from dominio.servicios.gestor_trabajos import Trabajo


class Juego:

    """
    Aquí se ejecuta el mainloop principal del juego y el
    manejo de escenas, así como sus actualizaciones, dibujos
    y manejo de eventos.
    """

    def __init__(self):

        datos_resolucion = cargar_config_json("resolucion")

        self.ancho = datos_resolucion["ancho"]
        self.alto = datos_resolucion["alto"]

        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Innomath")

        self.reloj = pygame.time.Clock()
        self.corriendo = True

        # Objeto que manejará las diferentes escenas
        self.manejador_escenas = ManejadorEscenas()

        # Jugador con tamaño definido desde infraestructura/config
        ancho_jugador = FRAME_ANCHO * ESCALA_JUGADOR
        alto_jugador  = FRAME_ALTO  * ESCALA_JUGADOR
        self.jugador = Jugador(0, 0, ancho=ancho_jugador, alto=alto_jugador)

        # Trabajo aceptado desde el correo, pendiente de reparar en el taller.
        # EscenaTaller lo lee para saber qué dispositivo mostrar.
        self.trabajo_activo: "Trabajo | None" = None

        # Se inicializa en la escena del menú principal
        self.manejador_escenas.cambiar_escena(MenuPrincipal(self))

    def run(self) -> None:
        """Bucle principal del juego."""

        while self.corriendo:
            dt = self.reloj.tick(FPS) / 1000
            eventos = pygame.event.get()

            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.corriendo = False

            self.manejador_escenas.manejar_eventos(eventos)
            self.manejador_escenas.actualizar(dt)
            self.manejador_escenas.dibujar(self.pantalla)

            pygame.display.flip()

        pygame.quit()
