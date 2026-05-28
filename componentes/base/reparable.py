from abc import ABC, abstractmethod
from sistema.resultado_operaciones import ResultadoOperacion


class Reparable(ABC):
    
    """
    Interfaz que moldea componentes reparables
    """
    
    @abstractmethod
    def reparar(self) -> ResultadoOperacion:
        pass