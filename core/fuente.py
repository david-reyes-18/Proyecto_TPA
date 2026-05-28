import pygame
from core.rutas import Rutas


class Fuente:
    
    """
    Clase que genera fuentes de texto, especificamente la fuente
    pixel.ttf en distintos tamaños dependiendo cúal se nesesite
    """
    
    #Los tamaños se van almacenando en un caché temporalpara evitar crear demasiados objetos
    _cache = {}
    
    FUENTE = Rutas.fuente("pixel.ttf")
    
    @classmethod
    def obtener(cls, size: int) -> pygame.font.Font:
        key = (cls.FUENTE, size)
        if key not in cls._cache:
            cls._cache[key] = pygame.font.Font(
                cls.FUENTE,
                size
            )
        return cls._cache[key]