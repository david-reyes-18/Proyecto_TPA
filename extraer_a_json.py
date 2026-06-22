#!/usr/bin/env python3
"""
Script para extraer los componentes de catalogo_componentes.py y guardarlos como JSON individuales.
"""

import json
from dataclasses import is_dataclass, asdict
from enum import Enum
from typing import Any, Dict, List, get_type_hints

# Importar los catálogos desde el módulo existente
from fabricas.dispositivos.catalogo_componentes import CatalogoLaptop, CatalogoPCEscritorio


def convertir_a_dict_compatibles_json(obj: Any) -> Any:
    """
    Convierte una instancia de dataclass (o enum, o lista, etc.) a un formato compatible con JSON.
    - Las dataclasses se convierten a dict, recursivamente.
    - Los Enums se convierten a su nombre (string).
    - Las listas y tuplas se procesan elemento a elemento.
    - Otros tipos se devuelven tal cual.
    """
    if is_dataclass(obj):
        # Procesar cada campo de la dataclass
        resultado = {}
        for campo in obj.__dataclass_fields__.values():
            valor = getattr(obj, campo.name)
            resultado[campo.name] = convertir_a_dict_compatibles_json(valor)
        return resultado
    elif isinstance(obj, Enum):
        return obj.name  # Ej: SocketCPU.BGA -> "BGA"
    elif isinstance(obj, (list, tuple)):
        return [convertir_a_dict_compatibles_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {clave: convertir_a_dict_compatibles_json(valor) for clave, valor in obj.items()}
    else:
        # str, int, float, bool, None
        return obj


def extraer_lista_de_clase(clase_catologo, nombre_atributo):
    """
    Extrae una lista de atributos de una clase de catálogo y la convierte a formato JSON-compatible.
    """
    lista = getattr(clase_catologo, nombre_atributo, [])
    if not isinstance(lista, (list, tuple)):
        return []
    return [convertir_a_dict_compatibles_json(item) for item in lista]


def determinar_tipo_dispositivo_y_categoria(nombre_atributo):
    """
    Determina si el atributo pertenece a laptop o pc_escritorio y su categoría (basica, intermedia, gamer)
    basado en el nombre del atributo.
    Asume que los nombres de atributo siguen el patrón: <COMPONENTE>_<CATEGORIA> o <COMPONENTE>_<CATEGORIA>_<SUB>
    """
    nombre = nombre_atributo.upper()
    # Primero, verificar si es de laptop o pc_escritorio mirando el nombre de la clase? No, lo haremos por separado.
    # En lugar de eso, procesaremos cada clase de catálogo por separado y asignaremos el tipo de dispositivo.
    # Esta función será llamada desde el contexto de conocer si estamos procesando CatalogoLaptop o CatalogoPCEscritorio.
    # Por ahora, devolvemos solo la categoría y asumiremos que el llamador sabe el tipo de dispositivo.
    if 'BASICA' in nombre:
        categoria = 'basica'
    elif 'INTERMEDIA' in nombre:
        categoria = 'intermedia'
    elif 'GAMER' in nombre:
        categoria = 'gamer'
    else:
        # Si no encaja, intentar adivinar por otros patrones o devolver None
        categoria = None
    return categoria


def construir_estructura_json(datos_por_tipo_y_categoria):
    """
    Convierte un diccionario cuya clave es (tipo_dispositivo, categoria) y valor es lista de componentes
    en la estructura JSON deseada: {tipo_dispositivo: {categoria: lista}}
    """
    resultado = {}
    for (tipo_dispositivo, categoria), lista in datos_por_tipo_y_categoria.items():
        if tipo_dispositivo not in resultado:
            resultado[tipo_dispositivo] = {}
        resultado[tipo_dispositivo][categoria] = lista
    return resultado


def main():
    # Mapeo de nombres de atributo a nombre de archivo JSON (sin extension)
    # Agrupamos por tipo de componente
    mapeo_atributo_a_componente = {
        # CPUs
        'CPUS_BASICA': 'cpus',
        'CPUS_INTERMEDIA': 'cpus',
        'CPUS_GAMER': 'cpus',
        # GPUs
        'GPUS_BASICA': 'gpus',
        'GPUS_INTERMEDIA': 'gpus',
        'GPUS_GAMER': 'gpus',
        # RAM módulos
        'MODULOS_RAM_BASICA': 'rams',
        'MODULOS_RAM_INTERMEDIA': 'rams',
        'MODULOS_RAM_GAMER': 'rams',
        # Para PC de escritorio, tenemos divisiones adicionales de RAM
        'MODULOS_RAM_INTERMEDIA_DDR4': 'rams',
        'MODULOS_RAM_INTERMEDIA_DDR5': 'rams',
        # SSDs
        'SSDS_BASICA': 'ssds',
        'SSDS_INTERMEDIA': 'ssds',
        'SSDS_GAMER': 'ssds',
        # Baterías
        'BATERIAS_BASICA': 'baterias',
        'BATERIAS_INTERMEDIA': 'baterias',
        'BATERIAS_GAMER': 'baterias',
        # Pantallas
        'PANTALLAS_BASICA': 'pantallas',
        'PANTALLAS_INTERMEDIA': 'pantallas',
        'PANTALLAS_GAMER': 'pantallas',
        # Placas base
        'PLACAS_BASICA': 'placas',
        'PLACAS_INTERMEDIA': 'placas',
        'PLACAS_GAMER': 'placas',
        # Fuentes de poder (solo PC de escritorio) - son tuplas de enteros
        'FUENTES_BASICA': 'fuentes',
        'FUENTES_INTERMEDIA': 'fuentes',
        'FUENTES_GAMER': 'fuentes',
        # Modelos de equipo - listas de strings
        'MODELOS_BASICA': 'modelos',
        'MODELOS_INTERMEDIA': 'modelos',
        'MODELOS_GAMER': 'modelos',
    }

    # Diccionario para acumular datos por (tipo_dispositivo, componente, categoria)
    # Estructura: {componente: {tipo_dispositivo: {categoria: lista}}}
    acumular = {}

    # Procesar CatalogoLaptop
    laptop = CatalogoLaptop()
    for nombre_atributo in dir(laptop):
        if nombre_atributo.startswith('_'):
            continue
        valor = getattr(laptop, nombre_atributo)
        if isinstance(valor, (list, tuple)) and len(valor) > 0:
            # Verificar si el primer elemento es una dataclass (o al menos tiene __dataclass_fields__)
            # O si es una lista de strings o enteros (como MODELs o FUENTES)
            # Vamos a intentar procesarlo de todos modos; nuestra función de conversion manejará los tipos.
            if nombre_atributo in mapeo_atributo_a_componente:
                componente = mapeo_atributo_a_componente[nombre_atributo]
                categoria = determinar_tipo_dispositivo_y_categoria(nombre_atributo)
                if categoria is None:
                    # Si no podemos determinar la categoría, omitir o usar un default?
                    continue
                lista_json = convertir_a_dict_compatibles_json(valor)
                if componente not in acumular:
                    acumular[componente] = {}
                if 'laptop' not in acumular[componente]:
                    acumular[componente]['laptop'] = {}
                acumular[componente]['laptop'][categoria] = lista_json

    # Procesar CatalogoPCEscritorio
    pc = CatalogoPCEscritorio()
    for nombre_atributo in dir(pc):
        if nombre_atributo.startswith('_'):
            continue
        valor = getattr(pc, nombre_atributo)
        if isinstance(valor, (list, tuple)) and len(valor) > 0:
            if nombre_atributo in mapeo_atributo_a_componente:
                componente = mapeo_atributo_a_componente[nombre_atributo]
                categoria = determinar_tipo_dispositivo_y_categoria(nombre_atributo)
                if categoria is None:
                    continue
                lista_json = convertir_a_dict_compatibles_json(valor)
                if componente not in acumular:
                    acumular[componente] = {}
                if 'pc_escritorio' not in acumular[componente]:
                    acumular[componente]['pc_escritorio'] = {}
                acumular[componente]['pc_escritorio'][categoria] = lista_json

    # Ahora, para cada componente, construir la estructura final y escribir el JSON
    for componente, datos_por_dispositivo in acumular.items():
        # Construir la estructura: {tipo_dispositivo: {categoria: lista}}
        estructura_final = {}
        for tipo_dispositivo, datos_por_categoria in datos_por_dispositivo.items():
            estructura_final[tipo_dispositivo] = {}
            for categoria, lista in datos_por_categoria.items():
                estructura_final[tipo_dispositivo][categoria] = lista

        # Nombre del archivo
        nombre_archivo = f"{componente}.json"
        ruta_archivo = f"/home/david/Proyecto_TPA/fabricas/dispositivos/datos/{nombre_archivo}"

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(estructura_final, f, indent=2, ensure_ascii=False)

        print(f"Generado: {ruta_archivo}")

if __name__ == '__main__':
    main()