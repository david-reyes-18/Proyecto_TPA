"""
Catálogo de componentes accesible mediante variables pre-cargadas.
Carga todos los JSONs desde fabricas/dispositivos/datos/ y los expone
como variables de fácil acceso (CPUS, GPUS, etc.).
"""

import json
from pathlib import Path

# Importar la función cargar_json del módulo existente para reutilizarla
from .cargar_catalogo import cargar_json

_DIR_DATOS = Path(__file__).parent / "datos"

# Mapeo de nombre de archivo JSON (sin extension) a nombre de variable
# Nota: algunos archivos pueden contener solo datos de pc_escritorio (como fuentes)
# pero aún así los cargamos.
_ARCHIVOS_JSON = [
    "cpus",
    "gpus",
    "rams",
    "ssds",
    "baterias",
    "pantallas",
    "placas",
    "fuentes",
    "modelos",
]

# Cargar cada JSON y asignarlo a una variable global con nombre en mayúsculas
globals().update({
    nombre.upper(): cargar_json(f"{nombre}.json")
    for nombre in _ARCHIVOS_JSON
    if (_DIR_DATOS / f"{nombre}.json").exists()
})

# También ofrecer un diccionario que contenga todos ellos para acceso por nombre
CATALOGO = {
    nombre.upper(): cargar_json(f"{nombre}.json")
    for nombre in _ARCHIVOS_JSON
    if (_DIR_DATOS / f"{nombre}.json").exists()
}

# Función de conveniencia para recargar todos los JSONs (útil si se modifican durante ejecución)
def recargar():
    """Recarga todos los JSONs y actualiza las variables globales y CATALOGO."""
    globals().update({
        nombre.upper(): cargar_json(f"{nombre}.json")
        for nombre in _ARCHIVOS_JSON
        if (_DIR_DATOS / f"{nombre}.json").exists()
    })
    global CATALOGO
    CATALOGO = {
        nombre.upper(): cargar_json(f"{nombre}.json")
        for nombre in _ARCHIVOS_JSON
        if (_DIR_DATOS / f"{nombre}.json").exists()
    }