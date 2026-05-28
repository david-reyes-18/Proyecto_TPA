from abc import ABC, abstractmethod
from sistema.resultado_operaciones import ResultadoOperacion
from componentes.base.componente import Componente

"""
Interfaz que moldea componentes reemplazables
"""

class Reemplazable(ABC):
    
    @abstractmethod
    def reemplazar(self, nuevo_componente: Componente, costo: int) -> ResultadoOperacion:
        pass