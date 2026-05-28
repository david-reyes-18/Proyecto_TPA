from abc import ABC, abstractmethod
from sistema.resultado_operaciones import ResultadoOperacion

"""
Interfaz que moldea componentes reparables
"""

class Reparable(ABC):
    
    @abstractmethod
    def reparar(self) -> ResultadoOperacion:
        pass