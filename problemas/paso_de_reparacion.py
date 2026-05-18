from desafios.desafio import Desafio
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class PasoDeReparacion:
    def __init__(self, descripcion_accion: str, explicacion: str, desafio: Desafio):
        self._descripcion_accion = descripcion_accion
        self._explicacion = explicacion
        self._desafio = desafio
        self._completado = False
        
    #   Propiedades
        
    @property
    def descripcion_accion(self) -> str:
        return self._descripcion_accion
    
    @property
    def explicacion(self) -> str:
        return self._explicacion
    
    @property
    def desafio(self) -> Desafio:
        return self._desafio
    
    @property
    def completado(self) -> bool:
        return self._completado
    
    
    #   Metodos
    
    def verificar_respuesta(self, respuesta_usuario: float) -> ResultadoOperacion:
        if respuesta_usuario == self._desafio.respuesta:
            self._completado = True
            return ResultadoOperacion(
                exito_operacion=True,
                codigo_operacion=CodigoOperacion.RESPUESTA_CORRECTA,
                mensaje_sistema=MensajesSistema.RESPUESTA_CORRECTA
            )
        return ResultadoOperacion(
            exito_operacion=False,
            codigo_operacion=CodigoOperacion.RESPUESTA_INCORRECTA,
            mensaje_sistema=MensajesSistema.RESPUESTA_INCORRECTA
        )