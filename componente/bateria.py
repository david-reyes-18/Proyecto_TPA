from componente.componente import Componente

class Bateria(Componente):
    def __init__(self, capacidad_mah: int, salud: int):
        super().__init__("Bateria")
        self._capacidad_mah = capacidad_mah
        self._salud = salud
    
    @property
    def capacidad_mah(self) -> int:
        return self._capacidad_mah
    
    @property
    def salud(self) -> int:
        return self._salud
    
    def diagnosticar(self):
        if self._salud < 30:
            return "Bateria defectuosa"
        elif self._salud < 50:
            return "Bateria Operativa pero degradada"
        else:
            return "Bateria en buen estado"