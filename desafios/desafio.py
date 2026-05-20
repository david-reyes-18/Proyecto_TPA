from abc import ABC, abstractmethod
from desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from sistema.resultado_operaciones import ResultadoOperacion
from desafios.dificultad_desafio import NivelDificultad


class Desafio(ABC):
    def __init__(
        self, 
        enunciado: str, 
        tipo: NombreTipoDesafio, 
        dificultad: NivelDificultad = NivelDificultad.FACIL
    ):
        self._enunciado = enunciado.strip()
        self._tipo = tipo
        self._dificultad = dificultad

    #   Propiedades

    @property
    def enunciado(self) -> str:
        return self._enunciado

    @property
    def tipo(self) -> NombreTipoDesafio:
        return self._tipo
    
    @property
    def dificultad(self) -> NivelDificultad:
        return self._dificultad

    #   Método

    @abstractmethod
    def verificar_respuesta(self, respuesta_usuario) -> ResultadoOperacion:
        pass
