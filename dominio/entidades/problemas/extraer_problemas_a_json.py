#!/usr/bin/env python3
"""
Script para extraer los problemas de catalogo_problemas_aleatorios.py y catalogo_problemas_historia.py
y convertirlos a archivos JSON por tipo de componente en dominio/entidades/problemas/datos/
"""

import json
import sys
from pathlib import Path
from enum import Enum

# Añadir el directorio raíz del proyecto al path para poder importar dominio
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Importar catálogos de problemas
from dominio.entidades.problemas.catalogo_problemas_aleatorios import CatalogoProblemasAleatorios
from dominio.entidades.problemas.catalogo_problemas_historia import CatalogoProblemasHistoria

# Importar componentes y sus enums
from dominio.entidades.componentes.ram.ram import RAM
from dominio.entidades.componentes.ram.generacion_ram import GeneracionRAM
from dominio.entidades.componentes.ram.formato_ram import FormatoRAM

from dominio.entidades.componentes.ssd.ssd import SSD
from dominio.entidades.componentes.ssd.interfaz_ssd import InterfazSSD

from dominio.entidades.componentes.bateria.bateria import Bateria
from dominio.entidades.componentes.bateria.forma_bateria import FormaBateria

from dominio.entidades.componentes.gpu.gpu import GPU
from dominio.entidades.componentes.gpu.tipo_gpu import TipoGPU
from dominio.entidades.componentes.gpu.tipo_memoria_gpu import TipoMemoriaGPU
from dominio.entidades.componentes.gpu.tipo_interfaz import InterfazGPU

from dominio.entidades.componentes.cpu.cpu import CPU
from dominio.entidades.componentes.cpu.socket import SocketCPU

from dominio.entidades.componentes.pantalla.pantalla import Pantalla
from dominio.entidades.componentes.pantalla.tipo_panel import TipoPanel

# Importar desafíos para serializar los desafíos dentro de los pasos
from dominio.entidades.desafios.desafio import Desafio
from dominio.entidades.desafios.desafio_logico.desafio_logico_booleano import DesafioLogicoBooleano
from dominio.entidades.desafios.desafio_logico.desafio_logico_multiple import DesafioLogicoMultiple
from dominio.entidades.desafios.desafio_logico.desafio_logico_escritura import DesafioLogicoEscritura
from dominio.entidades.desafios.desafio_matematico.desafio_matematico_booleano import DesafioMatematicoBooleano
from dominio.entidades.desafios.desafio_matematico.desafio_matematico_multiple import DesafioMatematicoMultiple
from dominio.entidades.desafios.desafio_matematico.desafio_matematico_escritura import DesafioMatematicoEscritura
from dominio.entidades.desafios.desafio_tecnologico.desafio_tecnologico_booleano import DesafioTecnologicoBooleano
from dominio.entidades.desafios.desafio_tecnologico.desafio_tecnologico_multiple import DesafioTecnologicoMultiple
from dominio.entidades.desafios.desafio_tecnologico.desafio_tecnologico_escritura import DesafioTecnologicoEscritura

from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.componente_tematico import ComponenteTematico


def enum_to_str(e):
    """Convierte un Enum a su nombre (string) para JSON."""
    if isinstance(e, Enum):
        return e.name
    return e


def convertir_componente_a_dict(componente):
    """Convierte una instancia de Componente (o subclase) a dict serializable."""
    # Campos comunes de Componente
    resultado = {
        "nombre": componente.nombre,
        "es_reemplazable": componente.es_reemplazable,
        "es_reparable": componente.es_reparable,
        "esta_funcionando": componente.esta_funcionando,
    }
    # Ahora agregamos campos específicos según el tipo
    if isinstance(componente, RAM):
        resultado.update({
            "tipo": "RAM",
            "capacidad_gb": componente.capacidad_gb,
            "velocidad_mhz": componente.velocidad_mhz,
            "generacion": enum_to_str(componente.generacion),
            "formato": enum_to_str(componente.formato),
        })
    elif isinstance(componente, SSD):
        resultado.update({
            "tipo": "SSD",
            "capacidad_gb": componente.capacidad_gb,
            "velocidad_lectura_mbps": componente.velocidad_lectura_mbps,
            "velocidad_escritura_mbps": componente.velocidad_escritura_mbps,
            "interfaz": enum_to_str(componente.interfaz),
        })
    elif isinstance(componente, Bateria):
        resultado.update({
            "tipo": "Bateria",
            "voltaje_v": componente.voltaje_v,
            "forma_bateria": enum_to_str(componente.forma_bateria),
            "capacidad_wh": componente.capacidad_wh,
            "salud": componente.salud,
        })
    elif isinstance(componente, GPU):
        resultado.update({
            "tipo": "GPU",
            "modelo": componente.modelo,
            "memoria_gb": componente.memoria_gb,
            "tipo_memoria": enum_to_str(componente.tipo_memoria),
            "tipo_gpu": enum_to_str(componente.tipo_gpu),
            "interfaz": enum_to_str(componente.interfaz),
            "tdp_watts": componente.tdp_watts,
        })
    elif isinstance(componente, CPU):
        resultado.update({
            "tipo": "CPU",
            "modelo": componente.modelo,
            "nucleos": componente.nucleos,
            "frecuencia_ghz": componente.frecuencia_ghz,
            "socket": enum_to_str(componente.socket),
            "tdp_watts": componente.tdp_watts,
        })
    elif isinstance(componente, Pantalla):
        resultado.update({
            "tipo": "Pantalla",
            "pulgadas": componente.pulgadas,
            "resolucion": componente.resolucion,
            "tipo_panel": enum_to_str(componente.tipo_panel),
            "tasa_refresco_hz": componente.tasa_refresco_hz,
        })
    else:
        # Si no reconocemos, al menos incluimos el tipo de clase
        resultado["tipo"] = componente.__class__.__name__
    return resultado


