from __future__ import annotations
from dataclasses import dataclass, field
from dominio.entidades.dispositivos.dispositivo import Dispositivo
from dominio.entidades.jugador.inventario import Inventario
from dominio.entidades.jugador.stats_jugador import StatsJugador
from dominio.entidades.problemas.problema import Problema
from dominio.entidades.problemas.perfil_dispositivo import (
    PerfilDispositivo,
    TipoDispositivo,
    TierDispositivo,
)
from fabricas.dispositivos.fabrica_dispositivo import FabricaDispositivo
from fabricas.dispositivos.fabrica_laptop import FabricaLaptop
from fabricas.dispositivos.fabrica_pc_escritorio import FabricaEscritorio
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion


@dataclass
class Trabajo:
    """Solicitud de reparación recibida por correo."""

    problema: Problema
    recompensa_dinero: int = 100
    recompensa_experiencia: int = 50
    aceptado: bool = False
    completado: bool = False
    dispositivo: Dispositivo | None = field(default=None, repr=False)

    @property
    def asunto_email(self) -> str:
        return f"Trabajo de reparación: {self.problema.nombre}"

    @property
    def descripcion_email(self) -> str:
        return self.problema.descripcion_email


class ServicioGestorTrabajos:
    """Caso de uso: correo → taller → recompensa."""

    def __init__(
        self,
        fabricas: dict[TipoDispositivo, FabricaDispositivo] | None = None,
    ) -> None:
        self._fabricas = fabricas or {
            TipoDispositivo.LAPTOP: FabricaLaptop(),
            TipoDispositivo.PC_ESCRITORIO: FabricaEscritorio(),
        }

    def aceptar(self, trabajo: Trabajo, inventario: Inventario) -> Dispositivo | None:
        if trabajo.aceptado:
            return trabajo.dispositivo

        perfil = trabajo.problema.perfil_dispositivo
        fabrica = self._fabricas.get(perfil.tipo)
        if fabrica is None:
            return None

        dispositivo = self._crear_dispositivo(fabrica, trabajo.problema, perfil.tier)
        if dispositivo is None:
            return None

        trabajo.aceptado = True
        trabajo.dispositivo = dispositivo
        inventario.agregar_dispositivo(dispositivo)

        return dispositivo

    def completar(
        self,
        trabajo: Trabajo,
        stats: StatsJugador,
    ) -> ResultadoOperacion:
        if not trabajo.aceptado:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="Este trabajo aún no ha sido aceptado.",
            )

        if trabajo.completado:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="Este trabajo ya fue completado.",
            )

        if trabajo.dispositivo is None or not trabajo.dispositivo.esta_reparado:
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="El dispositivo aún no está reparado.",
            )

        trabajo.completado = True
        stats.agregar_dinero(trabajo.recompensa_dinero)
        stats.agregar_experiencia(trabajo.recompensa_experiencia)

        return ResultadoOperacion(
            exito_operacion=True,
            codigo_operacion=CodigoOperacion.EXITO_REPARACION,
            mensaje_sistema=(
                f"Trabajo completado. +${trabajo.recompensa_dinero} "
                f"+{trabajo.recompensa_experiencia} XP"
            ),
            costo=trabajo.recompensa_dinero,
            experiencia=trabajo.recompensa_experiencia,
        )

    def crear_trabajo_desde_problema(
        self,
        problema: Problema,
        recompensa_dinero: int = 100,
        recompensa_experiencia: int = 50,
    ) -> Trabajo:
        return Trabajo(
            problema=problema,
            recompensa_dinero=recompensa_dinero,
            recompensa_experiencia=recompensa_experiencia,
        )

    def _crear_dispositivo(
        self,
        fabrica: FabricaDispositivo,
        problema: Problema,
        tier: TierDispositivo,
    ) -> Dispositivo | None:
        creadores = {
            TierDispositivo.BASICO: fabrica.crear_dispositivo_basico,
            TierDispositivo.INTERMEDIO: fabrica.crear_dispositivo_intermedio,
            TierDispositivo.GAMER: fabrica.crear_dispositivo_gamer,
        }
        creador = creadores.get(tier)
        if creador is None:
            return None
        return creador(problema)
