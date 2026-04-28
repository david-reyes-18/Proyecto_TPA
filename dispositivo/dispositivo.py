from problema.problema import Problema
from componente.componente import Componente

class Dispositivo:
    def __init__(self, componentes: list[Componente], problema: Problema):
        self._componentes = componentes
        self._problema = problema
        self._esta_reparado = False
    
    @property
    def componentes(self) -> list[Componente]:
        return self._componentes
    
    @property
    def problema(self) -> Problema:
        return self._problema
    
    @property
    def esta_reparado(self) -> bool:
        return self._esta_reparado
    
    def marcar_reparado(self):
        self._esta_reparado = True
    
    def obtener_componente(self, nombre: str) -> Componente | None:
        for componente in self._componentes:
            if componente.nombre.lower() == nombre.lower():
                return componente
        return None
    
    def diagnosticar(self) -> list[str]:
        diagnosticos = []
        for componente in self._componentes:
            diagnosticos.append(componente.diagnosticar())
        return diagnosticos