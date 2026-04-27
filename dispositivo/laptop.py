from dispositivo.dispositivo import Dispositivo

class Laptop(Dispositivo):
    def __init__(self, componentes, problema):
        super().__init__(componentes, problema)