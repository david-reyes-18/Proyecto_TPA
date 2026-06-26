from abc import ABC, abstractmethod
from dominio.entidades.componentes.base.componente import Componente
from dominio.entidades.problemas.perfil_dispositivo import TipoDispositivo


class RepositorioComponentes(ABC):
    """
    Puerto (interfaz) para acceder a los componentes disponibles en el catálogo.
    
    Implementado en infraestructura por RepositorioComponentesJson,
    que lee fabricas/dispositivos/datos/*.json.
    
    Separado de RepositorioDispositivos (ISP): las fábricas solo necesitan
    obtener listas de componentes, no modelos completos de dispositivos.
    """
    
    @abstractmethod
    def obtener_cpus(self) -> list[dict]:
        """Devuelve todos los CPUs del catálogo como datos crudos."""
    
    @abstractmethod
    def obtener_rams(self) -> list[dict]:
        """Devuelve todos los módulos RAM del catálogo."""
    
    @abstractmethod
    def obtener_gpus(self) -> list[dict]:
        """Devuelve todas las GPUs del catálogo."""
    
    @abstractmethod
    def obtener_ssds(self) -> list[dict]:
        """Devuelve todos los SSDs del catálogo."""

    @abstractmethod
    def obtener_baterias(self) -> list[dict]:
        """Devuelve todas las baterías del catálogo."""
    
    @abstractmethod
    def obtener_pantallas(self) -> list[dict]:
        """Devuelve todas las pantallas del catálogo."""
    
    @abstractmethod
    def obtener_placas(self) -> list[dict]:
        """Devuelve todas las placas base del catálogo."""
    
    @abstractmethod
    def obtener_fuentes(self) -> list[dict]:
        """Devuelve todas las fuentes de poder del catálogo."""
    
    @abstractmethod
    def obtener_por_tipo(self, tipo: str) -> list[dict]:
        """
        Devuelve componentes por tipo ('CPU', 'RAM', 'SSD', 'GPU',
        'BATERIA', 'PANTALLA', 'PLACA', 'FUENTE').
        """
    
    def obtener_compatibles_con(self, tipo_dispositivo: TipoDispositivo) -> dict[str, list[dict]]:
        """
        Devuelve un mapa tipo_componente → lista de componentes compatibles
        con el tipo de dispositivo indicado (LAPTOP no tiene fuente de poder;
        PC_ESCRITORIO no tiene batería).
        """
        todos = {
            "CPU": self.obtener_cpus(),
            "RAM": self.obtener_rams(),
            "GPU": self.obtener_gpus(),
            "SSD": self.obtener_ssds(),
            "PLACA": self.obtener_placas(),
        }
        if tipo_dispositivo == TipoDispositivo.LAPTOP:
            todos["BATERIA"] = self.obtener_baterias()
            todos["PANTALLA"] = self.obtener_pantallas()
        else:
            todos["FUENTE"] = self.obtener_fuentes()
        
        return {
            tipo: [c for c in componentes if self._compatible(c, tipo_dispositivo)]
            for tipo, componentes in todos.items()
        }
    
    def _compatible(self, componente: dict, tipo: TipoDispositivo) -> bool:
        """
        Verifica compatibilidad básica de un componente con el tipo de dispositivo.
        Las implementaciones concretas pueden sobreescribir esto para lógica más fina.
        """
        dispositivo_campo = componente.get("dispositivo", "ambos").lower()
        if dispositivo_campo == "ambos":
            return True
        if tipo == TipoDispositivo.LAPTOP and dispositivo_campo == "laptop":
            return True
        if tipo == TipoDispositivo.PC_ESCRITORIO and dispositivo_campo in ("pc", "escritorio", "pc_escritorio"):
            return True
        return False