from core.manejador_jsons import cargar_datos_json, guardar_datos_json


class StatsJugador:
    """
    Cargar y guarda stats del jugador como el dinero, experiencia
    y nivel actual
    """
    
    def __init__(self):
        
        # Se cargan las stats del jugador del json
        stats_jugador = self._cargar_stats()
        
        self._dinero = stats_jugador["dinero"]
        self._experiencia = stats_jugador["experiencia"]
        self._nivel = stats_jugador["nivel"]
    
    #   Propiedades
    
    @property
    def dinero(self) -> int:
        return self._dinero
    
    @property
    def experiencia(self) -> int:
        return self._experiencia
    
    @property
    def nivel(self) -> int:
        return self._nivel
    
    #  Setters
    
    @dinero.setter
    def dinero(self, valor: int) -> None:
        if valor != self._dinero:
            self._dinero = valor
            self._guardar_stats()
    
    @experiencia.setter
    def experiencia(self, valor: int) -> None:
        if valor != self._experiencia:
            self._experiencia = valor
            self._guardar_stats()

    @nivel.setter
    def nivel(self, valor: int) -> None:
        if valor != self._nivel:
            self._nivel = valor
            self._guardar_stats()
    
    #   Métodos
    
    def _cargar_stats(self) -> dict:
        """Carga los datos del json"""
        stats = cargar_datos_json("stats_jugador.json")
        return stats
    
    def _guardar_stats(self) -> None:
        """Guarda los stats del jugador en el json"""
        datos = {
            "dinero": self._dinero,
            "experiencia": self._experiencia,
            "nivel": self._nivel
        }
        guardar_datos_json("stats_jugador.json", datos)
    
    def agregar_dinero(self, cantidad: int) -> None:
        """Añade dinero al jugador."""
        self._dinero += cantidad
        # Asegura que el dinero no baje de cero (decision de diseño del juego)
        if self._dinero < 0:
            self._dinero = 0
        self._guardar_stats()
    
    def agregar_experiencia(self, cantidad: int) -> None:
        """
        Añade experiencia y sube de nivel si es necesario.
        
        Usa un sistema de nivelación progresiva donde cada nivel requiere
        más experiencia que el anterior (nivel * 100)
        """
        if cantidad <= 0:
            return
        self._experiencia += cantidad
        
        # Sube de nivel mientras la experiencia sea suficiente
        while self._experiencia >= self._nivel * 100 and self._nivel < 100:  # Límite en nivel 100
            self._experiencia -= self._nivel * 100
            self._nivel += 1
        
        self._guardar_stats()