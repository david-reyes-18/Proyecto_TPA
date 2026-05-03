from componentes.componente import Componente
from componentes.ssd.interfaz_ssd import InterfazSSD
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema

class SSD(Componente):
    def __init__(self, capacidad_gb: int, interfaz: InterfazSSD, velocidad_lectura_mbps: int):
        super().__init__("SSD", es_reemplazable=True, es_reparable=False)
        self._capacidad_gb = capacidad_gb
        self._interfaz = interfaz
        self._velocidad_lectura_mbps = velocidad_lectura_mbps
        self._sectores_danados = 0

    @property
    def capacidad_gb(self) -> int:
        return self._capacidad_gb

    @property
    def interfaz(self) -> InterfazSSD:
        return self._interfaz

    def agregar_sectores_danados(self, porcentaje: int):
        self._sectores_danados = porcentaje
        if self._sectores_danados >= 30:
            self._esta_funcionando = False

    def reparar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion=False,
            codigo_operacion=CodigoOperacion.NO_REPARABLE,
            mensaje_sistema=MensajesSistema.NO_REPARABLE
        )

    def reemplazar(self, nuevo_ssd: SSD, costo: int) -> ResultadoOperacion:
        if self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.COMPONENTE_FUNCIONAL,
                mensaje_sistema=MensajesSistema.COMPONENTE_FUNCIONAL
            )
        if nuevo_ssd.interfaz != self._interfaz:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SSD_INTERFAZ_INCOMPATIBLE,
                mensaje_sistema=MensajesSistema.SSD_INTERFAZ_INCOMPATIBLE
            )
        if nuevo_ssd.capacidad_gb < self._capacidad_gb:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SSD_CAPACIDAD_INSUFICIENTE,
                mensaje_sistema=MensajesSistema.SSD_CAPACIDAD_INSUFICIENTE
            )
        self._capacidad_gb = nuevo_ssd.capacidad_gb
        self._interfaz = nuevo_ssd.interfaz
        self._sectores_danados = 0
        self._esta_funcionando = True
        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_REEMPLAZO,
            mensaje_sistema=MensajesSistema.EXITO_REEMPLAZO,
            costo=costo
        )

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