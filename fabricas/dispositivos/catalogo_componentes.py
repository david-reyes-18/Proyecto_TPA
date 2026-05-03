from dataclasses import dataclass
from componentes.gpu.tipo_gpu import TipoGPU
from componentes.gpu.tipo_memoria_gpu import TipoMemoriaGPU
from componentes.gpu.tipo_interfaz import InterfazGPU
from componentes.ssd.interfaz_ssd import InterfazSSD
from componentes.bateria.forma_bateria import FormaBateria


#   Data clases que representan los datos de los componentes de los dispositivos, 
#   los cuales son inmutables

@dataclass(frozen=True)
class DatosCPU:
    modelo: str
    nucleos: int
    frecuencia_ghz: float
    es_reemplazable: bool = True


@dataclass(frozen=True)
class DatosGPU:
    modelo: str
    memoria_gb: int
    tipo_memoria: TipoMemoriaGPU
    tipo_gpu: TipoGPU
    interfaz: InterfazGPU


@dataclass(frozen=True)
class DatosRAM:
    tipo: str
    velocidad_mhz: int
    capacidad_slot_gb: int
    max_ram_gb: int
    opciones_gb: tuple[int, ...]
    n_slots: int = 2


@dataclass(frozen=True)
class DatosSSD:
    interfaz: InterfazSSD
    velocidad_lectura_mbps: int
    opciones_gb: tuple[int, ...]


@dataclass(frozen=True)
class DatosBateria:
    voltaje: float
    forma: FormaBateria
    opciones_mah: tuple[int, ...]


@dataclass(frozen=True)
class DatosPantalla:
    opciones_pulgadas: tuple[int, ...]
    opciones_resoluciones: tuple[str, ...]


#                           CATALOGO DE LAS LAPTOPS QUE SE CREARAN
#   Aqui cada laptop que se cree debera tener un componente del catalogo dependiendo su categoria

