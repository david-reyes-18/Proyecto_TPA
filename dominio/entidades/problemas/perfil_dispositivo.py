"""
Perfil de dispositivo asociado a un Problema.

Declara explícitamente qué tipo de equipo y tier de complejidad debe
generar la fábrica al aceptar un trabajo, sin depender de parsing por strings.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TipoDispositivo(Enum):
    LAPTOP = "laptop"
    PC_ESCRITORIO = "pc_escritorio"


class TierDispositivo(Enum):
    BASICO = "basico"
    INTERMEDIO = "intermedio"
    GAMER = "gamer"


@dataclass(frozen=True)
class PerfilDispositivo:
    tipo: TipoDispositivo
    tier: TierDispositivo


def inferir_perfil_desde_nombre(nombre: str) -> PerfilDispositivo:
    """
    Inferencia de respaldo para problemas que aún no declaran perfil explícito.
    Usado por catálogos aleatorios y código legado.
    """
    nombre_lower = nombre.lower()

    if "laptop" in nombre_lower:
        tipo = TipoDispositivo.LAPTOP
    elif "pc" in nombre_lower or "escritorio" in nombre_lower:
        tipo = TipoDispositivo.PC_ESCRITORIO
    else:
        tipo = TipoDispositivo.LAPTOP

    if any(palabra in nombre_lower for palabra in ("avanzado", "socket", "gamer")):
        tier = TierDispositivo.GAMER
    elif any(palabra in nombre_lower for palabra in ("upgrade", "migracion", "migración")):
        tier = TierDispositivo.INTERMEDIO
    else:
        tier = TierDispositivo.BASICO

    return PerfilDispositivo(tipo=tipo, tier=tier)
