from pathlib import Path
import sys

class Rutas:
    if getattr(sys, "frozen", False):
        RAIZ = Path(sys.executable).parent
    else:
        RAIZ = Path(__file__).resolve().parent.parent
    
    ASSETS = RAIZ / "assets"
    
    IMAGENES = ASSETS / "images"
    FUENTES = ASSETS / "fonts"
    SONIDOS = ASSETS / "sounds"
    MUSICA = ASSETS / "music"
    MAPAS = ASSETS / "maps"
    
    
    @classmethod
    def imagen(cls, archivo: str) -> Path:
        return cls.IMAGENES / archivo
    
    
    @classmethod
    def fuente(cls, archivo: str) -> Path:
        return cls.FUENTES / archivo
    
    
    @classmethod
    def sonido(cls, archivo: str) -> Path:
        return cls.SONIDOS / archivo
    
    
    @classmethod
    def musica(cls, archivo: str) -> Path:
        return cls.MUSICA / archivo
    
    
    @classmethod
    def mapa(cls, archivo: str) -> Path:
        return cls.MAPAS / archivo