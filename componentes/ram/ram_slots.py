from __future__ import annotations
from componentes.ram.ram import RAM
from componentes.ram.generacion_ram import GeneracionRAM
from componentes.ram.formato_ram import FormatoRAM
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class RAMSlot:
    
    """
    Clase que moldea una ranura para insertar una memoria RAM
    """
    
    def __init__(
        self, 
        capacidad_maxima_ram: int, 
        capacidad_maxima_mhz: int,
        generacion_compatible: GeneracionRAM,
        formato_compatible: FormatoRAM,
        modulo: RAM | None = None
    ) -> None:
    
        self._capacidad_maxima_ram = capacidad_maxima_ram
        self._capacidad_maxima_mhz = capacidad_maxima_mhz
        self._generacion_compatible = generacion_compatible
        self._formato_compatible = formato_compatible
        self._modulo = modulo
        self._esta_soldada = False
        
        # Sólo estará soldada si el formato es LPDDR
        self._esta_soldada: bool = (
            modulo is not None and modulo.formato == FormatoRAM.LPDDR
        )
    
    
    #   Getters
    
    @property
    def capacidad_maxima_ram(self) -> int:
        return self._capacidad_maxima_ram
    
    @property
    def capacidad_maxima_mhz(self) -> int:
        return self._capacidad_maxima_mhz
    
    @property
    def generacion_compatible(self) -> GeneracionRAM:
        return self._generacion_compatible
    
    @property
    def formato_compatible(self) -> FormatoRAM:
        return self._formato_compatible
    
    @property
    def modulo(self) -> RAM | None:
        return self._modulo
    
    @property
    def esta_soldada(self) -> bool:
        return self._esta_soldada
    
    
    #   Métodos
    
    def esta_ocupado(self) -> bool:
        return self._modulo is not None
    
    def esta_vacio(self) -> bool:
        return self._modulo is None
    
    def ram_compatible(self, nueva_ram: RAM) -> bool:
        return (
            self._formato_compatible == nueva_ram.formato and
            self._generacion_compatible == nueva_ram.generacion and
            self._capacidad_maxima_ram >= nueva_ram.capacidad_gb and
            self._capacidad_maxima_mhz >= nueva_ram.velocidad_mhz
        )
    
    def instalar_ram(self, nueva_ram: RAM) -> ResultadoOperacion:
        if self.esta_ocupado():
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.SLOT_OCUPADO,
                mensaje_sistema = MensajesSistema.SLOT_OCUPADO
            )
        
        if nueva_ram.capacidad_gb > self._capacidad_maxima_ram:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.CAPACIDAD_MAXIMA_GB_EXCEDIDA,
                mensaje_sistema = MensajesSistema.CAPACIDAD_MAXIMA_GB_EXCEDIDA
            )
        
        if not self.ram_compatible(nueva_ram):
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
    
    def remover_ram(self) -> RAM | ResultadoOperacion:
        if self._esta_soldada:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.RAM_SOLDADA,
                mensaje_sistema=MensajesSistema.RAM_SOLDADA
            )
        
        if self.esta_vacio():
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SLOT_VACIO,
                mensaje_sistema=MensajesSistema.SLOT_VACIO
            )
        
        ram_removida = self._modulo
        self._modulo = None
        
        return ram_removida