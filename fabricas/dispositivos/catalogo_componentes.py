"""
catalogo_componentes.py
=======================
Catálogo centralizado de hardware realista para el simulador TPA.

Arquitectura:
- DatosPlacaBase es el eje central: define los parámetros que restringen
todos los demás componentes.
- Los catálogos de CPU, GPU, RAM y SSD están enlazados a las restricciones
de la placa base de su categoría.
- La aleatoriedad controlada se delega a las fábricas, no al catálogo.
"""

from dataclasses import dataclass
from componentes.cpu.socket import SocketCPU
from componentes.gpu.tipo_gpu import TipoGPU
from componentes.gpu.tipo_memoria_gpu import TipoMemoriaGPU
from componentes.gpu.tipo_interfaz import InterfazGPU
from componentes.ram.generacion_ram import GeneracionRAM
from componentes.ram.formato_ram import FormatoRAM
from componentes.ssd.interfaz_ssd import InterfazSSD
from componentes.bateria.forma_bateria import FormaBateria
from componentes.pantalla.pantalla import TipoPanel


# ─────────────────────────────────────────────────────────────────────────────
#  DTOs (inmutables, sólo datos)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class DatosCPU:
    modelo: str
    nucleos: int
    frecuencia_ghz: float
    socket: SocketCPU
    tdp_watts: int


@dataclass(frozen=True)
class DatosGPU:
    modelo: str
    memoria_gb: int
    tipo_memoria: TipoMemoriaGPU
    tipo_gpu: TipoGPU
    interfaz: InterfazGPU
    tdp_watts: int


@dataclass(frozen=True)
class DatosRAMSlot:
    capacidad_maxima_gb: int
    velocidad_maxima_mhz: int
    generacion: GeneracionRAM
    formato: FormatoRAM


@dataclass(frozen=True)
class DatosSSDSlot:
    interfaz: InterfazSSD


@dataclass(frozen=True)
class DatosPlacaBase:
    """
    Núcleo de restricciones del sistema.
    Todo componente debe ser compatible con esta placa.
    """
    modelo: str
    socket_compatible: SocketCPU
    generacion_ram: GeneracionRAM
    formato_ram: FormatoRAM
    velocidad_maxima_ram_mhz: int
    n_slots_ram: int
    capacidad_maxima_ram_gb: int
    slots_ssd: tuple[DatosSSDSlot, ...]      # slots disponibles
    interfaz_gpu: InterfazGPU
    cantidad_slots_gpu: int                   # 0 = laptop, 1+ = desktop


@dataclass(frozen=True)
class DatosRAMModulo:
    """Un módulo específico que puede instalarse en un slot compatible."""
    modelo: str
    capacidad_gb: int
    velocidad_mhz: int
    generacion: GeneracionRAM
    formato: FormatoRAM


@dataclass(frozen=True)
class DatosSSD:
    modelo: str
    capacidad_gb: int
    interfaz: InterfazSSD
    velocidad_lectura_mbps: int
    velocidad_escritura_mbps: int


@dataclass(frozen=True)
class DatosBateria:
    voltaje_v: float
    capacidad_wh: float
    forma: FormaBateria


@dataclass(frozen=True)
class DatosPantalla:
    pulgadas: float
    resolucion: str
    tipo_panel: TipoPanel
    tasa_refresco_hz: int


# ─────────────────────────────────────────────────────────────────────────────
#  CATÁLOGO LAPTOPS
# ─────────────────────────────────────────────────────────────────────────────

