from dominio.entidades.desafios.desafio import Desafio
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class TipoMultiple(Desafio):
    def __init__(
        self,
        enunciado: str,
        alternativas: list[str],
        indice_correcto: int,
        dificultad: NivelDificultad = NivelDificultad.FACIL
        
    ):
        super().__init__(enunciado, NombreTipoDesafio.MULTIPLE, dificultad)

        self._alternativas = [a.strip() for a in alternativas]
        self._indice_correcto = indice_correcto

    @property
    def alternativas(self) -> list[str]:
        return list(self._alternativas)

    @property
    def indice_correcto(self) -> int:
        return self._indice_correcto

    @property
    def respuesta_correcta(self) -> str:
        return self._alternativas[self._indice_correcto]

    def verificar_respuesta(self, respuesta_usuario: int) -> ResultadoOperacion:
        if respuesta_usuario == self._indice_correcto:
            return ResultadoOperacion(
                exito_operacion=True,
                codigo_operacion=CodigoOperacion.RESPUESTA_CORRECTA,
                mensaje_sistema=MensajesSistema.RESPUESTA_CORRECTA,
            )
        return ResultadoOperacion(
            exito_operacion=False,
            codigo_operacion=CodigoOperacion.RESPUESTA_INCORRECTA,
            mensaje_sistema=MensajesSistema.RESPUESTA_INCORRECTA,
        )