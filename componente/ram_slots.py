from componente.ram import RAM

class RAMSlot:
    def __init__(self, modulo: RAM | None = None):
        self._modulo = modulo
    
    @property
    def modulo(self) -> RAM | None:
        return self._modulo
    
    def instalar_ram(self, nueva_ram: RAM) -> bool:
        if self._modulo is None:
            self._modulo = nueva_ram
            return True
        return False
    
    def remover_ram(self) -> RAM | None:
        ram_removida = self._modulo
        self._modulo = None
        return ram_removida