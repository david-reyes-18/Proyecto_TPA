import random
from fabricas.dispositivos.fabrica_laptop import FabricaLaptop
from problemas.problema import Problema
from fabricas.dispositivos.catalogo_componentes import CatalogoLaptop

print(random.choice(CatalogoLaptop.PLACAS_BASICA).modelo)