
class Desafio:
    def __init__(self, enunciado: str, respuesta: float):
        self._enunciado = enunciado
        self._respuesta = respuesta
    
    #   Propiedades
    
    @property
    def enunciado(self) -> str:
        return self._enunciado
    
    @property
    def respuesta(self) -> float:
        return self._respuesta
