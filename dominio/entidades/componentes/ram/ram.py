from __future__ import annotations
from dominio.entidades.componentes.base.componente import Componente
from dominio.entidades.componentes.ram.generacion_ram import GeneracionRAM
from dominio.entidades.componentes.ram.formato_ram import FormatoRAM
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class RAM(Componente):
    
    """
    Clase que moldea una RAM para laptop y pc de escritorio
    """
    
    def __init__(
            self, 
            nombre: str, 
            capacidad_gb: int, 
            velocidad_mhz: int,
            generacion: GeneracionRAM, 
            formato: FormatoRAM
        ) -> None:
        
        # Las únicas memorias RAM que no pueden ser reemplazadas
        # son las que tienen el formato LPDDR, las cuales son RAMs
        # soldadas a la placa
        
        es_reemplazable = (formato != FormatoRAM.LPDDR)
        
        super().__init__(nombre, es_reemplazable = es_reemplazable, es_reparable = False)
        
        self._capacidad_gb = capacidad_gb
        self._velocidad_mhz = velocidad_mhz
        self._generacion = generacion
        self._formato = formato
    
    #   Getters
    
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
    
    
    #   Método
    
    def diagnosticar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
        )