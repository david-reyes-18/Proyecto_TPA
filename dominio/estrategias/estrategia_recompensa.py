from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Recompensa:
    
    """
    Representa la recompensa final a partir de los valores base del trabajo
    y el nivel actual del jugador.
    """
    dinero: int
    experiencia: int


class EstrategiaRecompensa(ABC):
    """
    Interfaz para estrategias de recompensa.
    """

    @abstractmethod
    def calcular(
            self, 
            recompensa_base_dinero: int, 
            recompensa_base_xp: int, 
            nivel_jugador: int
        ) -> Recompensa:
        """
        Calcula la recompensa final a partir de los valores base del trabajo
        y el nivel actual del jugador.
        """
        pass


class RecompensaEstandar(EstrategiaRecompensa):
    """
    Recompenza por defecto: entrega exactamente los valores base definidos
    en el trabajo.
    """

    def calcular(
            self, 
            recompensa_base_dinero: int, 
            recompensa_base_xp: int, 
            nivel_jugador: int
        ) -> Recompensa:
        
        return Recompensa(dinero=recompensa_base_dinero, experiencia=recompensa_base_xp)


class RecompensaEscalada(EstrategiaRecompensa):
    """
    Recompensa por escala: aumenta la recompensa en modos aleatorios.

    Fórmula:
        dinero_final = base_dinero * (1 + nivel * 0.05)
        xp_final = base_xp    * (1 + nivel * 0.03)
    """

    def calcular(
            self, 
            recompensa_base_dinero: int, 
            recompensa_base_xp: int, 
            nivel_jugador: int
        ) -> Recompensa:
        
        factor_dinero = 1 + nivel_jugador * 0.05
        factor_xp = 1 + nivel_jugador * 0.03
        return Recompensa(
            dinero=int(recompensa_base_dinero * factor_dinero),
            experiencia=int(recompensa_base_xp * factor_xp),
        )


class RecompensaBonus(EstrategiaRecompensa):
    """
    Recompensa por bonus: aumenta la recompensa y entrega bonus en caso
    de urgencia
    """

    def __init__(self, bonus_dinero: int = 50, bonus_xp: int = 25) -> None:
        self._bonus_dinero = bonus_dinero
        self._bonus_xp = bonus_xp

    def calcular(
            self, 
            recompensa_base_dinero: int, 
            recompensa_base_xp: int, 
            nivel_jugador: int
            ) -> Recompensa:
        
        return Recompensa(
            dinero=recompensa_base_dinero + self._bonus_dinero,
            experiencia=recompensa_base_xp + self._bonus_xp,
        )
