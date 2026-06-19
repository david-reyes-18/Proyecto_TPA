from dominio.entidades.componentes.base.componente import Componente
from dominio.entidades.componentes.ssd.interfaz_ssd import InterfazSSD
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class SSD(Componente):
    
    """
    Clase encargada de modelar un SSD
    """
    
    def __init__(
        self,
        modelo: str,
        capacidad_gb: int, 
        interfaz: InterfazSSD, 
        velocidad_lectura_mbps: int,
        velocidad_escritura_mbps: int
    ) -> None:
        
        super().__init__("SSD", es_reemplazable=True, es_reparable=False)
        
        self._modelo = modelo
        self._capacidad_gb = capacidad_gb
        self._interfaz = interfaz
        self._velocidad_lectura_mbps = velocidad_lectura_mbps
        self._velocidad_escritura_mbps = velocidad_escritura_mbps
        self._sectores_danados = 0

    #   Getters
    
    @property
    def modelo(self) -> str:
        return self._modelo
    
    @property
    def capacidad_gb(self) -> int:
        return self._capacidad_gb

    @property
    def interfaz(self) -> InterfazSSD:
        return self._interfaz
    
    @property
    def velocidad_lectura_mbps(self) -> int:
        return self._velocidad_lectura_mbps
    
    @property
    def velocidad_escritura_mbps(self) -> int:
        return self._velocidad_escritura_mbps
    
    @property
    def sectores_danados(self) -> int:
        return self._sectores_danados
    
    #   Metodos
    
    def agregar_sectores_danados(self, porcentaje: int):
        self._sectores_danados = porcentaje
        if self._sectores_danados >= 30:
            self._esta_funcionando = False
    
    
    def diagnosticar(self) -> ResultadoOperacion:
        if not self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SSD_DANADO,
                mensaje_sistema=MensajesSistema.SSD_DANADO
            )
        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema=MensajesSistema.COMPONENTE_FUNCIONAL
        )