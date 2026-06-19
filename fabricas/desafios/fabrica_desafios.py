from abc import ABC, abstractmethod
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.componente_tematico import ComponenteTematico
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.entidades.desafios.desafio import Desafio

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