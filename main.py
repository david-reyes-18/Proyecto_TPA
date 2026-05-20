import random
from problemas.problema import Problema
from fabricas.dispositivos.catalogo_componentes import CatalogoLaptop
from fabricas.desafios.fabrica_desafios_catalogo import FabricaDesafiosCatalogo
from desafios.desafio import Desafio
from desafios.categoria_desafio import CategoriaDesafio
from desafios.componente_tematico import ComponenteTematico
from desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from desafios.dificultad_desafio import NivelDificultad
from componentes.cpu.cpu import CPU

print(random.choice(FabricaDesafiosCatalogo.crear_desafio(
    categoria=CategoriaDesafio.MATEMATICO, 
    componente=ComponenteTematico.CPU, 
    tipo=NombreTipoDesafio.MULTIPLE, 
    dificultad=NivelDificultad.FACIL
    )))