from __future__ import annotations
import json
from pathlib import Path
from dominio.repositorios.repositorio_desafios import RepositorioDesafios
from dominio.entidades.desafios.desafio import Desafio
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.componente_tematico import ComponenteTematico
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad
from dominio.entidades.desafios.desafio_logico.desafio_logico_booleano import DesafioLogicoBooleano
from dominio.entidades.desafios.desafio_logico.desafio_logico_multiple import DesafioLogicoMultiple
from dominio.entidades.desafios.desafio_logico.desafio_logico_escritura import DesafioLogicoEscritura
from dominio.entidades.desafios.desafio_matematico.desafio_matematico_booleano import DesafioMatematicoBooleano
from dominio.entidades.desafios.desafio_matematico.desafio_matematico_multiple import DesafioMatematicoMultiple
from dominio.entidades.desafios.desafio_matematico.desafio_matematico_escritura import DesafioMatematicoEscritura
from dominio.entidades.desafios.desafio_tecnologico.desafio_tecnologico_booleano import DesafioTecnologicoBooleano
from dominio.entidades.desafios.desafio_tecnologico.desafio_tecnologico_multiple import DesafioTecnologicoMultiple
from dominio.entidades.desafios.desafio_tecnologico.desafio_tecnologico_escritura import DesafioTecnologicoEscritura


class RepositorioDesafiosJson(RepositorioDesafios):
    """
    Lee los desafíos desde fabricas/desafios/datos/*_desafios.json
    y los expone como objetos de dominio.
    
    Uso:
        repo = RepositorioDesafiosJson()
        desafio = repo.obtener_aleatorio(
            ComponenteTematico.CPU,
            CategoriaDesafio.MATEMATICO,
            NombreTipoDesafio.ESCRITURA,
            NivelDificultad.MEDIA,
        )
    """
    
    _DIR_DATOS = Path(__file__).resolve().parent.parent.parent / "infraestructura" / "datos" / "desafios"
    
    _ARCHIVOS: dict[ComponenteTematico, str] = {
        ComponenteTematico.CPU:      "cpu_desafios.json",
        ComponenteTematico.RAM:      "ram_desafios.json",
        ComponenteTematico.SSD:      "ssd_desafios.json",
        ComponenteTematico.GPU:      "gpu_desafios.json",
        ComponenteTematico.BATERIA:  "baterias_desafios.json",
        ComponenteTematico.PANTALLA: "pantallas_desafios.json",
        ComponenteTematico.GENERAL:  "general_desafios.json",
    }
    
    _MAPA_CATEGORIA: dict[str, CategoriaDesafio] = {
        "MATEMATICO":  CategoriaDesafio.MATEMATICO,
        "LOGICO":      CategoriaDesafio.LOGICO,
        "TECNOLOGICO": CategoriaDesafio.TECNOLOGICO,
    }
    
    _MAPA_TIPO: dict[str, NombreTipoDesafio] = {
        "BOOLEANO":  NombreTipoDesafio.BOOLEANO,
        "MULTIPLE":  NombreTipoDesafio.MULTIPLE,
        "ESCRITURA": NombreTipoDesafio.ESCRITURA,
    }
    
    def __init__(self) -> None:
        self._cache: dict[ComponenteTematico, list[Desafio]] = {}
    
    def obtener_todos(self) -> list[Desafio]:
        todos: list[Desafio] = []
        for componente in self._ARCHIVOS:
            todos.extend(self._cargar_componente(componente))
        return todos
    
    def obtener_por_componente(self, componente: ComponenteTematico) -> list[Desafio]:
        return self._cargar_componente(componente)
    
    def obtener_por_categoria(self, categoria: CategoriaDesafio) -> list[Desafio]:
        return [d for d in self.obtener_todos() if d.categoria == categoria]
    
    def obtener_por_tipo(self, tipo: NombreTipoDesafio) -> list[Desafio]:
        return [d for d in self.obtener_todos() if d.tipo == tipo]
    
    def obtener_filtrado(
        self,
        componente: ComponenteTematico,
        categoria: CategoriaDesafio,
        tipo: NombreTipoDesafio,
        dificultad: NivelDificultad,
    ) -> list[Desafio]:
        return [
            d for d in self._cargar_componente(componente)
            if d.categoria == categoria
            and d.tipo == tipo
            and d.dificultad == dificultad
        ]
    
    def _cargar_componente(self, componente: ComponenteTematico) -> list[Desafio]:
        if componente not in self._cache:
            self._cache[componente] = self._cargar_desde_json(componente)
        return self._cache[componente]
    
    def _cargar_desde_json(self, componente: ComponenteTematico) -> list[Desafio]:
        archivo = self._ARCHIVOS.get(componente)
        if not archivo:
            return []
        ruta = self._DIR_DATOS / archivo
        if not ruta.exists():
            return []
        
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        resultado: list[Desafio] = []
        for cat_str, tipos in datos.items():
            categoria = self._MAPA_CATEGORIA.get(cat_str.upper())
            if categoria is None:
                continue
            for tipo_str, items in tipos.items():
                tipo = self._MAPA_TIPO.get(tipo_str.upper())
                if tipo is None:
                    continue
                for raw in items:
                    try:
                        desafio = self._construir(raw, componente, categoria, tipo)
                        resultado.append(desafio)
                    except Exception as e:
                        print(f"[RepositorioDesafiosJson] Error: {e}")
        return resultado
    
    @staticmethod
    def _construir(
        raw: dict,
        componente: ComponenteTematico,
        categoria: CategoriaDesafio,
        tipo: NombreTipoDesafio,
    ) -> Desafio:
        texto = raw["texto"]
        dificultad = NivelDificultad[raw["dificultad"].upper()]
        
        if tipo == NombreTipoDesafio.BOOLEANO:
            respuesta = bool(raw["respuesta"])
            if categoria == CategoriaDesafio.MATEMATICO:
                return DesafioMatematicoBooleano(texto, respuesta, componente, dificultad)
            if categoria == CategoriaDesafio.TECNOLOGICO:
                return DesafioTecnologicoBooleano(texto, respuesta, componente, dificultad)
            return DesafioLogicoBooleano(texto, respuesta, componente, dificultad)
        
        if tipo == NombreTipoDesafio.MULTIPLE:
            alternativas = raw.get("alternativas", [])
            indice = int(raw.get("indice_correcto", 0))
            if categoria == CategoriaDesafio.MATEMATICO:
                return DesafioMatematicoMultiple(texto, alternativas, indice, componente, dificultad)
            if categoria == CategoriaDesafio.TECNOLOGICO:
                return DesafioTecnologicoMultiple(texto, alternativas, indice, componente, dificultad)
            return DesafioLogicoMultiple(texto, alternativas, indice, componente, dificultad)
        
        if tipo == NombreTipoDesafio.ESCRITURA:
            respuesta = raw["respuesta"]
            tolerancia = float(raw.get("tolerancia", 0.0))
            if categoria == CategoriaDesafio.MATEMATICO:
                return DesafioMatematicoEscritura(texto, respuesta, componente, dificultad, tolerancia=tolerancia)
            if categoria == CategoriaDesafio.TECNOLOGICO:
                return DesafioTecnologicoEscritura(texto, respuesta, componente, dificultad, tolerancia=tolerancia)
            return DesafioLogicoEscritura(texto, respuesta, componente, dificultad, tolerancia=tolerancia)
        
        raise ValueError(f"Tipo no reconocido: {tipo}")