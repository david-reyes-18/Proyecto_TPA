from componente.componente import Componente

class Pantalla(Componente):
    def __init__(self, pulgadas: int, resolucion: str):
        super().__init__("Pantalla")
        self._pulgadas = pulgadas
        self._resolucion = resolucion
    
    @property
    def pulgadas(self) -> int:
        return self._pulgadas
    
    @property
    def resolucion(self) -> str:
        return self._resolucion
    
    def diagnosticar(self) -> str:
        if not self.esta_funcionando:
            return "Estado de Pantalla: Rota"
        return "Estado de Pantalla: Funcional"