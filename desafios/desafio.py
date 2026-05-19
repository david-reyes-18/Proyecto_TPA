from abc import ABC, abstractmethod
from desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from sistema.resultado_operaciones import ResultadoOperacion


class Desafio(ABC):
    def __init__(self, enunciado: str, tipo: NombreTipoDesafio):
        self._enunciado = enunciado.strip()
        self._tipo = tipo

    #   Propiedades

    @property
    def enunciado(self) -> str:
        return self._enunciado

    @property
    def tipo(self) -> NombreTipoDesafio:
        return self._tipo

    #   Método

    @abstractmethod
    def verificar_respuesta(self, respuesta_usuario) -> ResultadoOperacion:
        pass
