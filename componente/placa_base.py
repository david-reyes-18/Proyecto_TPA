from componente.componente import Componente

class PlacaBase(Componente):
    def __init__(self, tipo_ram: str, cantidad_slots: int, cantidad_maxima_ram: int):
        super().__init__("Placa Base", es_reemplazable = True, es_reparable = True)
        self._tipo_ram = tipo_ram
        self._cantidad_slots = cantidad_slots
        self._cantidad_maxima_ram = cantidad_maxima_ram
    
    @property
    def tipo_ram(self) -> str:
        return self._tipo_ram
    
    @property
    def cantidad_slots(self) -> int:
        return self._cantidad_slots
    
    @property
    def cantidad_maxima_ram(self) -> int:
        return self._cantidad_maxima_ram
    
    def cantidad_ram_por_slot(self) -> int:
        return self._cantidad_maxima_ram // self._cantidad_slots
    
    def reparar(self):
        return "Funcion no implementada"
    
    def reemplazar(self):
        return "Funcion no implementada"
    
    def diagnosticar(self) -> str:
        return f"""Placa base: {self._cantidad_slots} Slots, 
                {self._cantidad_maxima_ram} GB RAM {self._tipo_ram}"""