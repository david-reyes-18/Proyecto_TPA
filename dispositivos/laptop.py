from __future__ import annotations
from dispositivos.dispositivo import Dispositivo
from problemas.problema import Problema
from componentes.componente import Componente
from componentes.cpu import CPU
from componentes.ram.ram import RAM
from componentes.ram.ram_slots import RAMSlot
from componentes.bateria.bateria import Bateria
from componentes.pantalla import Pantalla
from componentes.placa_base import PlacaBase
from componentes.ssd.ssd import SSD
from componentes.ssd.ssd_slot import SSDSlot
from componentes.gpu.gpu import GPU
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class Laptop(Dispositivo):
    def __init__(
        self,
        modelo: str,
        cpu: CPU,
        gpu: GPU,
        slots_ram: list[RAMSlot],
        ssd: list[SSDSlot],
        bateria: Bateria,
        pantalla: Pantalla,
        placa_base: PlacaBase,
        problema: Problema,
    ):
        componentes: list[Componente] = [cpu, gpu, pantalla, placa_base]
        super().__init__(componentes, problema)

        self._modelo = modelo
        self._cpu = cpu
        self._gpu = gpu
        self._slots_ram = slots_ram
        self._ssd = ssd
        self._bateria = bateria
        self._pantalla = pantalla
        self._placa_base = placa_base

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def cpu(self) -> CPU:
        return self._cpu

    @property
    def gpu(self) -> GPU:
        return self._gpu

    @property
    def slots_ram(self) -> list[RAMSlot]:
        return self._slots_ram

    @property
    def ssd(self) -> SSD:
        return self._ssd

    @property
    def bateria(self) -> Bateria:
        return self._bateria

    @property
    def pantalla(self) -> Pantalla:
        return self._pantalla

    @property
    def placa_base(self) -> PlacaBase:
        return self._placa_base

    def instalar_ram_en_slot(self, indice_slot: int, nueva_ram: RAM) -> ResultadoOperacion:
        if indice_slot < 0 or indice_slot >= len(self._slots_ram):
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="El índice de slot no existe en esta laptop.",
            )
        return self._slots_ram[indice_slot].instalar_ram(nueva_ram)

    def ram_total_gb(self) -> int:
        return sum(
            slot.modulo.capacidad_gb for slot in self._slots_ram if slot.modulo is not None
        )
    
    def almacenamiento_total_gb(self) -> int:
        return sum(
            slot.ssd_instalado.capacidad_gb
            for slot in self._ssds
            if slot.ssd_instalado is not None
        )
    
    def diagnosticar_todo(self) -> dict[str, ResultadoOperacion]:
        resultados: dict[str, ResultadoOperacion] = {}
        for componente in self._componentes:
            resultados[componente.nombre] = componente.diagnosticar()
        for i, slot in enumerate(self._slots_ram):
            if slot.modulo is not None:
                resultados[f"RAM Slot {i}"] = slot.modulo.diagnosticar()
        for i, slot in enumerate(self._ssd):
            resultados[f"SSD Slot {i}"] = slot.diagnosticar()
        return resultados

    def __str__(self) -> str:
        return (
            f"Laptop {self._modelo} | "
            f"CPU: {self._cpu.modelo} | "
            f"RAM: {self.ram_total_gb()} GB | "
            f"SSD: {self._ssd.capacidad_gb} GB | "
            f"Pantalla: {self._pantalla.pulgadas}\" | "
            f"Batería: {self._bateria.salud}% salud | "
            f"Problema: {self._problema.descripcion}"
        )
