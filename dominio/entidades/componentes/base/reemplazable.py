from abc import ABC, abstractmethod
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.entidades.componentes.base.componente import Componente


class Reemplazable(ABC):
    
    """
    Interfaz que moldea componentes reemplazables
    """
    
    @abstractmethod
    def reemplazar(self, nuevo_componente: Componente, costo: int) -> ResultadoOperacion:
        pass