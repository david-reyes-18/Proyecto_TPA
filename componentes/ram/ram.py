from __future__ import annotations
from componentes.componente import Componente
from componentes.ram.generacion_ram import GeneracionRAM
from componentes.ram.formato_ram import FormatoRAM
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

class RAM(Componente):
    def __init__(self, 
                nombre: str, 
                capacidad_gb: int, 
                velocidad_mhz: int,
                generacion: GeneracionRAM, 
                formato: FormatoRAM
        ):
        
        es_reemplazable = (formato != FormatoRAM.LPDDR)
        
        super().__init__(nombre, es_reemplazable = es_reemplazable, es_reparable = False)
        
        self._capacidad_gb = capacidad_gb
        self._velocidad_mhz = velocidad_mhz
        self._generacion = generacion
        self._formato = formato
    
    #   Propiedades
    
    @property
    def capacidad_gb(self) -> int:
        return self._capacidad_gb
    
    @property
    def velocidad_mhz(self) -> int:
        return self._velocidad_mhz
    
    @property
    def generacion(self) -> str:
        return self._generacion
    
    @property
    def formato(self):
        return self._formato
    
    
    #   Metodos
    
    def reparar(self)-> ResultadoOperacion:
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