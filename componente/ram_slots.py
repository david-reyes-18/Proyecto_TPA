from componente.ram import RAM
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

class RAMSlot:
    def __init__(
        self, capacidad_maxima_ram: int, 
        capacidad_maxima_mhz: int,
        tipo_compatible: str, 
        modulo: RAM | None = None
    ):
    
        self._capacidad_maxima_ram = capacidad_maxima_ram
        self._capacidad_maxima_mhz = capacidad_maxima_mhz
        self._tipo_compatible = tipo_compatible
        self._modulo = modulo
    
    @property
    def capacidad_maxima_ram(self) -> int:
        return self._capacidad_maxima_ram
    
    @property
    def capacidad_maxima_mhz(self) -> int:
        return self._capacidad_maxima_mhz
    
    @property
    def tipo_compatible(self) -> str:
        return self._tipo_compatible
    
    @property
    def modulo(self) -> RAM | None:
        return self._modulo
    
    def instalar_ram(self, nueva_ram: RAM) -> ResultadoOperacion:
        if self._modulo is not None:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.SLOP_OCUPADO,
                mensaje_sistema = MensajesSistema.SLOT_OCUPADO
            )
        
        if nueva_ram.capacidad_gb > self._capacidad_maxima_ram:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.CAPACIDAD_MAXIMA_GB_EXCEDIDA,
                mensaje_sistema = MensajesSistema.CAPACIDAD_MAXIMA_GB_EXCEDIDA
            )
        
        if nueva_ram.tipo.lower() != self._tipo_compatible.lower():
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.RAM_INCOMPATIBLE,
                mensaje_sistema = MensajesSistema.RAM_INCOMPATIBLE
            )
        
        self._modulo = nueva_ram
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.EXITO_INSTALACION,
            mensaje_sistema = MensajesSistema.EXITO_INSTALACION
        )
    
    def remover_ram(self) -> RAM | None:
        ram_removida = self._modulo
        self._modulo = None
        return ram_removida