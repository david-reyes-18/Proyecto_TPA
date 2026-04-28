from componente.componente import Componente

class RAM(Componente):
    def __init__(self, nombre: str, capacidad_gb: int, velocidad_mhz: int, tipo: str):
        super().__init__(nombre)
        self._capacidad_gb = capacidad_gb
        self._velocidad_mhz = velocidad_mhz
        self._tipo = tipo
        
    @property
    def capacidad_gb(self) -> int:
        return self._capacidad_gb
    
    @property
    def velocidad_mhz(self) -> int:
        return self._velocidad_mhz
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    def diagnosticar(self) -> str:
        return f"{self.nombre} posee {self.capacidad_gb}GB de {self.velocidad_mhz} MHZ."