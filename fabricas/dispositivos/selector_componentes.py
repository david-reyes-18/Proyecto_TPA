import random
from fabricas.dispositivos.catalogo_componentes import (DatosPlacaBase, DatosCPU, DatosGPU, DatosBateria, DatosPantalla, DatosRAMModulo, DatosSSD,)
from componentes.cpu.cpu import CPU
from componentes.gpu.gpu import GPU
from componentes.bateria.bateria import Bateria
from componentes.pantalla.pantalla import Pantalla
from componentes.ram.ram import RAM
from componentes.ram.ram_slots import RAMSlot
from componentes.ssd.ssd import SSD
from componentes.ssd.ssd_slot import SSDSlot
from componentes.placa_base import PlacaBase

class SelectorComponentes():
    
    @staticmethod
    def elegir_placa_base(placas: list[DatosPlacaBase])-> PlacaBase:
        return random.choice(placas)
    
    
    @staticmethod
    def elegir_cpu(placa_base: DatosPlacaBase, cpus: list[DatosCPU]) -> CPU:
        compatibles = [c for c in cpus if c.socket == placa_base.socket_compatible]
        if not compatibles:
            raise ValueError("No hay CPUs compatibles con la placa base.")
        c = random.choice(compatibles)
        return CPU(c.modelo, c.nucleos, c.frecuencia_ghz, c.socket, c.tdp_watts)
    
    
    @staticmethod
    def elegir_gpu(placa_base: DatosPlacaBase, gpus: list[DatosGPU]) -> GPU:
        compatibles = [gpu for gpu in gpus if gpu.interfaz == placa_base.interfaz_gpu]
        if not compatibles:
            raise ValueError("No hay GPUs compatibles con la placa base.")
        gpu = random.choice(compatibles)
        return GPU(gpu.modelo, gpu.memoria_gb, gpu.tipo_memoria, gpu.tipo_gpu, gpu.interfaz, gpu.tdp_watts)
    
    
    @staticmethod
    def elegir_pantalla(pantallas: list[DatosPantalla]) -> Pantalla:
        pantalla = random.choice(pantallas)
        return Pantalla(pantalla.pulgadas, pantalla.resolucion, pantalla.tipo_panel, pantalla.tasa_refresco_hz)
    
    
    @staticmethod
    def elegir_bateria(baterias: list[DatosBateria], salud: int) -> Bateria:
        bateria = random.choice(baterias)
        return Bateria(bateria.voltaje_v, bateria.forma, bateria.capacidad_wh, salud, esta_conectada=True)
    
    
    @staticmethod
    def armar_slots_ram(placa_base: DatosPlacaBase, rams: list[DatosRAMModulo]) -> list[RAMSlot]:

        n_llenar = random.randint(1, placa_base.n_slots_ram)

        compatibles = [
            ram for ram in rams
            if ram.generacion == placa_base.generacion_ram
            and ram.formato == placa_base.formato_ram
            and ram.velocidad_mhz <= placa_base.velocidad_maxima_ram_mhz
        ]

        slots = []
        for i in range(placa_base.n_slots_ram):
            slot = RAMSlot(
                capacidad_maxima_ram=placa_base.capacidad_maxima_ram_gb // placa_base.n_slots_ram,
                capacidad_maxima_mhz=placa_base.velocidad_maxima_ram_mhz,
                generacion_compatible=placa_base.generacion_ram,
                formato_compatible=placa_base.formato_ram,
            )
            if i < n_llenar and compatibles:
                ram = random.choice(compatibles)
                slot._modulo = RAM(ram.modelo, ram.capacidad_gb, ram.velocidad_mhz, ram.generacion, ram.formato)

            slots.append(slot)
        return slots

    @staticmethod
    def armar_slots_ssd(placa_base: DatosPlacaBase, ssds: list[DatosSSD]) -> list[SSDSlot]:
        
        n_llenar = random.randint(1, len(placa_base.slots_ssd))

        slots = []
        for i, slot_datos in enumerate(placa_base.slots_ssd):
            slot = SSDSlot(interfaz_soportada=slot_datos.interfaz)
            
            if i < n_llenar:
                compatibles = [ssd for ssd in ssds if ssd.interfaz == slot_datos.interfaz]
                if compatibles:
                    ssd = random.choice(compatibles)
                    slot._ssd_instalado = SSD(
                        modelo=ssd.modelo,
                        capacidad_gb=ssd.capacidad_gb,
                        interfaz=ssd.interfaz,
                        velocidad_lectura_mbps=ssd.velocidad_lectura_mbps,
                        velocidad_escritura_mbps=ssd.velocidad_escritura_mbps,
                    )
            
            slots.append(slot)
        return slots