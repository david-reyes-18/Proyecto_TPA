from desafios.tipo_desafio.tipo_escritura import TipoEscritura
from desafios.dificultad_desafio import NivelDificultad
from desafios.categoria_desafio   import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico


class DesafioTecnologicoEscritura(TipoEscritura):
    def __init__(
        self,
        enunciado: str,
        respuesta: int | float | str,
        componente: ComponenteTematico = ComponenteTematico.GENERAL,
        tolerancia: float = 0.0,
        dificultad: NivelDificultad = NivelDificultad.FACIL
    ):
        super().__init__(enunciado, respuesta, tolerancia, dificultad)
        self._categoria  = CategoriaDesafio.TECNOLOGICO
        self._componente = componente

    @property
    def categoria(self) -> CategoriaDesafio:
        return self._categoria

    @property
    def componente(self) -> ComponenteTematico:
        return self._componente
