import pygame
from infraestructura.recursos.rutas import Rutas
from infraestructura.recursos.manejador_jsons import cargar_config_json, cargar_datos_json, guardar_datos_json


class ManejadorSonidos:

    """
    Carga y maneja efectos de sonido independientes de la música
    actual, guarda los efectos cargados en un caché.
    """

    datos_volumen = cargar_config_json("volumen")
    volumen_sonidos = datos_volumen["sonidos"]

    _volumen: float = volumen_sonidos
    _cache: dict[str, pygame.mixer.Sound] = {}
    _inicializado: bool = False


    @classmethod
    def inicializar(cls) -> None:
        if not cls._inicializado:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            cls._inicializado = True

    @classmethod
    def reproducir(cls, archivo: str) -> None:
        """
        Reproduce un efecto de sonido. Si el archivo no está en caché lo carga.
        El sonido se superpone a la música y a otros efectos.

        :param archivo: Nombre del archivo dentro de assets/sounds/
                        Ej: "click.ogg", "pasos.ogg"
        """
        cls.inicializar()

        if archivo not in cls._cache:
            ruta = Rutas.sonido(archivo)
            try:
                cls._cache[archivo] = pygame.mixer.Sound(str(ruta))
            except pygame.error as e:
                print(f"[ManejadorSonidos] No se pudo cargar '{archivo}': {e}")
                return

        sonido = cls._cache[archivo]
        sonido.set_volume(cls._volumen)
        sonido.play()

    @classmethod
    def establecer_volumen(cls, volumen: float) -> None:

        cls._volumen = max(0.0, min(1.0, volumen))
        for sonido in cls._cache.values():
            sonido.set_volume(cls._volumen)

        datos_config = cargar_datos_json("config.json")
        datos_config["volumen"]["sonidos"] = cls._volumen
        guardar_datos_json("config.json", datos_config)

    @classmethod
    def obtener_volumen(cls) -> float:
        return cls._volumen

    def precargar(cls, *archivos: str) -> None:
        """
        Carga archivos en caché sin reproducirlos todavía.
        Útil para precargar al inicio de una escena y evitar lag.

        Ej: ManejadorEfectos.precargar("click.ogg", "pasos.ogg", "correcto.ogg")
        """
        cls.inicializar()
        for archivo in archivos:
            if archivo not in cls._cache:
                ruta = Rutas.sonido(archivo)
                try:
                    cls._cache[archivo] = pygame.mixer.Sound(str(ruta))
                    cls._cache[archivo].set_volume(cls._volumen)
                except pygame.error as e:
                    print(f"[ManejadorSonidos] No se pudo precargar '{archivo}': {e}")