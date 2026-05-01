from componente.componente import Componente
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class CPU(Componente):
    def __init__(self, 
                modelo: str, 
                nucleos: int, 
                frecuencia_ghz: float, 
                es_reemplazable: bool):
        super().__init__("CPU", es_reemplazable=es_reemplazable, es_reparable=False)
        self._modelo = modelo
        self._nucleos = nucleos
        self._frecuencia_ghz = frecuencia_ghz

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def nucleos(self) -> int:
        return self._nucleos

    @property
    def frecuencia_ghz(self) -> float:
        return self._frecuencia_ghz

    def aplicar_pasta_termica(self) -> ResultadoOperacion:
        if not self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.CPU_SOBRECALENTADO,
                mensaje_sistema=MensajesSistema.CPU_SOBRECALENTADO
            )
        
        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_REPARACION,
            mensaje_sistema=MensajesSistema.EXITO_REPARACION
        )

    def reparar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion=False,
            codigo_operacion=CodigoOperacion.NO_REPARABLE,
            mensaje_sistema=MensajesSistema.NO_REPARABLE
        )

    def reemplazar(self, nuevo_cpu: CPU, costo: int) -> ResultadoOperacion:
        if not self._es_reemplazable:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.NO_REEMPLAZABLE,
                mensaje_sistema=MensajesSistema.NO_REEMPLAZABLE
            )
        
        if nuevo_cpu.nucleos < self._nucleos:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.CPU_INCOMPATIBLE,
                mensaje_sistema=MensajesSistema.CPU_INCOMPATIBLE
            )

        self._modelo = nuevo_cpu.modelo
        self._nucleos = nuevo_cpu.nucleos
        self._frecuencia_ghz = nuevo_cpu.frecuencia_ghz
        self._esta_funcionando = True

        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_REEMPLAZO,
            mensaje_sistema=MensajesSistema.EXITO_REEMPLAZO,
            costo = costo
        )
    
    def diagnosticar(self) -> ResultadoOperacion:
        if not self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.CPU_SOBRECALENTADO,
                mensaje_sistema=MensajesSistema.CPU_SOBRECALENTADO
            )

        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema=MensajesSistema.COMPONENTE_FUNCIONAL
        )