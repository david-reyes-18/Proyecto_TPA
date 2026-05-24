import pygame
from core.rutas import Rutas

class Fuente:
    
    _cache = {}
    FUENTE = Rutas.fuente("pixel.ttf")
    
    @classmethod
    def get(cls, size: int) -> pygame.font.Font:
        
        key = (cls.FUENTE, size)
        if key not in cls._cache:
            cls._cache[key] = pygame.font.Font(
                cls.FUENTE,
                size
            )
        return cls._cache[key]