class CatalogoLaptop:

    # CPU
    
    CPUS_BASICA: list[DatosCPU] = [
        # Intel — Celeron / Pentium / Core i3 (soldados, bajo consumo)
        DatosCPU("Intel Celeron N4020",          2,  2.8, es_reemplazable=False),
        DatosCPU("Intel Celeron N4500",          2,  2.8, es_reemplazable=False),
        DatosCPU("Intel Celeron N5100",          4,  2.8, es_reemplazable=False),
        DatosCPU("Intel Pentium Silver N5030",   4,  3.1, es_reemplazable=False),
        DatosCPU("Intel Pentium Silver N6000",   4,  3.3, es_reemplazable=False),
        DatosCPU("Intel Core i3-1005G1",         2,  3.4, es_reemplazable=False),
        DatosCPU("Intel Core i3-1115G4",         2,  4.1, es_reemplazable=False),
        DatosCPU("Intel Core i3-1215U",          6,  4.4, es_reemplazable=False),
        # AMD — Athlon / Ryzen 3
        DatosCPU("AMD Athlon Silver 3050U",      2,  3.2, es_reemplazable=False),
        DatosCPU("AMD Athlon Gold 3150U",        2,  3.3, es_reemplazable=False),
        DatosCPU("AMD Ryzen 3 3250U",            2,  3.5, es_reemplazable=False),
        DatosCPU("AMD Ryzen 3 5300U",            4,  3.8, es_reemplazable=False),
        DatosCPU("AMD Ryzen 3 7320U",            4,  4.1, es_reemplazable=False),
    ]

    CPUS_INTERMEDIA: list[DatosCPU] = [
        # Intel — Core i5 / i7 serie U y P
        DatosCPU("Intel Core i5-10210U",         4,  4.2, es_reemplazable=False),
        DatosCPU("Intel Core i5-1135G7",         4,  4.2, es_reemplazable=False),
        DatosCPU("Intel Core i5-1235U",         10,  4.4, es_reemplazable=False),
        DatosCPU("Intel Core i5-1240P",         12,  4.4, es_reemplazable=False),
        DatosCPU("Intel Core i5-1335U",         10,  4.6, es_reemplazable=False),
        DatosCPU("Intel Core i5-1340P",         12,  4.6, es_reemplazable=False),
        DatosCPU("Intel Core i7-1165G7",         4,  4.7, es_reemplazable=False),
        DatosCPU("Intel Core i7-1255U",         10,  4.7, es_reemplazable=False),
        DatosCPU("Intel Core i7-1260P",         12,  4.7, es_reemplazable=False),
        DatosCPU("Intel Core i7-1360P",         13,  5.0, es_reemplazable=False),
        # AMD — Ryzen 5 / 7 serie U
        DatosCPU("AMD Ryzen 5 4500U",            6,  4.0, es_reemplazable=False),
        DatosCPU("AMD Ryzen 5 5500U",            6,  4.0, es_reemplazable=False),
        DatosCPU("AMD Ryzen 5 5600U",            6,  4.2, es_reemplazable=False),
        DatosCPU("AMD Ryzen 5 7530U",            6,  4.5, es_reemplazable=False),
        DatosCPU("AMD Ryzen 5 7540U",            6,  4.9, es_reemplazable=False),
        DatosCPU("AMD Ryzen 7 5700U",            8,  4.3, es_reemplazable=False),
        DatosCPU("AMD Ryzen 7 7730U",            8,  4.5, es_reemplazable=False),
        DatosCPU("AMD Ryzen 7 7745U",            8,  5.1, es_reemplazable=False),
    ]

    CPUS_GAMER: list[DatosCPU] = [
        # Intel — Core i7 / i9 serie H y HX (alto voltaje, gaming)
        DatosCPU("Intel Core i7-12700H",        14,  4.7, es_reemplazable=False),
        DatosCPU("Intel Core i7-13700H",        14,  5.0, es_reemplazable=False),
        DatosCPU("Intel Core i7-14700HX",       20,  5.5, es_reemplazable=False),
        DatosCPU("Intel Core i9-12900H",        20,  5.0, es_reemplazable=False),
        DatosCPU("Intel Core i9-13900H",        20,  5.4, es_reemplazable=False),
        DatosCPU("Intel Core i9-13900HX",       24,  5.6, es_reemplazable=False),
        DatosCPU("Intel Core i9-14900HX",       24,  5.8, es_reemplazable=False),
        # AMD — Ryzen 7 / 9 serie HX (alto voltaje, gaming)
        DatosCPU("AMD Ryzen 7 6800H",            8,  4.7, es_reemplazable=False),
        DatosCPU("AMD Ryzen 7 7745HX",           8,  5.1, es_reemplazable=False),
        DatosCPU("AMD Ryzen 7 8845HS",           8,  5.1, es_reemplazable=False),
        DatosCPU("AMD Ryzen 9 6900HX",           8,  4.9, es_reemplazable=False),
        DatosCPU("AMD Ryzen 9 7940HX",          16,  5.4, es_reemplazable=False),
        DatosCPU("AMD Ryzen 9 7945HX",          16,  5.4, es_reemplazable=False),
        DatosCPU("AMD Ryzen 9 8945HS",           8,  5.2, es_reemplazable=False),
    ]

    #GPU
    
    GPUS_BASICA: list[DatosGPU] = [
        # Gráficos integrados — única opción realista en laptops de entrada
        DatosGPU("Intel UHD Graphics 600",      2, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
        DatosGPU("Intel UHD Graphics 620",      2, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
        DatosGPU("Intel UHD Graphics 730",      2, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
        DatosGPU("Intel Iris Xe Graphics",      4, TipoMemoriaGPU.LPDDR5,  TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
        DatosGPU("AMD Radeon Graphics (Vega 3)", 2, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
        DatosGPU("AMD Radeon Graphics (Vega 6)", 2, TipoMemoriaGPU.LPDDR4X, TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
        DatosGPU("AMD Radeon 610M",             2, TipoMemoriaGPU.LPDDR5,  TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
        DatosGPU("AMD Radeon 740M",             4, TipoMemoriaGPU.LPDDR5,  TipoGPU.INTEGRADA, InterfazGPU.INTEGRADA),
    ]

    GPUS_INTERMEDIA: list[DatosGPU] = [
        # NVIDIA — MX series y RTX 30 entry
        DatosGPU("NVIDIA GeForce MX450",        2, TipoMemoriaGPU.GDDR5,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA GeForce MX550",        2, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 2050",             4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 3050 Laptop",      4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 3050 Ti Laptop",   4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 4050 Laptop",      6, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        # AMD — RX 6000 mobile mid
        DatosGPU("AMD Radeon RX 6500M",         4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("AMD Radeon RX 6600M",         8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("AMD Radeon RX 6650M",         8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("AMD Radeon RX 7600M XT",      8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        # Intel Arc mobile
        DatosGPU("Intel Arc A370M",             4, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("Intel Arc A530M",             8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
    ]

    GPUS_GAMER: list[DatosGPU] = [
        # NVIDIA RTX 30 alta gama laptop
        DatosGPU("NVIDIA RTX 3070 Ti Laptop",   8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 3080 Laptop",     16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 3080 Ti Laptop",  16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        # NVIDIA RTX 40 laptop
        DatosGPU("NVIDIA RTX 4060 Laptop",      8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 4070 Laptop",      8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 4070 Ti Laptop",  12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 4080 Laptop",     12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("NVIDIA RTX 4090 Laptop",     16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.MXM),
        # AMD RX 6000 / 7000 alta gama laptop
        DatosGPU("AMD Radeon RX 6700M",        10, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("AMD Radeon RX 6800M",        12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("AMD Radeon RX 6850M XT",     12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
        DatosGPU("AMD Radeon RX 7900M",        16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.MXM),
    ]

    # ─────────────────────────────────────────────
    #  RAM
    # ─────────────────────────────────────────────

    RAM_BASICA      = DatosRAM("DDR4", 2666, capacidad_slot_gb=8,   max_ram_gb=16,  opciones_gb=(4, 8, 16),         n_slots=2)
    RAM_INTERMEDIA  = DatosRAM("DDR5", 4800, capacidad_slot_gb=16,  max_ram_gb=32,  opciones_gb=(8, 16, 32),        n_slots=2)
    RAM_GAMER       = DatosRAM("DDR5", 5600, capacidad_slot_gb=64,  max_ram_gb=128, opciones_gb=(16, 32, 64, 128),  n_slots=2)

    # ─────────────────────────────────────────────
    #  SSD
    # ─────────────────────────────────────────────

    SSD_BASICA      = DatosSSD(InterfazSSD.SATA,    550,   opciones_gb=(128, 256, 512))
    SSD_INTERMEDIA  = DatosSSD(InterfazSSD.M2_NVME, 5000,  opciones_gb=(256, 512, 1024))
    SSD_GAMER       = DatosSSD(InterfazSSD.M2_NVME, 10000, opciones_gb=(512, 1024, 2048))

    # ─────────────────────────────────────────────
    #  Batería
    # ─────────────────────────────────────────────

    BATERIA_BASICA      = DatosBateria(11.4, FormaBateria.RECTANGULAR, (3000, 3500, 4000, 4500))
    BATERIA_INTERMEDIA  = DatosBateria(15.4, FormaBateria.RECTANGULAR, (4500, 5000, 5500, 6000))
    BATERIA_GAMER       = DatosBateria(20.0, FormaBateria.RECTANGULAR, (5500, 6000, 7500, 9000, 9900))

    # ─────────────────────────────────────────────
    #  Pantalla
    # ─────────────────────────────────────────────

    PANTALLA_BASICA     = DatosPantalla(
        opciones_pulgadas    = (14, 15),
        opciones_resoluciones= ("1366x768", "1600x900", "1920x1080"),
    )
    PANTALLA_INTERMEDIA = DatosPantalla(
        opciones_pulgadas    = (14, 15, 16),
        opciones_resoluciones= ("1920x1080", "1920x1200", "2560x1440", "2560x1600"),
    )
    PANTALLA_GAMER      = DatosPantalla(
        opciones_pulgadas    = (15, 16, 17, 18),
        opciones_resoluciones= ("1920x1080", "2560x1440", "2560x1600", "3840x2160"),
    )

    # ─────────────────────────────────────────────
    #  Modelos de equipo
    # ─────────────────────────────────────────────

    MODELOS_BASICA: list[str] = [
        "Acer Aspire 3 A315",
        "Acer Aspire 5 A515",
        "ASUS VivoBook Go 14",
        "ASUS VivoBook Go 15",
        "HP 14s-dq",
        "HP 15s-eq",
        "HP 255 G9",
        "Lenovo IdeaPad 1 14",
        "Lenovo IdeaPad 1 15",
        "Lenovo IdeaPad Slim 1",
        "Samsung Galaxy Book Go",
        "Toshiba Dynabook Satellite Pro",
    ]

    MODELOS_INTERMEDIA: list[str] = [
        "Acer Swift 3",
        "Acer Aspire 7",
        "ASUS VivoBook 15",
        "ASUS VivoBook 16X",
        "ASUS ZenBook 14",
        "Dell Inspiron 15 3520",
        "Dell Inspiron 15 5520",
        "HP Pavilion 15",
        "HP Envy x360 15",
        "Lenovo IdeaPad 5",
        "Lenovo IdeaPad Flex 5",
        "Lenovo ThinkBook 15",
        "MSI Modern 15",
        "Samsung Galaxy Book2",
    ]

    MODELOS_GAMER: list[str] = [
        "Acer Nitro 5",
        "Acer Predator Helios 16",
        "Acer Predator Triton 500 SE",
        "ASUS ROG Strix G16",
        "ASUS ROG Zephyrus G14",
        "ASUS ROG Zephyrus G16",
        "ASUS TUF Gaming A15",
        "ASUS TUF Gaming F17",
        "Dell Alienware m16",
        "Dell Alienware x16",
        "HP OMEN 16",
        "HP Victus 16",
        "Lenovo Legion 5 Pro",
        "Lenovo Legion 7",
        "Lenovo Legion Pro 7i",
        "MSI Raider GE78 HX",
        "MSI Stealth 16 Studio",
        "MSI Titan GT77 HX",
        "Razer Blade 15",
        "Razer Blade 16",
    ]


# =============================================================================
#  CATÁLOGO DE PCs DE ESCRITORIO
# =============================================================================

class CatalogoPCEscritorio:
    """
    Todos los componentes disponibles para PCs de escritorio, organizados
    por categoría: Básico · Intermedio · Gamer/Workstation
    """

    # ─────────────────────────────────────────────
    #  CPUs
    # ─────────────────────────────────────────────

    CPUS_BASICA: list[DatosCPU] = [
        # Intel — Pentium / Celeron / Core i3 de escritorio
        DatosCPU("Intel Celeron G5925",          2,  3.6),
        DatosCPU("Intel Celeron G6900",          2,  3.4),
        DatosCPU("Intel Pentium Gold G6400",     2,  4.0),
        DatosCPU("Intel Pentium Gold G6600",     2,  4.2),
        DatosCPU("Intel Pentium Gold G7400",     2,  3.7),
        DatosCPU("Intel Core i3-10100",          4,  4.3),
        DatosCPU("Intel Core i3-12100",          4,  4.3),
        DatosCPU("Intel Core i3-12100F",         4,  4.3),
        DatosCPU("Intel Core i3-13100",          4,  4.5),
        DatosCPU("Intel Core i3-13100F",         4,  4.5),
        # AMD — Athlon / Ryzen 3 de escritorio
        DatosCPU("AMD Athlon 3000G",             2,  3.5),
        DatosCPU("AMD Ryzen 3 3200G",            4,  4.0),
        DatosCPU("AMD Ryzen 3 4300G",            4,  4.0),
        DatosCPU("AMD Ryzen 3 5300G",            4,  4.2),
        DatosCPU("AMD Ryzen 3 5300GE",           4,  4.0),
        DatosCPU("AMD Ryzen 5 4500",             6,  4.1),
    ]

    CPUS_INTERMEDIA: list[DatosCPU] = [
        # Intel — Core i5 / i7 no-K
        DatosCPU("Intel Core i5-10400",          6,  4.3),
        DatosCPU("Intel Core i5-10600",          6,  4.8),
        DatosCPU("Intel Core i5-11400",          6,  4.4),
        DatosCPU("Intel Core i5-11600",          6,  4.8),
        DatosCPU("Intel Core i5-12400",          6,  4.4),
        DatosCPU("Intel Core i5-12400F",         6,  4.4),
        DatosCPU("Intel Core i5-12600",          6,  4.8),
        DatosCPU("Intel Core i5-13400",         10,  4.6),
        DatosCPU("Intel Core i5-13400F",        10,  4.6),
        DatosCPU("Intel Core i5-13500",         14,  4.8),
        DatosCPU("Intel Core i7-10700",          8,  4.8),
        DatosCPU("Intel Core i7-11700",          8,  4.9),
        DatosCPU("Intel Core i7-12700",         12,  4.9),
        DatosCPU("Intel Core i7-12700F",        12,  4.9),
        DatosCPU("Intel Core i7-13700",         16,  5.2),
        DatosCPU("Intel Core i7-13700F",        16,  5.2),
        # AMD — Ryzen 5 / 7 no-X
        DatosCPU("AMD Ryzen 5 5600",             6,  4.4),
        DatosCPU("AMD Ryzen 5 5600G",            6,  4.4),
        DatosCPU("AMD Ryzen 5 5600X",            6,  4.6),
        DatosCPU("AMD Ryzen 5 7600",             6,  5.1),
        DatosCPU("AMD Ryzen 5 7600X",            6,  5.3),
        DatosCPU("AMD Ryzen 7 5700G",            8,  4.6),
        DatosCPU("AMD Ryzen 7 5700X",            8,  4.6),
        DatosCPU("AMD Ryzen 7 5800X",            8,  4.7),
        DatosCPU("AMD Ryzen 7 7700",             8,  5.3),
        DatosCPU("AMD Ryzen 7 7700X",            8,  5.4),
    ]

    CPUS_GAMER: list[DatosCPU] = [
        # Intel — Core i7-K / i9-K desbloqueados
        DatosCPU("Intel Core i7-12700K",        12,  5.0),
        DatosCPU("Intel Core i7-12700KF",       12,  5.0),
        DatosCPU("Intel Core i7-13700K",        16,  5.4),
        DatosCPU("Intel Core i7-13700KF",       16,  5.4),
        DatosCPU("Intel Core i7-14700K",        20,  5.6),
        DatosCPU("Intel Core i7-14700KF",       20,  5.6),
        DatosCPU("Intel Core i9-12900K",        16,  5.2),
        DatosCPU("Intel Core i9-12900KF",       16,  5.2),
        DatosCPU("Intel Core i9-13900K",        24,  5.8),
        DatosCPU("Intel Core i9-13900KF",       24,  5.8),
        DatosCPU("Intel Core i9-14900K",        24,  6.0),
        DatosCPU("Intel Core i9-14900KF",       24,  6.0),
        # AMD — Ryzen 7X / 9X desbloqueados
        DatosCPU("AMD Ryzen 7 7700X",            8,  5.4),
        DatosCPU("AMD Ryzen 7 7800X3D",          8,  5.0),
        DatosCPU("AMD Ryzen 9 5900X",           12,  4.8),
        DatosCPU("AMD Ryzen 9 5950X",           16,  4.9),
        DatosCPU("AMD Ryzen 9 7900X",           12,  5.6),
        DatosCPU("AMD Ryzen 9 7900X3D",         12,  5.6),
        DatosCPU("AMD Ryzen 9 7950X",           16,  5.7),
        DatosCPU("AMD Ryzen 9 7950X3D",         16,  5.7),
        DatosCPU("AMD Ryzen 9 9950X",           16,  5.7),
    ]

    # ─────────────────────────────────────────────
    #  GPUs
    # ─────────────────────────────────────────────

    GPUS_BASICA: list[DatosGPU] = [
        # NVIDIA — GTX 10 / 16 series (entrada)
        DatosGPU("NVIDIA GeForce GT 1030",       2, TipoMemoriaGPU.DDR4,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA GeForce GTX 1050 Ti",   4, TipoMemoriaGPU.GDDR5, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA GeForce GTX 1650",      4, TipoMemoriaGPU.GDDR5, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA GeForce GTX 1650 Super",4, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA GeForce GTX 1660",      6, TipoMemoriaGPU.GDDR5, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA GeForce RTX 3050",      8, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        # AMD — RX 6000 entry
        DatosGPU("AMD Radeon RX 6400",           4, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6500 XT",        4, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6600",           8, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        # Intel Arc entry
        DatosGPU("Intel Arc A380",               6, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("Intel Arc A580",               8, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIe),
    ]

    GPUS_INTERMEDIA: list[DatosGPU] = [
        # NVIDIA — RTX 30 / 40 mid
        DatosGPU("NVIDIA GeForce GTX 1660 Ti",   6, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA GeForce GTX 1660 Super",6, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 2060",              6, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 2060 Super",        8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 2070",              8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 3060",             12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 3060 Ti",           8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 3070",              8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 4060",              8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 4060 Ti",          16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 4070",             12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        # AMD — RX 6000 / 7000 mid
        DatosGPU("AMD Radeon RX 6600 XT",        8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6650 XT",        8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6700",          10, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6700 XT",       12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6750 XT",       12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 7600",           8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 7700 XT",       12, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 7800 XT",       16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        # Intel Arc mid
        DatosGPU("Intel Arc A750",               8, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("Intel Arc A770",              16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
    ]

    GPUS_GAMER: list[DatosGPU] = [
        # NVIDIA RTX 30 alta gama
        DatosGPU("NVIDIA RTX 3080",             10, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 3080 Ti",          12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 3090",             24, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 3090 Ti",          24, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        # NVIDIA RTX 40 alta gama
        DatosGPU("NVIDIA RTX 4070 Ti",          12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 4070 Ti Super",    16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 4080",             16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 4080 Super",       16, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("NVIDIA RTX 4090",             24, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIe),
        # AMD RX 6000 alta gama
        DatosGPU("AMD Radeon RX 6800",          16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6800 XT",       16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6900 XT",       16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 6950 XT",       16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        # AMD RX 7000 alta gama
        DatosGPU("AMD Radeon RX 7900 GRE",      16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 7900 XT",       20, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 7900 XTX",      24, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
        DatosGPU("AMD Radeon RX 7900M",         16, TipoMemoriaGPU.GDDR6,  TipoGPU.DEDICADA, InterfazGPU.PCIe),
    ]

    # ─────────────────────────────────────────────
    #  RAM  (4 slots en desktop)
    # ─────────────────────────────────────────────

    RAM_BASICA      = DatosRAM("DDR4", 2666, capacidad_slot_gb=8,  max_ram_gb=32,  opciones_gb=(4, 8, 16, 32),      n_slots=4)
    RAM_INTERMEDIA  = DatosRAM("DDR5", 4800, capacidad_slot_gb=16, max_ram_gb=64,  opciones_gb=(16, 32, 64),        n_slots=4)
    RAM_GAMER       = DatosRAM("DDR5", 6000, capacidad_slot_gb=32, max_ram_gb=128, opciones_gb=(32, 64, 128),       n_slots=4)

    # ─────────────────────────────────────────────
    #  SSD principal
    # ─────────────────────────────────────────────

    SSD_BASICA      = DatosSSD(InterfazSSD.SATA,    550,   opciones_gb=(256, 512, 1024))
    SSD_INTERMEDIA  = DatosSSD(InterfazSSD.M2_NVME, 5000,  opciones_gb=(512, 1024, 2048))
    SSD_GAMER       = DatosSSD(InterfazSSD.M2_NVME, 10000, opciones_gb=(1024, 2048, 4096))

    # ─────────────────────────────────────────────
    #  Fuente de poder (watts)
    # ─────────────────────────────────────────────

    FUENTE_BASICA:      tuple[int, ...] = (300, 350, 400, 450)
    FUENTE_INTERMEDIA:  tuple[int, ...] = (550, 600, 650, 750)
    FUENTE_GAMER:       tuple[int, ...] = (850, 1000, 1200, 1600)

    # ─────────────────────────────────────────────
    #  Modelos de equipo
    # ─────────────────────────────────────────────

    MODELOS_BASICA: list[str] = [
        "Acer Aspire TC-885",
        "ASUS VivoPC M32",
        "Dell Inspiron 3020",
        "Dell OptiPlex 3000",
        "Dell OptiPlex 3090",
        "HP Slimline 290",
        "HP 280 G4",
        "Lenovo IdeaCentre 3",
        "Lenovo IdeaCentre AIO 3",
        "MSI Pro DP21",
    ]

    MODELOS_INTERMEDIA: list[str] = [
        "Acer Aspire TC-1760",
        "ASUS ExpertCenter D5",
        "ASUS ProArt Station PD5",
        "Dell Inspiron 3910",
        "Dell OptiPlex 5000",
        "HP Pavilion TP01",
        "HP EliteDesk 800 G6",
        "Lenovo IdeaCentre 5",
        "Lenovo ThinkCentre M70s",
        "MSI Pro DP130",
        "Zotac ZBOX Magnus One",
    ]

    MODELOS_GAMER: list[str] = [
        "Acer Predator Orion 3000",
        "Acer Predator Orion 5000",
        "Acer Predator Orion 7000",
        "Alienware Aurora R15",
        "Alienware Aurora R16",
        "ASUS ROG Strix GT35",
        "ASUS ROG Strix GT15",
        "Corsair One i300",
        "HP OMEN 45L",
        "HP OMEN 25L",
        "Lenovo Legion Tower 5i",
        "Lenovo Legion Tower 7i",
        "MSI Aegis Ti5",
        "MSI MEG Infinite X2",
        "MSI Trident X2",
        "Thermaltake Tower 900",
    ]