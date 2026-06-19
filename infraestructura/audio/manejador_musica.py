import pygame
from infraestructura.recursos.rutas import Rutas
from infraestructura.recursos.manejador_jsons import cargar_datos_json, guardar_datos_json, cargar_config_json


class ManejadorMusica:

    datos_volumen = cargar_config_json("volumen")
    volumen_musica = datos_volumen["musica"]

    _pista_actual: str | None = None
    _volumen: float = volumen_musica
    _inicializado: bool = False

    @classmethod
    def inicializar(cls) -> None:
        if not cls._inicializado:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            cls._inicializado = True

    @classmethod
    def reproducir(cls, archivo: str, loops: int = -1, fade_ms: int = 800) -> None:

        cls.inicializar()
        # Misma canción → no interrumpir
        if cls._pista_actual == archivo and pygame.mixer.music.get_busy():
            return

        # Distinta canción → fade-out rápido, luego cargar y reproducir
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(400)

        ruta = Rutas.musica(archivo)
        try:
            pygame.mixer.music.load(str(ruta))
            pygame.mixer.music.set_volume(cls._volumen)
            pygame.mixer.music.play(loops, fade_ms=fade_ms)
            cls._pista_actual = archivo
        except pygame.error as e:
            print(f"[ManejadorMusica] No se pudo cargar '{archivo}': {e}")

    @classmethod
    def detener(cls, fade_ms: int = 500) -> None:
        """Detiene la música con fade-out."""
        cls.inicializar()
        pygame.mixer.music.fadeout(fade_ms)
        cls._pista_actual = None

    @classmethod
    def pausar(cls) -> None:
        cls.inicializar()
        pygame.mixer.music.pause()

    @classmethod
    def reanudar(cls) -> None:
        cls.inicializar()
        pygame.mixer.music.unpause()

    @classmethod
    def establecer_volumen(cls, volumen: float) -> None:
        cls._volumen = max(0.0, min(1.0, volumen))
        cls.inicializar()
        pygame.mixer.music.set_volume(cls._volumen)
        datos_config = cargar_datos_json("config.json")
        datos_config["volumen"]["musica"] = cls._volumen
        guardar_datos_json("config.json", datos_config)

    @classmethod
    def obtener_volumen(cls) -> float:
        return cls._volumen

    @classmethod
    def pista_actual(cls) -> str | None:
        return cls._pista_actual