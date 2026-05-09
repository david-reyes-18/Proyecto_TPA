import random
from fabricas.dispositivos.catalogo_componentes import CatalogoLaptop
from fabricas.dispositivos.fabrica_dispositivo import FabricaDispositivo
from dispositivos.laptop import Laptop

class FabricaLaptop(FabricaDispositivo):
    
    
    
    def crear_dispositivo_basico(self, problema):
        PLACA_BASE = random.choice(CatalogoLaptop.PLACAS_BASICA)
        
        