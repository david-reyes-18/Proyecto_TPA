from dominio.entidades.desafios.desafio import Desafio
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class TipoBooleano(Desafio):
    def __init__(
        self, 
        enunciado: str, 
        respuesta: bool,
        dificultad: NivelDificultad = NivelDificultad.FACIL
    ):
        super().__init__(enunciado, NombreTipoDesafio.BOOLEANO, dificultad)
        self._respuesta = respuesta

    #   Propiedades

    @property
    def respuesta(self) -> bool:
        return self._respuesta

    # ── Verificación ─────────────────────────────────────────────────────────

    def verificar_respuesta(self, respuesta_usuario) -> ResultadoOperacion:

        if self._respuesta == respuesta_usuario:
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
