
#!/usr/bin/env python3
"""
Script para extraer los desafíos de catalogo_desafios.py y convertirlos a archivos JSON.
Estructura de salida: un JSON por componente (cpu, gpu, ram, etc.) en fabricas/desafios/datos/
"""

import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar dominio
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fabricas.desafios.catalogo_desafios import CATALOGO
from dominio.entidades.desafios.componente_tematico import ComponenteTematico
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad

# Mapeo de componentes a nombres de archivo
COMPONENTE_A_ARCHIVO = {
    ComponenteTematico.CPU: "cpu_desafios",
    ComponenteTematico.RAM: "ram_desafios",
    ComponenteTematico.SSD: "ssd_desafios",
    ComponenteTematico.GPU: "gpu_desafios",
    ComponenteTematico.BATERIA: "baterias_desafios",
    ComponenteTematico.PANTALLA: "pantallas_desafios",
    ComponenteTematico.GENERAL: "general_desafios",
}

def extraer_valor_enum(enum_val):
    """Extrae el valor string de un enum para JSON."""
    if hasattr(enum_val, 'value'):
        return enum_val.value
    return str(enum_val).split('.')[-1]  # Obtener solo el nombre del enum

def convertir_desafio_a_dict(desafio):
    """Convierte una instancia de desafío a diccionario para JSON."""
    # Todos los desafíos tienen estos atributos básicos
    resultado = {
        "texto": desafio.enunciado,
        "dificultad": extraer_valor_enum(desafio.dificultad),
    }

    # Según el tipo de desafío, agregamos los atributos específicos
    if hasattr(desafio, 'respuesta'):  # Para Booleanos y Escritura
        resultado["respuesta"] = desafio.respuesta

        # Los desafíos de escritura pueden tener tolerancia
        if hasattr(desafio, 'tolerancia'):
            resultado["tolerancia"] = desafio.tolerancia

    elif hasattr(desafio, 'opciones'):  # Para Múltiple choice
        resultado["opciones"] = desafio.opciones
        resultado["respuesta_indice"] = desafio.respuesta_indice

    return resultado

def extraer_desafios_a_json():
    """Extrae todos los desafíos del CATALOGO y los guarda como archivos JSON."""
    # Directorio de salida
    output_dir = Path(__file__).parent / "datos"
    output_dir.mkdir(exist_ok=True)

    # Inicializar estructuras para cada componente
    datos_por_componente = {}
    for componente in ComponenteTematico:
        datos_por_componente[componente] = {
            CategoriaDesafio.MATEMATICO: {
                NombreTipoDesafio.BOOLEANO: [],
                NombreTipoDesafio.MULTIPLE: [],
                NombreTipoDesafio.ESCRITURA: []
            },
            CategoriaDesafio.LOGICO: {
                NombreTipoDesafio.BOOLEANO: [],
                NombreTipoDesafio.MULTIPLE: [],
                NombreTipoDesafio.ESCRITURA: []
            },
            CategoriaDesafio.TECNOLOGICO: {
                NombreTipoDesafio.BOOLEANO: [],
                NombreTipoDesafio.MULTIPLE: [],
                NombreTipoDesafio.ESCRITURA: []
            }
        }

    # Procesar cada entrada del CATALOGO
    for componente, categorias in CATALOGO.items():
        for categoria, tipos in categorias.items():
            for tipo, desafios in tipos.items():
                for desafio in desafios:
                    desafio_dict = convertir_desafio_a_dict(desafio)
                    datos_por_componente[componente][categoria][tipo].append(desafio_dict)

    # Guardar cada componente en su archivo JSON
    for componente, datos in datos_por_componente.items():
        nombre_archivo = COMPONENTE_A_ARCHIVO[componente] + ".json"
        ruta_archivo = output_dir / nombre_archivo

        # Convertir enums a strings para JSON
        datos_serializables = {}
        for categoria_str, tipos_dict in datos.items():
            datos_serializables[categoria_str.value] = {}
            for tipo_str, lista_desafios in tipos_dict.items():
                datos_serializables[categoria_str.value][tipo_str.value] = lista_desafios

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_serializables, f, indent=2, ensure_ascii=False)

        print(f"Generado: {ruta_archivo}")

if __name__ == "__main__":
    extraer_desafios_a_json()