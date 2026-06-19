from dominio.entidades.desafios.tipo_desafio.tipo_booleano import TipoBooleano
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.componente_tematico import ComponenteTematico

class DesafioMatematicoBooleano(TipoBooleano):
    def __init__(
        self,
        enunciado: str,
        respuesta: bool,
        componente: ComponenteTematico = ComponenteTematico.GENERAL,
        dificultad: NivelDificultad = NivelDificultad.FACIL
    ):
        super().__init__(enunciado, respuesta, dificultad)
        self._categoria  = CategoriaDesafio.MATEMATICO
        self._componente = componente

    @property
    def categoria(self) -> CategoriaDesafio:
        return self._categoria

    @property
    def componente(self) -> ComponenteTematico:
        return self._componente