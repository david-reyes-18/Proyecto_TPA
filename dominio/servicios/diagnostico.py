from __future__ import annotations
from dataclasses import dataclass, field
from dominio.entidades.dispositivos.dispositivo import Dispositivo
from dominio.entidades.dispositivos.laptop import Laptop
from dominio.entidades.dispositivos.pc_escritorio import PCEscritorio
from dominio.entidades.problemas.problema import Problema
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


@dataclass
class InformeDiagnostico:
    """
    Resultado agregado de diagnosticar un dispositivo completo.
    """

    dispositivo_modelo: str
    resultados: dict[str, ResultadoOperacion] = field(default_factory=dict)
    componente_afectado: str | None = None
    resultado_afectado: ResultadoOperacion | None = None

    @property
    def tiene_fallas(self) -> bool:
        return any(not r.exito_operacion for r in self.resultados.values())

    @property
    def fallas(self) -> list[tuple[str, ResultadoOperacion]]:
        return [
            (nombre, resultado)
            for nombre, resultado in self.resultados.items()
            if not resultado.exito_operacion
        ]

    @property
    def resumen(self) -> str:
        if not self.tiene_fallas:
            return "Todos los componentes reportan estado funcional."
        nombres = ", ".join(nombre for nombre, _ in self.fallas)
        return f"Fallas detectadas en: {nombres}"


class ServicioDiagnostico:
    """
    Orquesta el diagnóstico de hardware sin acoplarse a la presentación.
    """
    
    def diagnosticar(
        self,
        dispositivo: Dispositivo,
        problema: Problema | None = None,
    ) -> InformeDiagnostico:
        """
        Ejecuta el diagnóstico completo del dispositivo.

        Usa `diagnosticar_todo()` cuando el dispositivo lo implementa
        (Laptop / PCEscritorio); si no, recurre al método base por componente.
        """
        resultados = self._obtener_resultados(dispositivo)
        problema_activo = problema or dispositivo.problema
        nombre_afectado = problema_activo.componente_afectado.nombre

        return InformeDiagnostico(
            dispositivo_modelo=self._obtener_modelo(dispositivo),
            resultados=resultados,
            componente_afectado=nombre_afectado,
            resultado_afectado=resultados.get(nombre_afectado),
        )

    def diagnosticar_componente(
        self,
        dispositivo: Dispositivo,
        nombre_componente: str,
    ) -> ResultadoOperacion:
        """Diagnostica un único componente por nombre."""
        componente = dispositivo.obtener_componente(nombre_componente)
        if componente is None:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema=f"Componente '{nombre_componente}' no encontrado.",
            )
        return componente.diagnosticar()

    def confirmar_falla_reportada(self, informe: InformeDiagnostico) -> ResultadoOperacion:
        """
        Verifica que el componente afectado del problema coincide con una falla real.
        Útil como primer paso del taller antes de iniciar la reparación.
        """
        if informe.resultado_afectado is None:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="No se pudo localizar el componente afectado.",
            )

        if informe.resultado_afectado.exito_operacion:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.COMPONENTE_FUNCIONAL,
                mensaje_sistema=(
                    f"{informe.componente_afectado} reporta estado funcional; "
                    "revisa si el problema es intermitente."
                ),
            )

        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.COMPONENTE_FUNCIONAL,
            mensaje_sistema=(
                f"Falla confirmada en {informe.componente_afectado}: "
                f"{informe.resultado_afectado.mensaje_sistema}"
            ),
        )

    def _obtener_resultados(self, dispositivo: Dispositivo) -> dict[str, ResultadoOperacion]:
        if isinstance(dispositivo, (Laptop, PCEscritorio)):
            return dispositivo.diagnosticar_todo()

        resultados: dict[str, ResultadoOperacion] = {}
        for componente in dispositivo.componentes:
            resultados[componente.nombre] = componente.diagnosticar()
        return resultados

    def _obtener_modelo(self, dispositivo: Dispositivo) -> str:
        if isinstance(dispositivo, (Laptop, PCEscritorio)):
            return dispositivo.modelo
        return dispositivo.problema.nombre
