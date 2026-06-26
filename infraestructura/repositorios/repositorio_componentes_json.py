from __future__ import annotations
from pathlib import Path
from dominio.repositorios.repositorio_dispositivos import RepositorioDispositivos
from dominio.repositorios.repositorio_componentes import RepositorioComponentes
from dominio.entidades.problemas.perfil_dispositivo import TipoDispositivo, TierDispositivo
from infraestructura.recursos.manejador_jsons import cargar_datos_json

_DIR_DATOS = Path(__file__).resolve().parent.parent.parent / "infraestructura" / "datos" /  "componentes"


class RepositorioComponentesJson(RepositorioComponentes):
    
    _MAPA_ARCHIVOS: dict[str, str] = {
        "CPU":      "cpus.json",
        "RAM":      "rams.json",
        "GPU":      "gpus.json",
        "SSD":      "ssds.json",
        "BATERIA":  "baterias.json",
        "PANTALLA": "pantallas.json",
        "PLACA":    "placas.json",
        "FUENTE":   "fuentes.json",
    }

    def __init__(self) -> None:
        self._cache: dict[str, list[dict]] = {}

    # ── Puerto ────────────────────────────────────────────────────────────────

    def obtener_cpus(self)      -> list[dict]: return self.obtener_por_tipo("CPU")
    def obtener_rams(self)      -> list[dict]: return self.obtener_por_tipo("RAM")
    def obtener_gpus(self)      -> list[dict]: return self.obtener_por_tipo("GPU")
    def obtener_ssds(self)      -> list[dict]: return self.obtener_por_tipo("SSD")
    def obtener_baterias(self)  -> list[dict]: return self.obtener_por_tipo("BATERIA")
    def obtener_pantallas(self) -> list[dict]: return self.obtener_por_tipo("PANTALLA")
    def obtener_placas(self)    -> list[dict]: return self.obtener_por_tipo("PLACA")
    def obtener_fuentes(self)   -> list[dict]: return self.obtener_por_tipo("FUENTE")

    def obtener_por_tipo(self, tipo: str) -> list[dict]:
        tipo_upper = tipo.upper()
        if tipo_upper not in self._cache:
            archivo = self._MAPA_ARCHIVOS.get(tipo_upper)
            if archivo is None:
                return []
            datos = cargar_datos_json(archivo)
            self._cache[tipo_upper] = datos if isinstance(datos, list) else []
        return self._cache[tipo_upper]

    def recargar(self) -> None:
        """Invalida el caché para que los JSONs se relean en la siguiente consulta."""
        self._cache.clear()