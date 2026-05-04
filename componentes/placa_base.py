from componentes.componente import Componente
from componentes.ram.generacion_ram import GeneracionRAM
from componentes.ram.formato_ram import FormatoRAM
from componentes.ram.ram_slots import RAMSlot
from componentes.ssd.ssd_slot import SSDSlot
from componentes.cpu.socket import SocketCPU
from componentes.gpu.tipo_interfaz import InterfazGPU
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

class PlacaBase(Componente):
    def __init__(self, 
                generacion_ram: GeneracionRAM,
                formato_ram: FormatoRAM, 
                slots_ram: list[RAMSlot],
                slots_ssd: list[SSDSlot],
                cantidad_maxima_ram: int,
                socket_compatible: SocketCPU,
                interfaz_gpu_compatible: InterfazGPU
            ):
        
        super().__init__("Placa Base", es_reemplazable = False, es_reparable = False)
        self._generacion_ram = generacion_ram
        self._formato_ram = formato_ram
        self._slots_ram = slots_ram
        self._slots_ssd = slots_ssd
        self._cantidad_maxima_ram = cantidad_maxima_ram
        self._socket_compatible = socket_compatible
        self._interfaz_gpu_compatible = interfaz_gpu_compatible
    
    @property
    def generacion_ram(self) -> GeneracionRAM:
        return self._generacion_ram
    
    @property
    def formato_ram(self) -> FormatoRAM:
        return self._formato_ram
    
    @property
    def slots_ram(self) -> list[RAMSlot]:
        return self._slots_ram
    
    @property
    def slots_ssd(self) -> list[SSDSlot]:
        return self._slots_ssd
    
    @property
    def cantidad_maxima_ram(self) -> int:
        return self._cantidad_maxima_ram
    
    @property
    def socket_compatible(self) -> SocketCPU:
        return self._socket_compatible
    
    @property
    def interfaz_gpu_compatible(self) -> InterfazGPU:
        return self._interfaz_gpu_compatible
    
    def cantidad_ram_por_slot(self) -> int:
        return self._cantidad_maxima_ram // self._slots_ram
    
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