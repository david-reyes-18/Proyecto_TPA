from componente.componente import Componente

class PlacaBase(Componente):
    def __init__(self, tipo_ram: str, cantidad_slots: int, cantidad_maxima_ram: int):
        super().__init__("Placa Base")
        self._tipo_ram = tipo_ram
        self._cantidad_slots = cantidad_slots
        self._cantidad_maxima_ram = cantidad_maxima_ram
    
    