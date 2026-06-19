"""
Capa de servicios del dominio.

Orquesta entidades y reglas de negocio sin depender de pygame, escenas ni JSON.
"""

from dominio.servicios.diagnostico import InformeDiagnostico, ServicioDiagnostico
from dominio.servicios.reparacion import ServicioReparacion
from dominio.servicios.gestor_trabajos import ServicioGestorTrabajos, Trabajo
from dominio.entidades.problemas.perfil_dispositivo import TipoDispositivo, TierDispositivo

__all__ = [
    "InformeDiagnostico",
    "ServicioDiagnostico",
    "ServicioReparacion",
    "ServicioGestorTrabajos",
    "Trabajo",
    "TipoDispositivo",
    "TierDispositivo",
]
