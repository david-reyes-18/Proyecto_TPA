import random
from fabricas.dispositivos.catalogo_componentes import CatalogoLaptop
from fabricas.dispositivos.fabrica_dispositivo import FabricaDispositivo
from dominio.entidades.dispositivos.laptop import Laptop
from fabricas.dispositivos.selector_componentes import SelectorComponentes
from dominio.entidades.componentes.placa_base import PlacaBase
from dominio.entidades.problemas.problema import Problema

class FabricaLaptop(FabricaDispositivo):

    def _crear_laptop(self, problema, placas, cpus, gpus, modulos_ram,
                    ssds, baterias, pantallas, modelos) -> Laptop:
        
        placa_datos = random.choice(placas)
        
        slots_ram = SelectorComponentes.armar_slots_ram(placa_datos, modulos_ram)
        slots_ssd = SelectorComponentes.armar_slots_ssd(placa_datos, ssds)
        
        placa_base = PlacaBase(
            modelo=placa_datos.modelo,
            generacion_ram=placa_datos.generacion_ram,
            formato_ram=placa_datos.formato_ram,
            velocidad_maxima_ram_mhz=placa_datos.velocidad_maxima_ram_mhz,
            slots_ram=slots_ram,
            slots_ssd=slots_ssd,
            cantidad_maxima_ram=placa_datos.capacidad_maxima_ram_gb,
            socket_compatible=placa_datos.socket_compatible,
            interfaz_gpu_compatible=placa_datos.interfaz_gpu,
        )
        
        return Laptop(
            modelo = random.choice(modelos),
            cpu = SelectorComponentes.elegir_cpu(placa_datos, cpus),
            gpu = SelectorComponentes.elegir_gpu(placa_datos, gpus),
            slots_ram = slots_ram,
            slots_ssd = slots_ssd,
            # Get salud from problema's componente if it's a Bateria, otherwise default
            bateria = SelectorComponentes.elegir_bateria(
                baterias,
                100 if not (hasattr(problema, 'componente_afectado') and hasattr(problema.componente_afectado, 'salud'))
                else problema.componente_afectado.salud
            ),
            pantalla = SelectorComponentes.elegir_pantalla(pantallas),
            placa_base = placa_base,
            problema = problema,
        )

    def crear_dispositivo_basico(self, problema: Problema) -> Laptop:
        return self._crear_laptop(
            problema = problema,
            placas = CatalogoLaptop.PLACAS_BASICA,
            cpus = CatalogoLaptop.CPUS_BASICA,
            gpus = CatalogoLaptop.GPUS_BASICA,
            modulos_ram = CatalogoLaptop.MODULOS_RAM_BASICA,
            ssds = CatalogoLaptop.SSDS_BASICA,
            baterias = CatalogoLaptop.BATERIAS_BASICA,
            pantallas = CatalogoLaptop.PANTALLAS_BASICA,
            modelos = CatalogoLaptop.MODELOS_BASICA,
        )

    def crear_dispositivo_intermedio(self, problema: Problema) -> Laptop:
        return self._crear_laptop(
            problema = problema,
            placas = CatalogoLaptop.PLACAS_INTERMEDIA,
            cpus = CatalogoLaptop.CPUS_INTERMEDIA,
            gpus = CatalogoLaptop.GPUS_INTERMEDIA,
            modulos_ram = CatalogoLaptop.MODULOS_RAM_INTERMEDIA,
            ssds = CatalogoLaptop.SSDS_INTERMEDIA,
            baterias = CatalogoLaptop.BATERIAS_INTERMEDIA,
            pantallas = CatalogoLaptop.PANTALLAS_INTERMEDIA,
            modelos = CatalogoLaptop.MODELOS_INTERMEDIA,
        )

    def crear_dispositivo_gamer(self, problema: Problema) -> Laptop:
        return self._crear_laptop(
            problema = problema,
            placas = CatalogoLaptop.PLACAS_GAMER,
            cpus = CatalogoLaptop.CPUS_GAMER,
            gpus = CatalogoLaptop.GPUS_GAMER,
            modulos_ram = CatalogoLaptop.MODULOS_RAM_GAMER,
            ssds = CatalogoLaptop.SSDS_GAMER,
            baterias = CatalogoLaptop.BATERIAS_GAMER,
            pantallas = CatalogoLaptop.PANTALLAS_GAMER,
            modelos = CatalogoLaptop.MODELOS_GAMER,
        )