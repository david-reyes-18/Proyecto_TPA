"""
Clase StatsJugador - gestiona las estadísticas del jugador.
Versión limpiada con encapsulación adecuada y lógica de nivelación.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class StatsJugador:
    """
    Gestiona las estadísticas del jugador siguiendo principios básicos de SOLID.

    Responsabilidades:
    - Rastrear y modificar dinero, experiencia y nivel del jugador
    - Manejar la lógica de subida de nivel
    - Proporcionar acceso a las estadísticas
    """

    dinero: int = 0
    experiencia: int = 0
    nivel: int = 1

    def agregar_dinero(self, cantidad: int) -> None:
        """Añade dinero al jugador."""
        self.dinero += cantidad
        # Asegura que el dinero no baje de cero (decision de diseño del juego)
        if self.dinero < 0:
            self.dinero = 0

    def agregar_experiencia(self, cantidad: int) -> None:
        """
        Añade experiencia y sube de nivel si es necesario.

        Usa un sistema de nivelación progresiva donde cada nivel requiere
        más experiencia que el anterior (nivel * 100)
        """
        if cantidad <= 0:
            return

        self.experiencia += cantidad

        # Sube de nivel mientras la experiencia sea suficiente
        while self.experiencia >= self.nivel * 100 and self.nivel < 100:  # Límite en nivel 100
            self.experiencia -= self.nivel * 100
            self.nivel += 1

    # Métodos de utilidad para sistemas del juego
    def obtener_experiencia_para_siguiente_nivel(self) -> int:
        """Obtiene la experiencia necesaria para el próximo nivel."""
        return self.nivel * 100 - self.experiencia

    def obtener_porcentaje_nivel_actual(self) -> float:
        """Obtiene el progreso hacia el nivel actual como porcentaje (0.0 a 1.0)."""
        experiencia_necesaria = self.nivel * 100
        if experiencia_necesaria == 0:
            return 1.0
        return self.experiencia / experiencia_necesaria

    def a_diccionario(self) -> Dict[str, Any]:
        """Convierte las estadísticas a diccionario para serialización."""
        return {
            "dinero": self.dinero,
            "experiencia": self.experiencia,
            "nivel": self.nivel
        }

    def desde_diccionario(self, datos: Dict[str, Any]) -> None:
        """Carga las estadísticas desde un diccionario."""
        self.dinero = max(0, datos.get("dinero", 0))
        self.experiencia = max(0, datos.get("experiencia", 0))
        self.nivel = max(1, min(datos.get("nivel", 1), 100))