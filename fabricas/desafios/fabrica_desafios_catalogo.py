import random
from fabricas.desafios.catalogo_desafios import CATALOGO
from desafios.desafio import Desafio
from desafios.categoria_desafio import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico
from desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from desafios.dificultad_desafio import NivelDificultad
from .fabrica_desafios import FabricaDesafios

class FabricaDesafiosCatalogo(FabricaDesafios):
    @staticmethod
    def crear_desafio(
        categoria: CategoriaDesafio,
        componente: ComponenteTematico,
        tipo: NombreTipoDesafio,
        dificultad: NivelDificultad
    ) -> Desafio:
        pool = CATALOGO[componente][categoria][tipo]
        candidatos = [d for d in pool if d.dificultad == dificultad]

        if not candidatos:
            raise ValueError(
                f"No hay desafíos para {categoria.value} / {componente.value} / "
                f"{tipo.value} / {dificultad.value}"
            )

        return random.choice(candidatos)