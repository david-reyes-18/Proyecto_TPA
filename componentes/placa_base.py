from componentes.componente import Componente
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

class PlacaBase(Componente):
    def __init__(self, tipo_ram: str, cantidad_slots: int, cantidad_maxima_ram: int):
        super().__init__("Placa Base", es_reemplazable = False, es_reparable = False)
        self._tipo_ram = tipo_ram
        self._cantidad_slots = cantidad_slots
        self._cantidad_maxima_ram = cantidad_maxima_ram
    
    @property
    def tipo_ram(self) -> str:
        return self._tipo_ram
    
    @property
    def cantidad_slots(self) -> int:
        return self._cantidad_slots
    
    @property
    def cantidad_maxima_ram(self) -> int:
        return self._cantidad_maxima_ram
    
    def cantidad_ram_por_slot(self) -> int:
        return self._cantidad_maxima_ram // self._cantidad_slots
    
    def reparar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = False,
            codigo_operacion = CodigoOperacion.NO_REPARABLE,
            mensaje_sistema = MensajesSistema.NO_REPARABLE
        )
    
    def reemplazar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = False,
            codigo_operacion = CodigoOperacion.NO_REEMPLAZABLE,
            mensaje_sistema = MensajesSistema.NO_REEMPLAZABLE
        )
    
    def diagnosticar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
        )