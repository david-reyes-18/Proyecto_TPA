import random
from fabricas.dispositivos.catalogo_componentes import CatalogoPCEscritorio
from fabricas.dispositivos.fabrica_dispositivo import FabricaDispositivo
from dominio.entidades.dispositivos.pc_escritorio import PCEscritorio
from fabricas.dispositivos.selector_componentes import SelectorComponentes
from dominio.entidades.componentes.placa_base import PlacaBase
from dominio.entidades.problemas.problema import Problema

class FabricaEscritorio(FabricaDispositivo):

    def _crear_escritorio(self, problema, placas, cpus, gpus, modulos_ram,
                        ssds, fuentes, modelos) -> PCEscritorio:
        
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
        
        return PCEscritorio(
            modelo = random.choice(modelos),
            cpu = SelectorComponentes.elegir_cpu(placa_datos, cpus),
            gpu = SelectorComponentes.elegir_gpu(placa_datos, gpus),
            slots_ram = slots_ram,
            slots_ssd = slots_ssd,
            placa_base = placa_base,
            fuente_watts = random.choice(fuentes),
            problema = problema,
        )

    def crear_dispositivo_basico(self, problema: Problema) -> PCEscritorio:
        return self._crear_escritorio(
            problema = problema,
            placas = CatalogoPCEscritorio.PLACAS_BASICA,
            cpus = CatalogoPCEscritorio.CPUS_BASICA,
            gpus = CatalogoPCEscritorio.GPUS_BASICA,
            modulos_ram = CatalogoPCEscritorio.MODULOS_RAM_BASICA,
            ssds = CatalogoPCEscritorio.SSDS_BASICA,
            fuentes = CatalogoPCEscritorio.FUENTES_BASICA,
            modelos = CatalogoPCEscritorio.MODELOS_BASICA,
        )

    def crear_dispositivo_intermedio(self, problema: Problema) -> PCEscritorio:
        modulos_ram = (CatalogoPCEscritorio.MODULOS_RAM_INTERMEDIA_DDR4
                    + CatalogoPCEscritorio.MODULOS_RAM_INTERMEDIA_DDR5)
        return self._crear_escritorio(
            problema = problema,
            placas = CatalogoPCEscritorio.PLACAS_INTERMEDIA,
            cpus = CatalogoPCEscritorio.CPUS_INTERMEDIA,
            gpus = CatalogoPCEscritorio.GPUS_INTERMEDIA,
            modulos_ram = modulos_ram,
            ssds = CatalogoPCEscritorio.SSDS_INTERMEDIA,
            fuentes = CatalogoPCEscritorio.FUENTES_INTERMEDIA,
            modelos = CatalogoPCEscritorio.MODELOS_INTERMEDIA,
        )

    def crear_dispositivo_gamer(self, problema: Problema) -> PCEscritorio:
        return self._crear_escritorio(
            problema = problema,
            placas = CatalogoPCEscritorio.PLACAS_GAMER,
            cpus = CatalogoPCEscritorio.CPUS_GAMER,
            gpus = CatalogoPCEscritorio.GPUS_GAMER,
            modulos_ram = CatalogoPCEscritorio.MODULOS_RAM_GAMER,
            ssds = CatalogoPCEscritorio.SSDS_GAMER,
            fuentes = CatalogoPCEscritorio.FUENTES_GAMER, 
            modelos = CatalogoPCEscritorio.MODELOS_GAMER,
        )