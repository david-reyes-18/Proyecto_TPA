from desafios.tipo_desafio.tipo_multiple  import TipoMultiple
from desafios.categoria_desafio   import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico

class DesafioLogicoMultiple(TipoMultiple):
    def __init__(
        self,
        enunciado: str,
        alternativas: list[str],
        indice_correcto: int,
        componente: ComponenteTematico = ComponenteTematico.GENERAL,
    ):
        super().__init__(enunciado, alternativas, indice_correcto)
        self._categoria  = CategoriaDesafio.LOGICO
        self._componente = componente

    @property
    def categoria(self) -> CategoriaDesafio:
        return self._categoria

    @property
    def componente(self) -> ComponenteTematico:
        return self._componente