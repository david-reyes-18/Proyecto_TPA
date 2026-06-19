from abc import ABC, abstractmethod
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.componente_tematico import ComponenteTematico


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
    
    @property
    @abstractmethod
    def categoria(self) -> CategoriaDesafio:
        pass

    @property
    @abstractmethod
    def componente(self) -> ComponenteTematico:
        pass
