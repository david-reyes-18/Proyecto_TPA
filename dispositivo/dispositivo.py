from abc import ABC, abstractmethod

class Dispositivo(ABC):
    def __init__(self, componentes: list, problema, esta_reparado: bool):
        self.componentes = componentes
        self.problema = problema
        self.esta_reparado = esta_reparado