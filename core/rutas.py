from pathlib import Path
import sys


class Rutas:
    
    
    """
    Clase que maneja las rutas de los archivos del sistema,
    como lo son las imagenes, fuentes, sonidos, música y mapas
    """
    
    # Si el juego ha sido empaquetado o congelado (si es un .exe), entonces 
    # la RAIZ el juego será laruta en odnde se encuentre el archivo ejecutable,
    # sino entonces el archivo está siendo ejecutado desde un editor de código
    # o por terminal, entonces entra a la carpeta RAIZ del proyecto
    
    if getattr(sys, "frozen", False):
        RAIZ = Path(sys.executable).parent
    else:
        RAIZ = Path(__file__).resolve().parent.parent
    
    #Carpeta de los archivos importantes del sistema
    ASSETS = RAIZ / "assets"
    
    #Carpetas dentro de assets
    IMAGENES = ASSETS / "images"
    FUENTES = ASSETS / "fonts"
    SONIDOS = ASSETS / "sounds"
    MUSICA = ASSETS / "music"
    MAPAS = ASSETS / "maps"
    
    #   Métodos para llamar al archivo que se quiere obtener
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