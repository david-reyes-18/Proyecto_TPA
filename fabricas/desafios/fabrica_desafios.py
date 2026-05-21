from abc import ABC, abstractmethod
from desafios.categoria_desafio import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico
from desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from desafios.dificultad_desafio import NivelDificultad
from desafios.desafio import Desafio

class FabricaDesafios(ABC):
    @staticmethod
    @abstractmethod
    def crear_desafio(
        categoria: CategoriaDesafio,
        componente: ComponenteTematico,
        tipo: NombreTipoDesafio,
        dificultad: NivelDificultad
    ) -> Desafio:
        pass