def convertir_desafio_a_dict(desafio: Desafio):
    """Convierte una instancia de Desafio a dict serializable."""
    resultado = {
        "enunciado": desafio.enunciado,
        "tipo": enum_to_str(desafio.tipo),  # NombreTipoDesafio
        "dificultad": enum_to_str(desafio.dificultad),  # NivelDificultad
    }
    # Agregar campos específicos según subclase
    if isinstance(desafio, (DesafioLogicoBooleano, DesafioMatematicoBooleano,
                            DesafioTecnologicoBooleano)):
        resultado["respuesta"] = desafio.respuesta
    elif isinstance(desafio, DesafioLogicoEscritura):
        resultado["respuesta"] = desafio.respuesta
        if hasattr(desafio, 'tolerancia'):
            resultado["tolerancia"] = desafio.tolerancia
    elif isinstance(desafio, DesafioMatematicoEscritura):
        resultado["respuesta"] = desafio.respuesta
        if hasattr(desafio, 'tolerancia'):
            resultado["tolerancia"] = desafio.tolerancia
    elif isinstance(desafio, DesafioTecnologicoEscritura):
        resultado["respuesta"] = desafio.respuesta
        if hasattr(desafio, 'tolerancia'):
            resultado["tolerancia"] = desafio.tolerancia
    elif isinstance(desafio, (DesafioLogicoMultiple, DesafioMatematicoMultiple,
                            DesafioTecnologicoMultiple)):
        # Use atributos alternativas and indice_correcto
        resultado["alternativas"] = desafio.alternativas
        resultado["indice_correcto"] = desafio.indice_correcto
    # Los desafíos también tienen componente y categoria, pero podemos incluirlos si se desea
    # Para mantenerlo simple, los omitimos aquí (pero podrían añadirse)
    return resultado


def convertir_problema_a_dict(problema):
    """Convierte una instancia de Problema a dict serializable."""
    resultado = {
        "nombre": problema.nombre,
        "descripcion_email": problema.descripcion_email,
        "componente_afectado": convertir_componente_a_dict(problema.componente_afectado),
        "pasos_reparacion": []
    }
    for paso in problema.pasos_de_reparacion:
        paso_dict = {
            "descripcion_accion": paso.descripcion_accion,
            "explicacion": paso.explicacion,
            "desafio": convertir_desafio_a_dict(paso.desafio)
        }
        resultado["pasos_reparacion"].append(paso_dict)
    return resultado


def extraer_problemas_desde_catalogo(catalogo_clase, es_aleatorio=True):
    """
    Extrae todas las instancias de problema del catalogo dado.
    Devuelve una dict agrupada por tipo de componente.
    """
    # Instanciamos el catalogo para acceder a sus atributos
    catalogo = catalogo_clase()
    problema_instances = []
    if es_aleatorio:
        # CatalogoProblemasAleatorios tiene _REGISTRO: dict[ComponenteTematico, list[type]]
        for componente, lista_clases in catalogo._REGISTRO.items():
            for cls in lista_clases:
                instancia = cls()  # crear instancia sin argumentos
                problema_instances.append(instancia)
    else:
        # CatalogoProblemasHistoria tiene _NIVELES: dict[int, type]
        for nivel, cls in catalogo._NIVELES.items():
            instancia = cls()
            problema_instances.append(instancia)
    # Ahora agrupar por tipo de componente (según el componente_afectado)
    grouped = {}
    for inst in problema_instances:
        comp = inst.componente_afectado
        comp_type = type(comp).__name__  # e.g., RAM, SSD, etc.
        # Normalizar a nombre usado en archivos JSON (minusculas)
        key = comp_type.lower()
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(convertir_problema_a_dict(inst))
    return grouped


def main():
    output_dir = Path(__file__).parent / "datos"
    output_dir.mkdir(exist_ok=True)

    # Extraer problemas aleatorios
    aleatorios = extraer_problemas_desde_catalogo(CatalogoProblemasAleatorios, es_aleatorio=True)
    # Extraer problemas de historia
    historias = extraer_problemas_desde_catalogo(CatalogoProblemasHistoria, es_aleatorio=False)

    # Para cada tipo de componente, crear un JSON que contenga tanto aleatorios como historias
    # Podemos mezclar o mantener separados; aquí vamos a crear un archivo por componente con dos claves: aleatorios e historias
    all_component_types = set(aleatorios.keys()) | set(historias.keys())
    for comp_type in all_component_types:
        data = {
            "aleatorios": aleatorios.get(comp_type, []),
            "historias": historias.get(comp_type, [])
        }
        # Nombre de archivo: e.g., ram.json
        nombre_archivo = f"{comp_type}.json"
        ruta_archivo = output_dir / nombre_archivo
        # Convertir cualquier resto de enums a strings (pero ya lo hicimos en las funciones)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Generado: {ruta_archivo}")

if __name__ == "__main__":
    main()