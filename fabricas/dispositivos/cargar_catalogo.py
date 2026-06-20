"""
Cargador de catálogo de componentes desde JSON.

Reconstruye las dataclasses Datos* (DatosCPU, DatosGPU, DatosPlacaBase, ...)
a partir de los archivos JSON en fabricas/dispositivos/datos/, sin tener que
escribir un loader a mano por cada tipo de componente.

Cómo funciona
-------------
Cada dataclass Datos* declara sus campos con tipos (ej: socket: SocketCPU).
construir() lee esos tipos con dataclasses.fields() y, para cada campo:
- si el tipo es un Enum  -> busca el valor por nombre (ej: "BGA" -> SocketCPU.BGA)
- si el tipo es otra dataclass -> se construye recursivamente (anidado)
- si no -> se usa el valor tal cual viene del JSON (str, int, float, bool)

Así, agregar un componente nuevo al catálogo NUNCA requiere tocar este
archivo: solo el JSON y, si hace falta, la propia dataclass en
catalogo_componentes.py.
"""

import json
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Type, TypeVar

T = TypeVar("T")

_DIR_DATOS = Path(__file__).parent / "datos"


def _convertir_campo(tipo, valor):
    """Convierte un valor crudo de JSON al tipo declarado en la dataclass."""

    # Campo que es otra dataclass anidada (ej: DatosSSDSlot dentro de DatosPlacaBase)
    if is_dataclass(tipo):
        return construir(tipo, valor)

    # Campo que es un Enum (ej: SocketCPU, FormaBateria, TipoPanel...)
    if isinstance(tipo, type) and issubclass(tipo, __import__("enum").Enum):
        return tipo[valor]  # "BGA" -> SocketCPU.BGA (por nombre, no por .value)

    # Tipo simple: str, int, float, bool -> tal cual
    return valor


def construir(cls: Type[T], datos: dict) -> T:
    """Construye una instancia de una dataclass Datos* a partir de un dict del JSON."""
    kwargs = {
        campo.name: _convertir_campo(campo.type, datos[campo.name])
        for campo in fields(cls)
    }
    return cls(**kwargs)


def construir_lista(cls: Type[T], lista_datos: list[dict]) -> list[T]:
    """Construye una lista de instancias de una dataclass Datos* a partir del JSON."""
    return [construir(cls, d) for d in lista_datos]


def cargar_json(nombre_archivo: str) -> dict:
    """Carga un archivo JSON desde fabricas/dispositivos/datos/."""
    ruta = _DIR_DATOS / nombre_archivo
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)
