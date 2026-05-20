from desafios.tipo_desafio.tipo_multiple  import TipoMultiple
from desafios.dificultad_desafio import NivelDificultad
from desafios.categoria_desafio   import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico


class DesafioTecnologicoMultiple(TipoMultiple):
    def __init__(
        self,
        enunciado: str,
        alternativas: list[str],
        indice_correcto: int,
        componente: ComponenteTematico = ComponenteTematico.GENERAL,
        dificultad: NivelDificultad = NivelDificultad.FACIL
    ):
        super().__init__(enunciado, alternativas, indice_correcto, dificultad)
        self._categoria  = CategoriaDesafio.TECNOLOGICO
        self._componente = componente

    @property
    def categoria(self) -> CategoriaDesafio:
        return self._categoria

    @property
    def componente(self) -> ComponenteTematico:
        return self._componente