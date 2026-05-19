from desafios.tipo_desafio.tipo_booleano  import TipoBooleano
from desafios.categoria_desafio   import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico

class DesafioLogicoBooleano(TipoBooleano):
    def __init__(
        self,
        enunciado: str,
        respuesta: bool,
        componente: ComponenteTematico = ComponenteTematico.GENERAL,
    ):
        super().__init__(enunciado, respuesta)
        self._categoria  = CategoriaDesafio.LOGICO
        self._componente = componente

    @property
    def categoria(self) -> CategoriaDesafio:
        return self._categoria

    @property
    def componente(self) -> ComponenteTematico:
        return self._componente