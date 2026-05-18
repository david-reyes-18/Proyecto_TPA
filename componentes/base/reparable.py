from abc import ABC, abstractmethod
from sistema.resultado_operaciones import ResultadoOperacion


class Reparable(ABC):

    @abstractmethod
    def reparar(self) -> ResultadoOperacion:
        pass