import pygame

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, tamano_casilla):
        super().__init__()
        # Usamos una Surface vacía (invisible) o de color temporal para depurar
        self.image = pygame.Surface((tamano_casilla, tamano_casilla))
        self.image.fill((0, 255, 0)) # Verde temporal para que veas dónde los pones
        self.rect = self.image.get_rect(topleft=(x, y))