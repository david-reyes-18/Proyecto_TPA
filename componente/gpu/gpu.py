from componente.componente import Componente
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

from componente.gpu.tipo_gpu import TipoGPU
from componente.gpu.tipo_memoria_gpu import TipoMemoriaGPU
from componente.gpu.tipo_interfaz import InterfazGPU

class GPU(Componente):
    def __init__(self, 
                modelo: str, 
                memoria_gb: int, 
                tipo_memoria: TipoMemoriaGPU, 
                tipo_gpu: TipoGPU,
                interfaz: InterfazGPU,
            ):
        super().__init__("GPU", es_reparable = False)
        self._modelo = modelo
        self._memoria_gb = memoria_gb
        self._tipo_memoria = tipo_memoria
        self._tipo_gpu = tipo_gpu
        self._interfaz = interfaz
        
        self._es_reemplazable = (
            tipo_gpu == TipoGPU.DEDICADA and
            interfaz == InterfazGPU.PCIe
        )       


    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def memoria_gb(self) -> int:
        return self._memoria_gb

    @property
    def tipo_memoria(self) -> TipoMemoriaGPU:
        return self._tipo_memoria

    @property
    def tipo_gpu(self) -> TipoGPU:
        return self._tipo_gpu
    
    @property
    def interfaz(self) -> InterfazGPU:
        return self._interfaz
    
    def compatible(self, nueva_gpu: GPU) -> bool:
        return (
            self._tipo_memoria == nueva_gpu.tipo_memoria and
            self._tipo_gpu == nueva_gpu.tipo_gpu and
            self._interfaz == nueva_gpu.interfaz
        )

    def reparar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion=False,
            codigo_operacion=CodigoOperacion.NO_REPARABLE,
            mensaje_sistema=MensajesSistema.NO_REPARABLE
        )

    def reemplazar(self, nueva_gpu: GPU, costo: int) -> ResultadoOperacion:
        if not self._es_reemplazable:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.NO_REEMPLAZABLE,
                mensaje_sistema=MensajesSistema.NO_REEMPLAZABLE
            )

        if self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.COMPONENTE_FUNCIONAL,
                mensaje_sistema=MensajesSistema.COMPONENTE_FUNCIONAL
            )

        if self.compatible(nueva_gpu):
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.GPU_INCOMPATIBLE,
                mensaje_sistema=MensajesSistema.GPU_INCOMPATIBLE
            )

        self._modelo = nueva_gpu.modelo
        self._memoria_gb = nueva_gpu.memoria_gb
        self._tipo_memoria = nueva_gpu.tipo_memoria
        self._tipo_gpu = nueva_gpu.tipo_gpu
        self._interfaz = nueva_gpu.interfaz
        self._esta_funcionando = True

        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_REEMPLAZO,
            mensaje_sistema=MensajesSistema.EXITO_REEMPLAZO
        )

    def diagnosticar(self) -> ResultadoOperacion:
        if not self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.GPU_FALLA,
                mensaje_sistema=MensajesSistema.GPU_FALLA
            )

        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema=MensajesSistema.COMPONENTE_FUNCIONAL
        )