import json
from pathlib import Path
from infraestructura.recursos.rutas import Rutas


def cargar_datos_json(archivo: str) -> dict | list:
    
    """
    Retorna todos los datos albergados en un archivo json
    ubicado en json/
    """
    
    ruta_archivo: Path = Rutas.json(archivo)
    
    with open(ruta_archivo, "r", encoding="utf-8") as file:
        datos = json.load(file)
    
    return datos


def guardar_datos_json(archivo: str, datos: dict | list) -> None:
    
    """
    Guarda datos manipulados en un archivo json
    ubicado en json/
    """
    
    ruta_archivo: Path = Rutas.json(archivo)
    
    with open(ruta_archivo, "w", encoding="utf-8") as file:
        json.dump(datos, file, indent=4)


def cargar_config_json(dato_deseado: str) -> dict:
    
    """
    Carga los datos que el usuario nesesita del 
    archivo jsons/config.json
    """
    
    datos_config = cargar_datos_json("config.json")
    datos = datos_config[dato_deseado]
    
    return datos