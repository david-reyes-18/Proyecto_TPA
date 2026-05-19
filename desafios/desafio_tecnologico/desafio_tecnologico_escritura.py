from desafios.tipo_desafio.tipo_escritura import TipoEscritura
from desafios.categoria_desafio   import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico


class DesafioTecnologicoEscritura(TipoEscritura):
    def __init__(
        self,
        enunciado: str,
        respuesta: int | float | str,
        componente: ComponenteTematico = ComponenteTematico.GENERAL,
        tolerancia: float = 0.0,
        ignorar_mayusculas: bool = True,
    ):
        super().__init__(enunciado, respuesta, tolerancia, ignorar_mayusculas)
        self._categoria  = CategoriaDesafio.TECNOLOGICO
        self._componente = componente

    @property
    def categoria(self) -> CategoriaDesafio:
        return self._categoria

    @property
    def componente(self) -> ComponenteTematico:
        return self._componente
