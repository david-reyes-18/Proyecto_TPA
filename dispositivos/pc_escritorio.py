from __future__ import annotations
from dispositivos.dispositivo import Dispositivo
from problemas.problema import Problema
from componentes.componente import Componente
from componentes.cpu import CPU
from componentes.ram.ram import RAM
from componentes.ram.ram_slots import RAMSlot
from componentes.placa_base import PlacaBase
from componentes.ssd.ssd import SSD
from componentes.ssd.ssd_slot import SSDSlot
from componentes.gpu.gpu import GPU
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class PCEscritorio(Dispositivo):
    def __init__(
        self,
        modelo: str,
        cpu: CPU,
        gpu: GPU,
        slots_ram: list[RAMSlot],
        ssds: list[SSDSlot],
        placa_base: PlacaBase,
        fuente_watts: int,
        problema: Problema,
    ):
        componentes: list[Componente] = [cpu, gpu, placa_base]
        super().__init__(componentes, problema)

        self._modelo = modelo
        self._cpu = cpu
        self._gpu = gpu
        self._slots_ram = slots_ram
        self._ssds = ssds
        self._placa_base = placa_base
        self._fuente_watts = fuente_watts

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
    def ssds(self) -> list[SSDSlot]:
        return self._ssds

    @property
    def placa_base(self) -> PlacaBase:
        return self._placa_base

    @property
    def fuente_watts(self) -> int:
        return self._fuente_watts

    def instalar_ram_en_slot(self, indice_slot: int, nueva_ram: RAM) -> ResultadoOperacion:
        """Instala un módulo de RAM en el slot indicado (0-based)."""
        if indice_slot < 0 or indice_slot >= len(self._slots_ram):
            return ResultadoOperacion(
                exito_operacion=False,
                codigo_operacion=CodigoOperacion.INCOMPATIBLE,
                mensaje_sistema="El índice de slot no existe en este PC.",
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
        for i, slot in enumerate(self._ssd):          # ← NUEVO
            resultados[f"SSD Slot {i}"] = slot.diagnosticar()
        return resultados

    def __str__(self) -> str:
        return (
            f"PC Escritorio {self._modelo} | "
            f"CPU: {self._cpu.modelo} | "
            f"RAM: {self.ram_total_gb()} GB | "
            f"Almacenamiento: {self.almacenamiento_total_gb()} GB | "
            f"GPU: {self._gpu.modelo} | "
            f"Fuente: {self._fuente_watts}W | "
            f"Problema: {self._problema.descripcion}"
        )