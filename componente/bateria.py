from componente.componente import Componente
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class Bateria(Componente):
    def __init__(self, capacidad_mah: int, salud: int, esta_conectada: bool):
        super().__init__("Bateria")
        self._capacidad_mah = capacidad_mah
        self._salud = salud
        self._esta_conectada = esta_conectada
    
    @property
    def capacidad_mah(self) -> int:
        return self._capacidad_mah
    
    @property
    def salud(self) -> int:
        return self._salud
    
    @property
    def esta_conectada(self) -> bool:
        return self._esta_conectada
    
    def desconectar(self) -> ResultadoOperacion:
        pass
    
    def diagnosticar(self):
        if self._salud < 30:
            return "Bateria defectuosa"
        elif self._salud < 50:
            return "Bateria Operativa pero degradada"
        else:
            return "Bateria en buen estado"