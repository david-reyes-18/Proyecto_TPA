import pygame

class GrupoCamara(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # Obtenemos la pantalla actual y calculamos su centro exacto
        self.pantalla = pygame.display.get_surface()
        self.mitad_ancho = self.pantalla.get_size()[0] // 2
        self.mitad_alto = self.pantalla.get_size()[1] // 2
        
        # El Vector2 es ideal para guardar coordenadas X e Y de forma limpia
        self.offset = pygame.math.Vector2()

    def dibujar_centrado(self, objetivo):
        # 1. Calculamos el desplazamiento basado en la posición del jugador
        self.offset.x = objetivo.rect.centerx - self.mitad_ancho
        self.offset.y = objetivo.rect.centery - self.mitad_alto

        # 2. Dibujamos todos los sprites del grupo aplicando ese desplazamiento
        for sprite in self.sprites():
            # Restamos el offset a la posición real del sprite en el mundo
            posicion_en_pantalla = sprite.rect.topleft - self.offset
            self.pantalla.blit(sprite.image, posicion_en_pantalla)