class CatalogoLaptop:
    """
    Componentes para laptops organizados por categoría.
    Todas las CPUs de laptop usan socket BGA (soldadas).
    GPU integrada para básica, MXM para intermedia/gamer.
    RAM formato SO-DIMM o LPDDR (soldada en ultrafinos).
    """

    # ── PLACAS BASE (definen las restricciones de cada categoría) ────────────

    PLACAS_BASICA: list[DatosPlacaBase] = [
        DatosPlacaBase(
            modelo="Intel N-Series Mobile Platform",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.SO_DIMM,
            velocidad_maxima_ram_mhz=3200,
            n_slots_ram=2,
            capacidad_maxima_ram_gb=16,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_SATA), DatosSSDSlot(InterfazSSD.SATA)),
            interfaz_gpu=InterfazGPU.INTEGRADA,
            cantidad_slots_gpu=0,
        ),
        DatosPlacaBase(
            modelo="AMD Mendocino / Barcelo-R Mobile",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.SO_DIMM,
            velocidad_maxima_ram_mhz=3200,
            n_slots_ram=2,
            capacidad_maxima_ram_gb=16,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_NVME),),
            interfaz_gpu=InterfazGPU.INTEGRADA,
            cantidad_slots_gpu=0,
        ),
        DatosPlacaBase(
            modelo="Intel Alder Lake-U Low Power",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.LPDDR4X,
            formato_ram=FormatoRAM.LPDDR,
            velocidad_maxima_ram_mhz=4267,
            n_slots_ram=1,             # soldada — 1 "slot" lógico
            capacidad_maxima_ram_gb=8,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_NVME),),
            interfaz_gpu=InterfazGPU.INTEGRADA,
            cantidad_slots_gpu=0,
        ),
    ]

    PLACAS_INTERMEDIA: list[DatosPlacaBase] = [
        DatosPlacaBase(
            modelo="Intel Raptor Lake-U/P Mobile",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.SO_DIMM,
            velocidad_maxima_ram_mhz=4800,
            n_slots_ram=2,
            capacidad_maxima_ram_gb=32,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_NVME), DatosSSDSlot(InterfazSSD.M2_NVME)),
            interfaz_gpu=InterfazGPU.MXM,
            cantidad_slots_gpu=0,     # MXM soldado en intermedias — no usuario-reemplazable
        ),
        DatosPlacaBase(
            modelo="AMD Phoenix / Rembrandt Mobile",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.SO_DIMM,
            velocidad_maxima_ram_mhz=4800,
            n_slots_ram=2,
            capacidad_maxima_ram_gb=32,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_NVME), DatosSSDSlot(InterfazSSD.M2_NVME)),
            interfaz_gpu=InterfazGPU.MXM,
            cantidad_slots_gpu=0,
        ),
        DatosPlacaBase(
            modelo="Intel Meteor Lake-U Mobile",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.LPDDR5,
            formato_ram=FormatoRAM.LPDDR,
            velocidad_maxima_ram_mhz=6400,
            n_slots_ram=1,
            capacidad_maxima_ram_gb=32,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_NVME),),
            interfaz_gpu=InterfazGPU.MXM,
            cantidad_slots_gpu=0,
        ),
    ]

    PLACAS_GAMER: list[DatosPlacaBase] = [
        DatosPlacaBase(
            modelo="Intel Raptor Lake-HX Gaming Mobile",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.SO_DIMM,
            velocidad_maxima_ram_mhz=5600,
            n_slots_ram=2,
            capacidad_maxima_ram_gb=64,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_SATA),
            ),
            interfaz_gpu=InterfazGPU.MXM,
            cantidad_slots_gpu=0,
        ),
        DatosPlacaBase(
            modelo="AMD Dragon Range / Storm Peak Gaming Mobile",
            socket_compatible=SocketCPU.BGA,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.SO_DIMM,
            velocidad_maxima_ram_mhz=5600,
            n_slots_ram=2,
            capacidad_maxima_ram_gb=64,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
            ),
            interfaz_gpu=InterfazGPU.MXM,
            cantidad_slots_gpu=0,
        ),
    ]

    # ── CPUs ─────────────────────────────────────────────────────────────────

    CPUS_BASICA: list[DatosCPU] = [
        DatosCPU("Intel Celeron N4020",         2,  2.8, SocketCPU.BGA,  6),
        DatosCPU("Intel Celeron N4500",         2,  2.8, SocketCPU.BGA,  6),
        DatosCPU("Intel Celeron N5100",         4,  2.8, SocketCPU.BGA,  6),
        DatosCPU("Intel Pentium Silver N5030",  4,  3.1, SocketCPU.BGA,  6),
        DatosCPU("Intel Pentium Silver N6000",  4,  3.3, SocketCPU.BGA,  6),
        DatosCPU("Intel Core i3-1005G1",        2,  3.4, SocketCPU.BGA, 15),
        DatosCPU("Intel Core i3-1115G4",        2,  4.1, SocketCPU.BGA, 15),
        DatosCPU("Intel Core i3-1215U",         6,  4.4, SocketCPU.BGA, 15),
        DatosCPU("AMD Athlon Silver 3050U",     2,  3.2, SocketCPU.BGA, 15),
        DatosCPU("AMD Athlon Gold 3150U",       2,  3.3, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 3 3250U",           2,  3.5, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 3 5300U",           4,  3.8, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 3 7320U",           4,  4.1, SocketCPU.BGA, 15),
    ]

    CPUS_INTERMEDIA: list[DatosCPU] = [
        DatosCPU("Intel Core i5-10210U",        4,  4.2, SocketCPU.BGA, 15),
        DatosCPU("Intel Core i5-1135G7",        4,  4.2, SocketCPU.BGA, 28),
        DatosCPU("Intel Core i5-1235U",        10,  4.4, SocketCPU.BGA, 15),
        DatosCPU("Intel Core i5-1240P",        12,  4.4, SocketCPU.BGA, 28),
        DatosCPU("Intel Core i5-1335U",        10,  4.6, SocketCPU.BGA, 15),
        DatosCPU("Intel Core i5-1340P",        12,  4.6, SocketCPU.BGA, 28),
        DatosCPU("Intel Core i7-1165G7",        4,  4.7, SocketCPU.BGA, 28),
        DatosCPU("Intel Core i7-1255U",        10,  4.7, SocketCPU.BGA, 15),
        DatosCPU("Intel Core i7-1260P",        12,  4.7, SocketCPU.BGA, 28),
        DatosCPU("Intel Core i7-1360P",        13,  5.0, SocketCPU.BGA, 28),
        DatosCPU("AMD Ryzen 5 4500U",           6,  4.0, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 5 5500U",           6,  4.0, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 5 5600U",           6,  4.2, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 5 7530U",           6,  4.5, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 5 7540U",           6,  4.9, SocketCPU.BGA, 28),
        DatosCPU("AMD Ryzen 7 5700U",           8,  4.3, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 7 7730U",           8,  4.5, SocketCPU.BGA, 15),
        DatosCPU("AMD Ryzen 7 7745U",           8,  5.1, SocketCPU.BGA, 28),
    ]

    CPUS_GAMER: list[DatosCPU] = [
        DatosCPU("Intel Core i7-12700H",       14,  4.7, SocketCPU.BGA, 45),
        DatosCPU("Intel Core i7-13700H",       14,  5.0, SocketCPU.BGA, 45),
        DatosCPU("Intel Core i7-14700HX",      20,  5.5, SocketCPU.BGA, 55),
        DatosCPU("Intel Core i9-12900H",       20,  5.0, SocketCPU.BGA, 45),
        DatosCPU("Intel Core i9-13900H",       20,  5.4, SocketCPU.BGA, 45),
        DatosCPU("Intel Core i9-13900HX",      24,  5.6, SocketCPU.BGA, 55),
        DatosCPU("Intel Core i9-14900HX",      24,  5.8, SocketCPU.BGA, 55),
        DatosCPU("AMD Ryzen 7 6800H",           8,  4.7, SocketCPU.BGA, 45),
        DatosCPU("AMD Ryzen 7 7745HX",          8,  5.1, SocketCPU.BGA, 55),
        DatosCPU("AMD Ryzen 7 8845HS",          8,  5.1, SocketCPU.BGA, 45),
        DatosCPU("AMD Ryzen 9 6900HX",          8,  4.9, SocketCPU.BGA, 45),
        DatosCPU("AMD Ryzen 9 7940HX",         16,  5.4, SocketCPU.BGA, 55),
        DatosCPU("AMD Ryzen 9 7945HX",         16,  5.4, SocketCPU.BGA, 55),
        DatosCPU("AMD Ryzen 9 8945HS",          8,  5.2, SocketCPU.BGA, 45),
    ]

    # ── GPUs ─────────────────────────────────────────────────────────────────

    GPUS_BASICA: list[DatosGPU] = [
        DatosGPU("Intel UHD Graphics 600",       0, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
        DatosGPU("Intel UHD Graphics 620",       0, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
        DatosGPU("Intel UHD Graphics 730",       0, TipoMemoriaGPU.DDR4,    TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
        DatosGPU("Intel Iris Xe Graphics",       0, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
        DatosGPU("AMD Radeon Graphics Vega 3",   0, TipoMemoriaGPU.DDR4,    TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
        DatosGPU("AMD Radeon Graphics Vega 6",   0, TipoMemoriaGPU.DDR4,    TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
        DatosGPU("AMD Radeon 610M",              0, TipoMemoriaGPU.LPDDR5,  TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
        DatosGPU("AMD Radeon 740M",              0, TipoMemoriaGPU.LPDDR5,  TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA,  0),
    ]
    # Nota: memoria_gb=0 para iGPU porque usa memoria del sistema (shared memory).
    # Las fábricas asignarán el valor correcto según la RAM instalada.

    GPUS_INTERMEDIA: list[DatosGPU] = [
        DatosGPU("NVIDIA GeForce MX450",        2, TipoMemoriaGPU.GDDR5,  TipoGPU.DEDICADA, InterfazGPU.MXM,  35),
        DatosGPU("NVIDIA GeForce MX550",        2, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  35),
        DatosGPU("NVIDIA RTX 2050 Laptop",      4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  45),
        DatosGPU("NVIDIA RTX 3050 Laptop",      4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  60),
        DatosGPU("NVIDIA RTX 3050 Ti Laptop",   4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  60),
        DatosGPU("NVIDIA RTX 4050 Laptop",      6, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  60),
        DatosGPU("AMD Radeon RX 6500M",         4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  50),
        DatosGPU("AMD Radeon RX 6600M",         8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  60),
        DatosGPU("AMD Radeon RX 6650M",         8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  60),
        DatosGPU("AMD Radeon RX 7600M XT",      8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  65),
        DatosGPU("Intel Arc A370M",             4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  35),
        DatosGPU("Intel Arc A530M",             8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM,  50),
    ]

    GPUS_GAMER: list[DatosGPU] = [
        DatosGPU("NVIDIA RTX 3070 Ti Laptop",   8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 125),
        DatosGPU("NVIDIA RTX 3080 Laptop",     16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 150),
        DatosGPU("NVIDIA RTX 3080 Ti Laptop",  16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 150),
        DatosGPU("NVIDIA RTX 4060 Laptop",      8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 115),
        DatosGPU("NVIDIA RTX 4070 Laptop",      8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 115),
        DatosGPU("NVIDIA RTX 4070 Ti Laptop",  12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.MXM, 150),
        DatosGPU("NVIDIA RTX 4080 Laptop",     12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.MXM, 150),
        DatosGPU("NVIDIA RTX 4090 Laptop",     16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.MXM, 175),
        DatosGPU("AMD Radeon RX 6700M",        10, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 100),
        DatosGPU("AMD Radeon RX 6800M",        12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 145),
        DatosGPU("AMD Radeon RX 6850M XT",     12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 145),
        DatosGPU("AMD Radeon RX 7900M",        16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM, 150),
    ]

    # ── Módulos RAM ──────────────────────────────────────────────────────────

    MODULOS_RAM_BASICA: list[DatosRAMModulo] = [
        DatosRAMModulo("Samsung DDR4 SO-DIMM",   4, 2666, GeneracionRAM.DDR4, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Samsung DDR4 SO-DIMM",   8, 2666, GeneracionRAM.DDR4, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Samsung DDR4 SO-DIMM",   8, 3200, GeneracionRAM.DDR4, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Crucial DDR4 SO-DIMM",   4, 2666, GeneracionRAM.DDR4, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Crucial DDR4 SO-DIMM",   8, 3200, GeneracionRAM.DDR4, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Kingston DDR4 SO-DIMM",  8, 2666, GeneracionRAM.DDR4, FormatoRAM.SO_DIMM),
        # LPDDR4X soldada (para placa Alder Lake-U low power)
        DatosRAMModulo("LPDDR4X Soldada",        4, 4267, GeneracionRAM.LPDDR4X, FormatoRAM.LPDDR),
        DatosRAMModulo("LPDDR4X Soldada",        8, 4267, GeneracionRAM.LPDDR4X, FormatoRAM.LPDDR),
    ]

    MODULOS_RAM_INTERMEDIA: list[DatosRAMModulo] = [
        DatosRAMModulo("Samsung DDR5 SO-DIMM",   8, 4800, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Samsung DDR5 SO-DIMM",  16, 4800, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Crucial DDR5 SO-DIMM",  16, 4800, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Kingston DDR5 SO-DIMM", 16, 4800, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Kingston DDR5 SO-DIMM", 32, 4800, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        # LPDDR5 soldada
        DatosRAMModulo("LPDDR5 Soldada",        16, 6400, GeneracionRAM.LPDDR5, FormatoRAM.LPDDR),
        DatosRAMModulo("LPDDR5 Soldada",        32, 6400, GeneracionRAM.LPDDR5, FormatoRAM.LPDDR),
    ]

    MODULOS_RAM_GAMER: list[DatosRAMModulo] = [
        DatosRAMModulo("Samsung DDR5 SO-DIMM",  16, 5600, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Samsung DDR5 SO-DIMM",  32, 5600, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("G.Skill Ripjaws DDR5",  16, 5600, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("G.Skill Ripjaws DDR5",  32, 5600, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Corsair Vengeance DDR5",32, 5600, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
        DatosRAMModulo("Kingston Fury DDR5",    32, 5600, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
    ]

    # ── SSDs ─────────────────────────────────────────────────────────────────

    SSDS_BASICA: list[DatosSSD] = [
        DatosSSD("Kingston A400 M.2",     128, InterfazSSD.M2_SATA,  500,  320),
        DatosSSD("Kingston A400 M.2",     256, InterfazSSD.M2_SATA,  500,  350),
        DatosSSD("Samsung 870 EVO SATA",  256, InterfazSSD.SATA,     560,  530),
        DatosSSD("Samsung 870 EVO SATA",  512, InterfazSSD.SATA,     560,  530),
        DatosSSD("WD Blue SATA",          256, InterfazSSD.SATA,     560,  530),
        DatosSSD("WD Blue M.2 SATA",      256, InterfazSSD.M2_SATA,  540,  500),
        DatosSSD("Crucial BX500",         480, InterfazSSD.SATA,     540,  500),
    ]

    SSDS_INTERMEDIA: list[DatosSSD] = [
        DatosSSD("Samsung 980 NVMe",       256, InterfazSSD.M2_NVME, 3500, 3000),
        DatosSSD("Samsung 980 NVMe",       512, InterfazSSD.M2_NVME, 3500, 3000),
        DatosSSD("Samsung 980 Pro NVMe",   512, InterfazSSD.M2_NVME, 7000, 5000),
        DatosSSD("Samsung 980 Pro NVMe",  1024, InterfazSSD.M2_NVME, 7000, 5000),
        DatosSSD("WD Black SN770",         512, InterfazSSD.M2_NVME, 5150, 4900),
        DatosSSD("WD Black SN770",        1024, InterfazSSD.M2_NVME, 5150, 4900),
        DatosSSD("Kingston NV2",           512, InterfazSSD.M2_NVME, 3500, 2100),
        DatosSSD("Crucial P3 Plus",        512, InterfazSSD.M2_NVME, 5000, 4200),
        DatosSSD("Crucial P3 Plus",       1024, InterfazSSD.M2_NVME, 5000, 4200),
    ]

    SSDS_GAMER: list[DatosSSD] = [
        DatosSSD("Samsung 990 Pro NVMe",   1024, InterfazSSD.M2_NVME, 7450, 6900),
        DatosSSD("Samsung 990 Pro NVMe",   2048, InterfazSSD.M2_NVME, 7450, 6900),
        DatosSSD("WD Black SN850X",        1024, InterfazSSD.M2_NVME, 7300, 6600),
        DatosSSD("WD Black SN850X",        2048, InterfazSSD.M2_NVME, 7300, 6600),
        DatosSSD("Seagate FireCuda 530",   1024, InterfazSSD.M2_NVME, 7300, 6900),
        DatosSSD("Seagate FireCuda 530",   2048, InterfazSSD.M2_NVME, 7300, 6900),
        DatosSSD("Corsair MP600 Pro",      1024, InterfazSSD.M2_NVME, 7100, 6800),
        DatosSSD("Kingston Fury Renegade", 2048, InterfazSSD.M2_NVME, 7300, 7000),
    ]

    # ── Baterías ─────────────────────────────────────────────────────────────

    BATERIAS_BASICA: list[DatosBateria] = [
        DatosBateria(11.4, 38.0, FormaBateria.RECTANGULAR),
        DatosBateria(11.4, 41.5, FormaBateria.RECTANGULAR),
        DatosBateria(11.4, 45.0, FormaBateria.RECTANGULAR),
        DatosBateria(10.8, 48.0, FormaBateria.RECTANGULAR),
    ]

    BATERIAS_INTERMEDIA: list[DatosBateria] = [
        DatosBateria(11.4, 52.5, FormaBateria.RECTANGULAR),
        DatosBateria(15.2, 56.0, FormaBateria.RECTANGULAR),
        DatosBateria(15.4, 63.5, FormaBateria.RECTANGULAR),
        DatosBateria(15.4, 70.0, FormaBateria.RECTANGULAR),
        DatosBateria(11.4, 72.0, FormaBateria.FORMA_L),
    ]

    BATERIAS_GAMER: list[DatosBateria] = [
        DatosBateria(15.4, 72.0, FormaBateria.RECTANGULAR),
        DatosBateria(15.4, 80.0, FormaBateria.RECTANGULAR),
        DatosBateria(15.4, 86.0, FormaBateria.IRREGULAR),
        DatosBateria(15.4, 90.0, FormaBateria.RECTANGULAR),
        DatosBateria(20.0, 99.9, FormaBateria.RECTANGULAR),  # Límite aerolíneas
    ]

    # ── Pantallas ─────────────────────────────────────────────────────────────

    PANTALLAS_BASICA: list[DatosPantalla] = [
        DatosPantalla(14.0, "1366x768",   TipoPanel.TN,  60),
        DatosPantalla(14.0, "1920x1080",  TipoPanel.IPS, 60),
        DatosPantalla(15.6, "1366x768",   TipoPanel.TN,  60),
        DatosPantalla(15.6, "1920x1080",  TipoPanel.IPS, 60),
        DatosPantalla(15.6, "1600x900",   TipoPanel.TN,  60),
    ]

    PANTALLAS_INTERMEDIA: list[DatosPantalla] = [
        DatosPantalla(14.0, "1920x1080",  TipoPanel.IPS, 60),
        DatosPantalla(14.0, "2560x1600",  TipoPanel.IPS, 90),
        DatosPantalla(15.6, "1920x1080",  TipoPanel.IPS, 60),
        DatosPantalla(15.6, "1920x1200",  TipoPanel.IPS, 60),
        DatosPantalla(16.0, "2560x1600",  TipoPanel.IPS, 120),
        DatosPantalla(16.0, "1920x1200",  TipoPanel.IPS, 60),
    ]

    PANTALLAS_GAMER: list[DatosPantalla] = [
        DatosPantalla(15.6, "1920x1080",  TipoPanel.IPS, 144),
        DatosPantalla(15.6, "1920x1080",  TipoPanel.IPS, 240),
        DatosPantalla(15.6, "2560x1440",  TipoPanel.IPS, 165),
        DatosPantalla(16.0, "2560x1600",  TipoPanel.IPS, 240),
        DatosPantalla(17.3, "1920x1080",  TipoPanel.IPS, 144),
        DatosPantalla(17.3, "2560x1440",  TipoPanel.IPS, 165),
        DatosPantalla(18.0, "2560x1600",  TipoPanel.IPS, 240),
        DatosPantalla(16.0, "2560x1600",  TipoPanel.OLED, 120),
    ]

    # ── Modelos de equipo ─────────────────────────────────────────────────────

    MODELOS_BASICA: list[str] = [
        "Acer Aspire 3 A315",        "Acer Aspire 5 A515",
        "ASUS VivoBook Go 14",       "ASUS VivoBook Go 15",
        "HP 14s-dq",                 "HP 15s-eq",
        "HP 255 G9",                 "Lenovo IdeaPad 1 14",
        "Lenovo IdeaPad 1 15",       "Lenovo IdeaPad Slim 1",
        "Samsung Galaxy Book Go",    "Toshiba Dynabook Satellite Pro",
        "Dell Inspiron 14 3420",     "Dell Inspiron 15 3520",
    ]

    MODELOS_INTERMEDIA: list[str] = [
        "Acer Swift 3",              "Acer Aspire 7",
        "ASUS VivoBook 15",          "ASUS VivoBook 16X",
        "ASUS ZenBook 14",           "Dell Inspiron 15 5520",
        "Dell Inspiron 16 5620",     "HP Pavilion 15",
        "HP Envy x360 15",           "Lenovo IdeaPad 5",
        "Lenovo IdeaPad Flex 5",     "Lenovo ThinkBook 15",
        "MSI Modern 15",             "Samsung Galaxy Book2",
        "Huawei MateBook D15",       "Xiaomi Mi Notebook Pro 15",
    ]

    MODELOS_GAMER: list[str] = [
        "Acer Nitro 5",              "Acer Predator Helios 16",
        "Acer Predator Triton 500 SE", "ASUS ROG Strix G16",
        "ASUS ROG Zephyrus G14",     "ASUS ROG Zephyrus G16",
        "ASUS TUF Gaming A15",       "ASUS TUF Gaming F17",
        "Dell Alienware m16",        "Dell Alienware x16",
        "HP OMEN 16",                "HP Victus 16",
        "Lenovo Legion 5 Pro",       "Lenovo Legion 7",
        "Lenovo Legion Pro 7i",      "MSI Raider GE78 HX",
        "MSI Stealth 16 Studio",     "MSI Titan GT77 HX",
        "Razer Blade 15",            "Razer Blade 16",
    ]


# ─────────────────────────────────────────────────────────────────────────────
#  CATÁLOGO PC ESCRITORIO
# ─────────────────────────────────────────────────────────────────────────────

class CatalogoPCEscritorio:
    """
    Componentes para PCs de escritorio.
    CPUs con socket físico (AM4, AM5, LGA1700, etc.).
    GPUs PCIe x16 (reemplazables).
    RAM DIMM (4 slots en ATX, 2 en ITX).
    """

    # ── PLACAS BASE ──────────────────────────────────────────────────────────

    PLACAS_BASICA: list[DatosPlacaBase] = [
        DatosPlacaBase(
            modelo="Intel H610 Micro-ATX",
            socket_compatible=SocketCPU.LGA1700,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=3200,
            n_slots_ram=2,
            capacidad_maxima_ram_gb=32,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_NVME), DatosSSDSlot(InterfazSSD.SATA)),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=1,
        ),
        DatosPlacaBase(
            modelo="Intel B660 ATX",
            socket_compatible=SocketCPU.LGA1700,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=3600,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=64,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_SATA),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=1,
        ),
        DatosPlacaBase(
            modelo="AMD A520 Micro-ATX",
            socket_compatible=SocketCPU.AM4,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=4600,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=128,
            slots_ssd=(DatosSSDSlot(InterfazSSD.M2_NVME), DatosSSDSlot(InterfazSSD.SATA)),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=1,
        ),
        DatosPlacaBase(
            modelo="AMD B450 ATX",
            socket_compatible=SocketCPU.AM4,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=3600,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=64,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=1,
        ),
    ]

    PLACAS_INTERMEDIA: list[DatosPlacaBase] = [
        DatosPlacaBase(
            modelo="Intel B760 ATX DDR5",
            socket_compatible=SocketCPU.LGA1700,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=6000,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=128,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=1,
        ),
        DatosPlacaBase(
            modelo="AMD B550 ATX",
            socket_compatible=SocketCPU.AM4,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=5100,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=128,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=1,
        ),
        DatosPlacaBase(
            modelo="AMD B650 ATX DDR5",
            socket_compatible=SocketCPU.AM5,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=6000,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=128,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=1,
        ),
    ]

    PLACAS_GAMER: list[DatosPlacaBase] = [
        DatosPlacaBase(
            modelo="Intel Z790 ATX DDR5",
            socket_compatible=SocketCPU.LGA1700,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=7600,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=192,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=2,
        ),
        DatosPlacaBase(
            modelo="AMD X670E ATX DDR5",
            socket_compatible=SocketCPU.AM5,
            generacion_ram=GeneracionRAM.DDR5,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=6600,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=192,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=2,
        ),
        DatosPlacaBase(
            modelo="AMD X570 ATX DDR4",
            socket_compatible=SocketCPU.AM4,
            generacion_ram=GeneracionRAM.DDR4,
            formato_ram=FormatoRAM.DIMM,
            velocidad_maxima_ram_mhz=5100,
            n_slots_ram=4,
            capacidad_maxima_ram_gb=128,
            slots_ssd=(
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.M2_NVME),
                DatosSSDSlot(InterfazSSD.SATA),
                DatosSSDSlot(InterfazSSD.SATA),
            ),
            interfaz_gpu=InterfazGPU.PCIE,
            cantidad_slots_gpu=2,
        ),
    ]

    # ── CPUs Desktop ─────────────────────────────────────────────────────────

    CPUS_BASICA: list[DatosCPU] = [
        DatosCPU("Intel Celeron G5925",         2,  3.6, SocketCPU.LGA1200, 58),
        DatosCPU("Intel Celeron G6900",         2,  3.4, SocketCPU.LGA1700, 46),
        DatosCPU("Intel Pentium Gold G6400",    2,  4.0, SocketCPU.LGA1200, 58),
        DatosCPU("Intel Pentium Gold G7400",    2,  3.7, SocketCPU.LGA1700, 46),
        DatosCPU("Intel Core i3-10100",         4,  4.3, SocketCPU.LGA1200, 65),
        DatosCPU("Intel Core i3-12100",         4,  4.3, SocketCPU.LGA1700, 60),
        DatosCPU("Intel Core i3-12100F",        4,  4.3, SocketCPU.LGA1700, 58),
        DatosCPU("Intel Core i3-13100",         4,  4.5, SocketCPU.LGA1700, 60),
        DatosCPU("Intel Core i3-13100F",        4,  4.5, SocketCPU.LGA1700, 58),
        DatosCPU("AMD Athlon 3000G",            2,  3.5, SocketCPU.AM4,     35),
        DatosCPU("AMD Ryzen 3 3200G",           4,  4.0, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 3 4300G",           4,  4.0, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 3 5300G",           4,  4.2, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 5 4500",            6,  4.1, SocketCPU.AM4,     65),
    ]

    CPUS_INTERMEDIA: list[DatosCPU] = [
        DatosCPU("Intel Core i5-10400",         6,  4.3, SocketCPU.LGA1200, 65),
        DatosCPU("Intel Core i5-11400",         6,  4.4, SocketCPU.LGA1200, 65),
        DatosCPU("Intel Core i5-12400",         6,  4.4, SocketCPU.LGA1700, 65),
        DatosCPU("Intel Core i5-12400F",        6,  4.4, SocketCPU.LGA1700, 65),
        DatosCPU("Intel Core i5-13400",        10,  4.6, SocketCPU.LGA1700, 65),
        DatosCPU("Intel Core i5-13400F",       10,  4.6, SocketCPU.LGA1700, 65),
        DatosCPU("Intel Core i5-13500",        14,  4.8, SocketCPU.LGA1700, 65),
        DatosCPU("Intel Core i7-12700",        12,  4.9, SocketCPU.LGA1700, 65),
        DatosCPU("Intel Core i7-12700F",       12,  4.9, SocketCPU.LGA1700, 65),
        DatosCPU("Intel Core i7-13700",        16,  5.2, SocketCPU.LGA1700, 65),
        DatosCPU("AMD Ryzen 5 5600",            6,  4.4, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 5 5600G",           6,  4.4, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 5 5600X",           6,  4.6, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 5 7600",            6,  5.1, SocketCPU.AM5,     65),
        DatosCPU("AMD Ryzen 5 7600X",           6,  5.3, SocketCPU.AM5,    105),
        DatosCPU("AMD Ryzen 7 5700G",           8,  4.6, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 7 5700X",           8,  4.6, SocketCPU.AM4,     65),
        DatosCPU("AMD Ryzen 7 5800X",           8,  4.7, SocketCPU.AM4,    105),
        DatosCPU("AMD Ryzen 7 7700",            8,  5.3, SocketCPU.AM5,     65),
        DatosCPU("AMD Ryzen 7 7700X",           8,  5.4, SocketCPU.AM5,    105),
    ]

    CPUS_GAMER: list[DatosCPU] = [
        DatosCPU("Intel Core i7-12700K",       12,  5.0, SocketCPU.LGA1700, 125),
        DatosCPU("Intel Core i7-12700KF",      12,  5.0, SocketCPU.LGA1700, 125),
        DatosCPU("Intel Core i7-13700K",       16,  5.4, SocketCPU.LGA1700, 125),
        DatosCPU("Intel Core i7-13700KF",      16,  5.4, SocketCPU.LGA1700, 125),
        DatosCPU("Intel Core i7-14700K",       20,  5.6, SocketCPU.LGA1700, 125),
        DatosCPU("Intel Core i9-12900K",       16,  5.2, SocketCPU.LGA1700, 125),
        DatosCPU("Intel Core i9-13900K",       24,  5.8, SocketCPU.LGA1700, 125),
        DatosCPU("Intel Core i9-14900K",       24,  6.0, SocketCPU.LGA1700, 125),
        DatosCPU("AMD Ryzen 7 7800X3D",         8,  5.0, SocketCPU.AM5,    120),
        DatosCPU("AMD Ryzen 9 5900X",          12,  4.8, SocketCPU.AM4,    105),
        DatosCPU("AMD Ryzen 9 5950X",          16,  4.9, SocketCPU.AM4,    105),
        DatosCPU("AMD Ryzen 9 7900X",          12,  5.6, SocketCPU.AM5,    170),
        DatosCPU("AMD Ryzen 9 7900X3D",        12,  5.6, SocketCPU.AM5,    120),
        DatosCPU("AMD Ryzen 9 7950X",          16,  5.7, SocketCPU.AM5,    170),
        DatosCPU("AMD Ryzen 9 7950X3D",        16,  5.7, SocketCPU.AM5,    120),
        DatosCPU("AMD Ryzen 9 9950X",          16,  5.7, SocketCPU.AM5,    170),
    ]

    # ── GPUs Desktop ─────────────────────────────────────────────────────────

    GPUS_BASICA: list[DatosGPU] = [
        DatosGPU("NVIDIA GeForce GT 1030",       2, TipoMemoriaGPU.DDR4,  TipoGPU.DEDICADA, InterfazGPU.PCIE,  30),
        DatosGPU("NVIDIA GeForce GTX 1050 Ti",   4, TipoMemoriaGPU.GDDR5, TipoGPU.DEDICADA, InterfazGPU.PCIE,  75),
        DatosGPU("NVIDIA GeForce GTX 1650",      4, TipoMemoriaGPU.GDDR5, TipoGPU.DEDICADA, InterfazGPU.PCIE,  75),
        DatosGPU("NVIDIA GeForce GTX 1650 Super",4, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE, 100),
        DatosGPU("NVIDIA GeForce GTX 1660",      6, TipoMemoriaGPU.GDDR5, TipoGPU.DEDICADA, InterfazGPU.PCIE, 120),
        DatosGPU("NVIDIA GeForce RTX 3050",      8, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE, 130),
        DatosGPU("AMD Radeon RX 6400",           4, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE,  53),
        DatosGPU("AMD Radeon RX 6500 XT",        4, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE,  55),
        DatosGPU("AMD Radeon RX 6600",           8, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE, 132),
        DatosGPU("Intel Arc A380",               6, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE,  75),
        DatosGPU("Intel Arc A580",               8, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE, 185),
    ]

    GPUS_INTERMEDIA: list[DatosGPU] = [
        DatosGPU("NVIDIA GeForce GTX 1660 Ti",   6, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 120),
        DatosGPU("NVIDIA RTX 2060",              6, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 160),
        DatosGPU("NVIDIA RTX 2070",              8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 175),
        DatosGPU("NVIDIA RTX 3060",             12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 170),
        DatosGPU("NVIDIA RTX 3060 Ti",           8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 200),
        DatosGPU("NVIDIA RTX 3070",              8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 220),
        DatosGPU("NVIDIA RTX 4060",              8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 115),
        DatosGPU("NVIDIA RTX 4060 Ti",          16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 165),
        DatosGPU("NVIDIA RTX 4070",             12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 200),
        DatosGPU("AMD Radeon RX 6700 XT",       12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 230),
        DatosGPU("AMD Radeon RX 6750 XT",       12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 250),
        DatosGPU("AMD Radeon RX 7600",           8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 165),
        DatosGPU("AMD Radeon RX 7700 XT",       12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 245),
        DatosGPU("AMD Radeon RX 7800 XT",       16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 263),
        DatosGPU("Intel Arc A750",               8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 225),
        DatosGPU("Intel Arc A770",              16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 225),
    ]

    GPUS_GAMER: list[DatosGPU] = [
        DatosGPU("NVIDIA RTX 3080",             10, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 320),
        DatosGPU("NVIDIA RTX 3080 Ti",          12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 350),
        DatosGPU("NVIDIA RTX 3090",             24, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 350),
        DatosGPU("NVIDIA RTX 4070 Ti",          12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 285),
        DatosGPU("NVIDIA RTX 4070 Ti Super",    16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 285),
        DatosGPU("NVIDIA RTX 4080",             16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 320),
        DatosGPU("NVIDIA RTX 4080 Super",       16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 320),
        DatosGPU("NVIDIA RTX 4090",             24, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 450),
        DatosGPU("AMD Radeon RX 6800 XT",       16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 300),
        DatosGPU("AMD Radeon RX 6900 XT",       16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 300),
        DatosGPU("AMD Radeon RX 7900 GRE",      16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 260),
        DatosGPU("AMD Radeon RX 7900 XT",       20, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 315),
        DatosGPU("AMD Radeon RX 7900 XTX",      24, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIE, 355),
    ]

    # ── Módulos RAM Desktop ──────────────────────────────────────────────────

    MODULOS_RAM_BASICA: list[DatosRAMModulo] = [
        DatosRAMModulo("Kingston ValueRAM DDR4",  4, 2666, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Kingston ValueRAM DDR4",  8, 2666, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Kingston ValueRAM DDR4",  8, 3200, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Crucial Basics DDR4",     8, 2666, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Crucial Basics DDR4",    16, 3200, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Corsair Vengeance DDR4",  8, 3200, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Corsair Vengeance DDR4", 16, 3200, GeneracionRAM.DDR4, FormatoRAM.DIMM),
    ]

    MODULOS_RAM_INTERMEDIA_DDR4: list[DatosRAMModulo] = [
        DatosRAMModulo("G.Skill Ripjaws V DDR4", 16, 3600, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("G.Skill Ripjaws V DDR4", 32, 3600, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Corsair Vengeance DDR4", 16, 3200, GeneracionRAM.DDR4, FormatoRAM.DIMM),
        DatosRAMModulo("Kingston Fury Beast DDR4",16, 3600, GeneracionRAM.DDR4, FormatoRAM.DIMM),
    ]

    MODULOS_RAM_INTERMEDIA_DDR5: list[DatosRAMModulo] = [
        DatosRAMModulo("G.Skill Trident Z5 DDR5", 16, 5600, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("G.Skill Trident Z5 DDR5", 32, 5600, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("Corsair Vengeance DDR5",   16, 5200, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("Corsair Vengeance DDR5",   32, 5200, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("Kingston Fury Beast DDR5", 16, 5600, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("Kingston Fury Beast DDR5", 32, 5600, GeneracionRAM.DDR5, FormatoRAM.DIMM),
    ]

    MODULOS_RAM_GAMER: list[DatosRAMModulo] = [
        DatosRAMModulo("G.Skill Trident Z5 DDR5", 32, 6000, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("G.Skill Trident Z5 DDR5", 32, 6400, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("Corsair Dominator DDR5",   32, 6000, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("Kingston Fury Renegade DDR5",32,6400, GeneracionRAM.DDR5, FormatoRAM.DIMM),
        DatosRAMModulo("TeamGroup T-Force DDR5",   32, 7200, GeneracionRAM.DDR5, FormatoRAM.DIMM),
    ]

    # ── SSDs Desktop ─────────────────────────────────────────────────────────

    SSDS_BASICA: list[DatosSSD] = [
        DatosSSD("Kingston A400",          240, InterfazSSD.SATA,     500,  320),
        DatosSSD("WD Blue SATA",           500, InterfazSSD.SATA,     560,  530),
        DatosSSD("Samsung 870 EVO",        500, InterfazSSD.SATA,     560,  530),
        DatosSSD("Crucial BX500",          480, InterfazSSD.SATA,     540,  500),
        DatosSSD("Kingston NV2 NVMe",      500, InterfazSSD.M2_NVME, 3500, 2100),
        DatosSSD("WD Blue SN570",          500, InterfazSSD.M2_NVME, 3500, 3000),
    ]

    SSDS_INTERMEDIA: list[DatosSSD] = [
        DatosSSD("Samsung 980 NVMe",       500, InterfazSSD.M2_NVME, 3500, 3000),
        DatosSSD("Samsung 980 NVMe",      1000, InterfazSSD.M2_NVME, 3500, 3000),
        DatosSSD("Samsung 980 Pro",       1000, InterfazSSD.M2_NVME, 7000, 5000),
        DatosSSD("WD Black SN770",        1000, InterfazSSD.M2_NVME, 5150, 4900),
        DatosSSD("WD Black SN770",        2000, InterfazSSD.M2_NVME, 5150, 4900),
        DatosSSD("Seagate Barracuda 510", 1000, InterfazSSD.M2_NVME, 3400, 3000),
        DatosSSD("Crucial P5 Plus",       1000, InterfazSSD.M2_NVME, 6600, 5000),
    ]

    SSDS_GAMER: list[DatosSSD] = [
        DatosSSD("Samsung 990 Pro",        1000, InterfazSSD.M2_NVME, 7450, 6900),
        DatosSSD("Samsung 990 Pro",        2000, InterfazSSD.M2_NVME, 7450, 6900),
        DatosSSD("Samsung 990 Pro",        4000, InterfazSSD.M2_NVME, 7450, 6900),
        DatosSSD("WD Black SN850X",        1000, InterfazSSD.M2_NVME, 7300, 6600),
        DatosSSD("WD Black SN850X",        2000, InterfazSSD.M2_NVME, 7300, 6600),
        DatosSSD("Seagate FireCuda 530",   1000, InterfazSSD.M2_NVME, 7300, 6900),
        DatosSSD("Seagate FireCuda 530",   2000, InterfazSSD.M2_NVME, 7300, 6900),
        DatosSSD("Corsair MP600 Pro",      2000, InterfazSSD.M2_NVME, 7100, 6800),
        DatosSSD("Kingston Fury Renegade", 4000, InterfazSSD.M2_NVME, 7300, 7000),
    ]

    # ── Fuentes de poder ─────────────────────────────────────────────────────

    FUENTES_BASICA:      tuple[int, ...] = (350, 400, 450, 500)
    FUENTES_INTERMEDIA:  tuple[int, ...] = (550, 600, 650, 750)
    FUENTES_GAMER:       tuple[int, ...] = (850, 1000, 1200, 1600)

    # ── Modelos de equipo ─────────────────────────────────────────────────────

    MODELOS_BASICA: list[str] = [
        "Acer Aspire TC-885",        "ASUS VivoPC M32",
        "Dell Inspiron 3020",        "Dell OptiPlex 3000",
        "HP Slimline 290",           "HP 280 G4",
        "Lenovo IdeaCentre 3",       "MSI Pro DP21",
        "HP ProDesk 400 G7",         "Dell Vostro 3910",
    ]

    MODELOS_INTERMEDIA: list[str] = [
        "Acer Aspire TC-1760",       "ASUS ExpertCenter D5",
        "ASUS ProArt Station PD5",   "Dell Inspiron 3910",
        "Dell OptiPlex 5000",        "HP Pavilion TP01",
        "HP EliteDesk 800 G6",       "Lenovo IdeaCentre 5",
        "Lenovo ThinkCentre M70s",   "MSI Pro DP130",
        "Zotac ZBOX Magnus One",     "Acer Veriton M4690G",
    ]

    MODELOS_GAMER: list[str] = [
        "Acer Predator Orion 3000",  "Acer Predator Orion 5000",
        "Acer Predator Orion 7000",  "Alienware Aurora R15",
        "Alienware Aurora R16",      "ASUS ROG Strix GT35",
        "ASUS ROG Strix GT15",       "Corsair One i300",
        "HP OMEN 45L",               "HP OMEN 25L",
        "Lenovo Legion Tower 5i",    "Lenovo Legion Tower 7i",
        "MSI Aegis Ti5",             "MSI MEG Infinite X2",
        "MSI Trident X2",            "Thermaltake Tower 900",
    ]


# Alias tipado para re-exportar DatosRAMModulo desde este módulo
__all__ = [
    "DatosCPU", "DatosGPU", "DatosRAMModulo", "DatosSSD",
    "DatosBateria", "DatosPantalla", "DatosPlacaBase", "DatosSSDSlot", "DatosRAMSlot",
    "CatalogoLaptop", "CatalogoPCEscritorio",
]