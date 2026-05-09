import random
from abc import ABC, abstractmethod
from problemas.problema import Problema
from dispositivos.dispositivo import Dispositivo
from fabricas.dispositivos.catalogo_componentes import DatosPlacaBase, DatosCPU, DatosGPU
from componentes.cpu.cpu import CPU
from componentes.gpu.gpu import GPU

class FabricaDispositivo(ABC):
    
    def elegir_cpu(self, placa_base: DatosPlacaBase, cpus: list[DatosCPU]) -> CPU:
        while True:
            cpu = random.choice(cpus)
            if cpu.socket == placa_base.socket_compatible:
                return CPU(
                    modelo=cpu.modelo,
                    nucleos=cpu.nucleos,
                    frecuencia_ghz=cpu.frecuencia_ghz,
                    socket=cpu.socket,
                    tdp_watts=cpu.tdp_watts
                )
    
    def elegir_cpu(self, placa_base: DatosPlacaBase, gpus: list[DatosGPU]) -> GPU:
        while True:
            gpu = random.choice(gpus)
            if gpu.interfaz == placa_base.interfaz_gpu:
                return GPU(
                    modelo=gpu.modelo,
                    memoria_gb=gpu.memoria_gb,
                    tipo_memoria=gpu.tipo_memoria,
                    tipo_gpu=gpu.tipo_gpu,
                    interfaz=gpu.interfaz,
                    tdp_watts=gpu.tdp_watts
                )
    
    @abstractmethod
    def crear_dispositivo_basico(self, problema: Problema) -> Dispositivo:
        pass
    
    @abstractmethod
    def crear_dispositivo_intermedio(self, problema: Problema) -> Dispositivo:
        pass
    
    @abstractmethod
    def crear_dispositivo_gamer(self, problema: Problema) -> Dispositivo:
        pass