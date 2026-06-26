from __future__ import annotations
from dominio.entidades.dispositivos.dispositivo import Dispositivo
from dominio.entidades.problemas.problema import Problema
from dominio.entidades.problemas.paso_de_reparacion import PasoDeReparacion
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class ServicioReparacion:
    """
    Orquesta el reparo de dispositivos.
    """
    
    def obtener_paso_actual(self, problema: Problema) -> PasoDeReparacion | None:
        """Devuelve el primer paso pendiente o None si ya terminó."""
        for paso in problema.pasos_de_reparacion:
            if not paso.completado:
                return paso
        return None

    def obtener_descripcion_paso_actual(self, problema: Problema) -> str:
        paso = self.obtener_paso_actual(problema)
        if paso is None:
            return "Reparación completada."
        return paso.descripcion_accion

    def progreso(self, problema: Problema) -> tuple[int, int]:
        """
        Retorna (pasos_completados, total_pasos).
        """
        completados = sum(1 for paso in problema.pasos_de_reparacion if paso.completado)
        return completados, problema.cantidad_pasos

    def porcentaje_avance(self, problema: Problema) -> float:
        completados, total = self.progreso(problema)
        if total == 0:
            return 100.0
        return (completados / total) * 100.0

    def responder_paso(
        self,
        paso: PasoDeReparacion,
        respuesta_usuario: bool | int | float | str,
    ) -> ResultadoOperacion:
        """
        Valida la respuesta del jugador contra el desafío del paso.
        Delega en PasoDeReparacion.verificar_respuesta, que a su vez
        delega en Desafio (cadena TipoBooleano / TipoMultiple / TipoEscritura).
        """
        if paso.completado:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="Este paso ya fue completado.",
            )
        return paso.verificar_respuesta(respuesta_usuario)

    def reparacion_completa(self, problema: Problema) -> bool:
        return all(paso.completado for paso in problema.pasos_de_reparacion)

    def finalizar(self, dispositivo: Dispositivo) -> ResultadoOperacion:
        """
        Marca el dispositivo como reparado si todos los pasos están completos.
        """
        problema = dispositivo.problema

        if not self.reparacion_completa(problema):
            completados, total = self.progreso(problema)
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema=(
                    f"Aún faltan pasos por completar ({completados}/{total})."
                ),
            )

        if dispositivo.esta_reparado:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="Este dispositivo ya fue reparado.",
            )

        dispositivo.marcar_reparado()

        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_REPARACION,
            mensaje_sistema=MensajesSistema.EXITO_REPARACION,
            experiencia=self._calcular_experiencia_paso(problema),
        )

    def reiniciar(self, problema: Problema) -> None:
        """Reinicia todos los pasos. Útil si el jugador abandona el taller."""
        problema.reiniciar_pasos()

    def _calcular_experiencia_paso(self, problema: Problema) -> int:
        """XP base por completar una reparación (ajustable por dificultad)."""
        return problema.cantidad_pasos * 10
