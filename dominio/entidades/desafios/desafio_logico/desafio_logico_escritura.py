from dominio.entidades.desafios.tipo_desafio.tipo_escritura import TipoEscritura
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.componente_tematico import ComponenteTematico


class DesafioLogicoEscritura(TipoEscritura):
    def __init__(
        self,
        enunciado: str,
        respuesta: int | float,
        componente: ComponenteTematico = ComponenteTematico.GENERAL,
        dificultad: NivelDificultad = NivelDificultad.FACIL,
        tolerancia: float = 0.0,
    ):
        super().__init__(enunciado, respuesta, tolerancia, dificultad)
        self._categoria  = CategoriaDesafio.LOGICO
        self._componente = componente

    @property
    def categoria(self) -> CategoriaDesafio:
        return self._categoria

    @property
    def componente(self) -> ComponenteTematico:
        return self._componente
