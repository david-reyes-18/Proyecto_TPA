from dominio.entidades.desafios.desafio import Desafio
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class TipoEscritura(Desafio):
    def __init__(
        self,
        enunciado: str,
        respuesta: int | float,
        tolerancia: float = 0.0,
        dificultad: NivelDificultad = NivelDificultad.FACIL
    ):
        super().__init__(enunciado, NombreTipoDesafio.ESCRITURA, dificultad)
        
        self._respuesta = respuesta
        self._tolerancia = tolerancia

    #   Propiedades

    @property
    def respuesta(self) -> int | float:
        return self._respuesta

    @property
    def tolerancia(self) -> float:
        return self._tolerancia

    #   Verificación 

    def verificar_respuesta(self, respuesta_usuario) -> ResultadoOperacion:
        if abs(respuesta_usuario - float(self._respuesta)) <= self._tolerancia:
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
