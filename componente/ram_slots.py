from componente.ram import RAM

class RAMSlot:
    def __init__(
        self, capacidad_maxima_ram: int, 
        capacidad_maxima_mhz: int,
        tipo_compatible: str, 
        modulo: RAM | None = None
    ):
    
        self._capacidad_maxima_ram = capacidad_maxima_ram
        self._capacidad_maxima_mhz = capacidad_maxima_mhz
        self._tipo_compatible = tipo_compatible
        self._modulo = modulo
    
    @property
    def capacidad_maxima_ram(self) -> int:
        return self._capacidad_maxima_ram
    
    @property
    def capacidad_maxima_mhz(self) -> int:
        return self._capacidad_maxima_mhz
    
    @property
    def tipo_compatible(self) -> str:
        return self._tipo_compatible
    
    @property
    def modulo(self) -> RAM | None:
        return self._modulo
    
    def instalar_ram(self, nueva_ram: RAM) -> bool:
        if self._modulo is not None:
            return False
        
        if nueva_ram.capacidad_gb > self._capacidad_maxima_ram:
            return False
        
        if nueva_ram.velocidad_mhz > self._capacidad_maxima_mhz:
            return False
        
        if nueva_ram.tipo.lower() != self._tipo_compatible.lower():
            return False
        
        self._modulo = nueva_ram
        return True
    
    def remover_ram(self) -> RAM | None:
        ram_removida = self._modulo
        self._modulo = None
        return ram_removida