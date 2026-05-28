from abc import ABC, abstractmethod
from sistema.resultado_operaciones import ResultadoOperacion


class Componente(ABC):
    
    """
    La clase abstarcta de Componente se encarga de darle un comportamiento básico
    a cada componente creado, los cuales son un nombre, ver si el componente
    es reemplazable o reparable, asi mismo si está funcionando o existe alguna fala. 
    Por último, cada componente debe tener el método abstracto diagnosticar.
    """
    
    def __init__(
        self, 
        nombre: str, 
        es_reemplazable: bool, 
        es_reparable: bool
    ) -> None:
        
        self._nombre = nombre
        self._es_reemplazable = es_reemplazable
        self._es_reparable = es_reparable
        self._esta_funcionando: bool = True
    
    
    #   Getters    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def es_reemplazable(self) -> bool:
        return self._es_reemplazable
    
    @property
    def es_reparable(self) -> bool:
        return self._es_reparable
    
    @property
    def esta_funcionando(self) -> bool:
        return self._esta_funcionando
    
    #   Setter
    
    @esta_funcionando.setter
    def esta_funcionando(self, nuevo_estado: bool) -> None:
        self._esta_funcionando = nuevo_estado

    #   Métodos
    
    @abstractmethod
    def diagnosticar(self) -> ResultadoOperacion:
        pass