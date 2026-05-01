from componente.componente import Componente
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

class RAM(Componente):
    def __init__(self, nombre: str, 
                capacidad_gb: int, 
                velocidad_mhz: int, 
                tipo: str
        ):
        super().__init__(nombre, es_reemplazable = True, es_reparable = False)
        self._capacidad_gb = capacidad_gb
        self._velocidad_mhz = velocidad_mhz
        self._tipo = tipo
        
    @property
    def capacidad_gb(self) -> int:
        return self._capacidad_gb
    
    @property
    def velocidad_mhz(self) -> int:
        return self._velocidad_mhz
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    def reparar(self)-> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = False,
            codigo_operacion = CodigoOperacion.SIN_REPARACION,
            mensaje_sistema = MensajesSistema.ERROR_NO_REPARABLE
        )
    
    def reemplazar(self, nueva_ram: RAM) -> ResultadoOperacion:
        self._capacidad_gb = nueva_ram.capacidad_gb
        self._velocidad_mhz = nueva_ram.velocidad_mhz
        self._tipo = nueva_ram.tipo
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.EXITO,
            mensaje_sistema = MensajesSistema.EXITO_REEMPLAZO
        )
    
    def diagnosticar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
        )