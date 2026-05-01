from componente.componente import Componente
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

class Pantalla(Componente):
    def __init__(self, pulgadas: int, resolucion: str):
        super().__init__("Pantalla", es_reemplazable = True, es_reparable = False)
        self._pulgadas = pulgadas
        self._resolucion = resolucion
    
    @property
    def pulgadas(self) -> int:
        return self._pulgadas
    
    @property
    def resolucion(self) -> str:
        return self._resolucion
    
    def reemplazar(self, nueva_pantalla: Pantalla, costo: int) -> ResultadoOperacion:
        if self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
                mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
            )
        
        if nueva_pantalla.pulgadas != self._pulgadas:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.TAMANO_PANTALLA_INCORRECTA,
                mensaje_sistema = MensajesSistema.TAMANO_PANTALLA_INCORRECTA
            )
        
        self._esta_funcionando = True
        
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.EXITO_REEMPLAZO,
            mensaje_sistema = MensajesSistema.EXITO_REEMPLAZO,
            costo = costo
        )
    
    def reparar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = False,
            codigo_operacion = CodigoOperacion.NO_REPARABLE,
            mensaje_sistema = MensajesSistema.NO_REPARABLE
        )
    
    def diagnosticar(self) -> ResultadoOperacion:
        if not self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.PANTALLA_ROTA,
                mensaje_sistema = MensajesSistema.PANTALLA_ROTA
            )
        
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
        )