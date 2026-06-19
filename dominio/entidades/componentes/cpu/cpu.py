from __future__ import annotations
from dominio.entidades.componentes.base.componente import Componente
from dominio.entidades.componentes.cpu.socket import SocketCPU
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class CPU(Componente):
    
    """
    Clase que moldea una CPU para laptops y pc de escritorio
    """
    
    def __init__(
            self, 
            modelo: str, 
            nucleos: int, 
            frecuencia_ghz: float,
            socket: SocketCPU,
            tdp_watts: int,
        ) -> None:
        
        # Sockets tipo BGA (Ball Grid Array) es un montaje para dejar soldada
        # de por vida el procesador, usado para laptops
        
        es_reemplazable: bool = (socket != SocketCPU.BGA)
        
        super().__init__("CPU", es_reemplazable = es_reemplazable, es_reparable = False)
        
        self._modelo = modelo
        self._nucleos = nucleos
        self._frecuencia_ghz = frecuencia_ghz
        self._socket = socket
        self._tdp_watts = tdp_watts
    
    #   Getters
    
    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def nucleos(self) -> int:
        return self._nucleos

    @property
    def frecuencia_ghz(self) -> float:
        return self._frecuencia_ghz
    
    @property
    def socket(self) -> SocketCPU:
        return self._socket
    
    @property
    def tdp_watts(self) -> int:
        return self._tdp_watts

    
    #   Metodos
    
    #TODO: realizar funcion recibir pasta termica y crear clase pasta termica 
    #def aplicar_pasta_termica(self) -> ResultadoOperacion:
    #    return ResultadoOperacion(
    #        exito_operacion = True,
    #        codigo_operacion = CodigoOperacion.EXITO_REPARACION,
    #        mensaje_sistema = MensajesSistema.EXITO_REPARACION
    #    )
    
    def diagnosticar(self) -> ResultadoOperacion:
        if not self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion = CodigoOperacion.CPU_SOBRECALENTADO,
                mensaje_sistema = MensajesSistema.CPU_SOBRECALENTADO
            )
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
        )