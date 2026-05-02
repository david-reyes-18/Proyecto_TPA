from componente.ssd.ssd import SSD
from componente.ssd.interfaz_ssd import InterfazSSD
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class SSDSlot:
    def __init__(self, interfaz_soportada: InterfazSSD, ssd_instalado: SSD = None):
        self._interfaz_soportada = interfaz_soportada
        self._ssd_instalado = ssd_instalado

    @property
    def interfaz_soportada(self) -> InterfazSSD:
        return self._interfaz_soportada

    @property
    def ssd_instalado(self) -> SSD | None:
        return self._ssd_instalado

    def esta_ocupado(self) -> bool:
        return self._ssd_instalado is not None

    def esta_vacio(self) -> bool:
        return self._ssd_instalado is None

    def instalar_ssd(self, nuevo_ssd: SSD) -> ResultadoOperacion:
        if self.esta_ocupado():
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SLOT_OCUPADO,
                mensaje_sistema=MensajesSistema.SLOT_OCUPADO
            )

        if nuevo_ssd.interfaz != self._interfaz_soportada:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SSD_INTERFAZ_INCOMPATIBLE,
                mensaje_sistema=MensajesSistema.SSD_INTERFAZ_INCOMPATIBLE
            )

        self._ssd_instalado = nuevo_ssd
        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_INSTALACION,
            mensaje_sistema=MensajesSistema.EXITO_INSTALACION
        )

    def reemplazar_ssd(self, nuevo_ssd: SSD, costo: int) -> ResultadoOperacion:
        if self.esta_vacio():
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SLOT_VACIO,
                mensaje_sistema=MensajesSistema.SLOT_VACIO
            )

        resultado = self._ssd_instalado.reemplazar(nuevo_ssd, costo)
        if resultado.exito_operacion:
            self._ssd_instalado = nuevo_ssd

        return resultado

    def remover_ssd(self) -> ResultadoOperacion:
        if self.esta_vacio():
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SLOT_VACIO,
                mensaje_sistema=MensajesSistema.SLOT_VACIO
            )

        self._ssd_instalado = None
        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_REMOCION,
            mensaje_sistema=MensajesSistema.EXITO_REMOCION
        )

    def diagnosticar(self) -> ResultadoOperacion:
        if self.esta_vacio():
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.SLOT_VACIO,
                mensaje_sistema=MensajesSistema.SLOT_VACIO
            )

        return self._ssd_instalado.diagnosticar()