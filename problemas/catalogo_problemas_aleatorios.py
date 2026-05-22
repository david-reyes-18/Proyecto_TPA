"""
Catálogo de Problemas Aleatorios
==================================
Colección de problemas prefabricados que aparecen al azar durante el juego.
Cada problema es autocontenido: tiene su componente afectado, pasos de reparación
y desafíos ya configurados. El sistema sólo necesita pedir uno aleatoriamente.

Categorías incluidas:
  • RAM    (laptop y PC)   – 5 problemas
  • SSD    (laptop y PC)   – 5 problemas
  • Batería (laptop)       – 4 problemas
  • GPU    (PC)            – 4 problemas
  • CPU    (PC y laptop)   – 4 problemas
  • Pantalla (laptop)      – 3 problemas
  Total: 25 problemas aleatorios

Uso:
    from problemas.catalogo_problemas_aleatorios import CatalogoProblemasAleatorios

    # Obtener uno al azar
    problema = CatalogoProblemasAleatorios.obtener_aleatorio()

    # Obtener uno al azar de un componente específico
    from desafios.componente_tematico import ComponenteTematico
    problema_ram = CatalogoProblemasAleatorios.obtener_aleatorio_por_componente(
        ComponenteTematico.RAM
    )

    # Ver todos disponibles
    todos = CatalogoProblemasAleatorios.obtener_todos()
"""

import random
from problemas.problema import Problema
from problemas.paso_de_reparacion import PasoDeReparacion

# Componentes
from componentes.ram.ram import RAM
from componentes.ram.generacion_ram import GeneracionRAM
from componentes.ram.formato_ram import FormatoRAM
from componentes.ssd.ssd import SSD
from componentes.ssd.interfaz_ssd import InterfazSSD
from componentes.bateria.bateria import Bateria
from componentes.bateria.forma_bateria import FormaBateria
from componentes.gpu.gpu import GPU
from componentes.gpu.tipo_gpu import TipoGPU
from componentes.gpu.tipo_memoria_gpu import TipoMemoriaGPU
from componentes.gpu.tipo_interfaz import InterfazGPU
from componentes.cpu.cpu import CPU
from componentes.cpu.socket import SocketCPU
from componentes.pantalla.pantalla import Pantalla
from componentes.pantalla.tipo_panel import TipoPanel

# Desafíos
from desafios.dificultad_desafio import NivelDificultad
from desafios.componente_tematico import ComponenteTematico

from desafios.desafio_logico.desafio_logico_booleano import DesafioLogicoBooleano
from desafios.desafio_logico.desafio_logico_multiple import DesafioLogicoMultiple
from desafios.desafio_logico.desafio_logico_escritura import DesafioLogicoEscritura

from desafios.desafio_matematico.desafio_matematico_booleano import DesafioMatematicoBooleano
from desafios.desafio_matematico.desafio_matematico_multiple import DesafioMatematicoMultiple
from desafios.desafio_matematico.desafio_matematico_escritura import DesafioMatematicoEscritura

from desafios.desafio_tecnologico.desafio_tecnologico_booleano import DesafioTecnologicoBooleano
from desafios.desafio_tecnologico.desafio_tecnologico_multiple import DesafioTecnologicoMultiple
from desafios.desafio_tecnologico.desafio_tecnologico_escritura import DesafioTecnologicoEscritura

_RAM = ComponenteTematico.RAM
_SSD = ComponenteTematico.SSD
_BAT = ComponenteTematico.BATERIA
_GPU = ComponenteTematico.GPU
_CPU = ComponenteTematico.CPU
_PAN = ComponenteTematico.PANTALLA
_GEN = ComponenteTematico.GENERAL

F = NivelDificultad.FACIL
M = NivelDificultad.MEDIA
D = NivelDificultad.DIFICIL


# ══════════════════════════════════════════════════════════════════════════════
#  RAM – 5 problemas
# ══════════════════════════════════════════════════════════════════════════════

class ProblemaAleatorio_RAM_1(Problema):
    """Laptop: un módulo SO-DIMM DDR4 no es detectado tras un golpe."""

    def __init__(self):
        super().__init__(
            nombre="Módulo RAM no detectado tras golpe (Laptop)",
            descripcion_email=(
                "El sistema reporta solo 4 GB de RAM cuando debería tener 8 GB. "
                "Tras un golpe uno de los módulos SO-DIMM DDR4 quedó mal asentado."
            ),
            componente_afectado=RAM("RAM SO-DIMM DDR4 4 GB", 4, 2666, GeneracionRAM.DDR4, FormatoRAM.SO_DIMM),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Apagar la laptop y retirar la batería",
                    "Siempre cortar energía antes de manipular RAM.",
                    DesafioLogicoBooleano("¿Se debe desconectar la batería antes de retirar la RAM?", True, _GEN, F),
                ),
                PasoDeReparacion(
                    "Retirar y reinsertar el módulo mal asentado",
                    "Presionar hasta escuchar el doble clic de las pestañas.",
                    DesafioLogicoMultiple(
                        "¿Qué ángulo adopta un módulo SO-DIMM al liberarse las pestañas?",
                        ["90°", "45°", "180°", "0°"], 1, _RAM, M,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar que el sistema detecta 8 GB",
                    "El POST y el SO deben reportar la capacidad completa.",
                    DesafioMatematicoEscritura(
                        "Hay 2 módulos de 4 GB. ¿Cuántos GB en total debe reportar el sistema?",
                        8, _RAM, F,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_RAM_2(Problema):
    """PC escritorio: error de paridad de memoria en canal A."""

    def __init__(self):
        super().__init__(
            nombre="Error de paridad en canal A – PC",
            descripcion_email=(
                "El sistema presenta pantallazos azules con error MEMORY_MANAGEMENT. "
                "El diagnóstico indica fallo en el módulo del canal A slot 1."
            ),
            componente_afectado=RAM("RAM DIMM DDR4 16 GB", 16, 3200, GeneracionRAM.DDR4, FormatoRAM.DIMM),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Ejecutar MemTest86 para identificar el módulo defectuoso",
                    "Probar un módulo a la vez; el que genera errores es el defectuoso.",
                    DesafioTecnologicoBooleano(
                        "¿MemTest86 permite identificar qué módulo RAM específico está fallando?",
                        True, _RAM, M,
                    ),
                ),
                PasoDeReparacion(
                    "Retirar el módulo defectuoso del slot 1 canal A",
                    "El módulo DIMM se retira presionando las pestañas blancas en ambos extremos.",
                    DesafioTecnologicoMultiple(
                        "¿Qué formato de RAM se usa en PCs de escritorio convencionales?",
                        ["SO-DIMM", "LPDDR", "DIMM", "MXM"], 2, _RAM, F,
                    ),
                ),
                PasoDeReparacion(
                    "Instalar módulo DDR4 DIMM de reemplazo",
                    "El nuevo módulo debe ser DDR4 DIMM con velocidad igual o compatible.",
                    DesafioLogicoBooleano(
                        "¿Un módulo DDR5 DIMM puede instalarse en un slot DDR4?",
                        False, _RAM, F,
                    ),
                ),
                PasoDeReparacion(
                    "Calcular nuevo ancho de banda en dual channel",
                    "Reemplazado el módulo, el sistema vuelve a dual channel.",
                    DesafioMatematicoBooleano(
                        "¿DDR4-3200 tiene velocidad efectiva de 3200 MT/s?",
                        True, _RAM, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_RAM_3(Problema):
    """Laptop: intento fallido de instalar DDR5 en placa DDR4."""

    def __init__(self):
        super().__init__(
            nombre="RAM incompatible instalada – Laptop no arranca",
            descripcion_email=(
                "Tras comprar RAM nueva DDR5, la laptop no arranca. "
                "Se instaló un módulo DDR5 SO-DIMM en una placa que sólo acepta DDR4."
            ),
            componente_afectado=RAM("RAM SO-DIMM DDR5 16 GB (incompatible)", 16, 4800, GeneracionRAM.DDR5, FormatoRAM.SO_DIMM),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Identificar la generación de RAM soportada por la placa",
                    "El manual de la laptop especifica si usa DDR4 o DDR5; nunca mezclar generaciones.",
                    DesafioTecnologicoBooleano(
                        "¿Un módulo DDR5 SO-DIMM es compatible físicamente con un slot DDR4 SO-DIMM?",
                        False, _RAM, F,
                    ),
                ),
                PasoDeReparacion(
                    "Retirar el módulo DDR5 incompatible",
                    "Presionar las pestañas para liberar el módulo a 45° y extraerlo.",
                    DesafioLogicoMultiple(
                        "¿Qué debe verificarse ANTES de comprar RAM de reemplazo?",
                        [
                            "El color del módulo",
                            "La generación y el formato soportados por la placa",
                            "La marca del fabricante",
                            "El peso del módulo",
                        ],
                        1, _RAM, F,
                    ),
                ),
                PasoDeReparacion(
                    "Instalar módulo DDR4 SO-DIMM correcto de 16 GB",
                    "El módulo correcto debe ser DDR4 SO-DIMM; encajará sin forzar.",
                    DesafioMatematicoEscritura(
                        "Si la laptop tenía 8 GB DDR4 y se agrega 1 módulo de 16 GB DDR4, ¿cuántos GB totales?",
                        24, _RAM, F,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_RAM_4(Problema):
    """PC escritorio: RAM LPDDR soldada en laptop no reemplazable (caso de diagnóstico)."""

    def __init__(self):
        super().__init__(
            nombre="RAM LPDDR soldada – No reemplazable (diagnóstico)",
            descripcion_email=(
                "El cliente quiere ampliar la RAM de su laptop ultradelgada. "
                "El diagnóstico revela que la RAM LPDDR5 está soldada en la placa; "
                "no puede reemplazarse y se orienta al cliente sobre alternativas."
            ),
            componente_afectado=RAM("RAM LPDDR5 16 GB (soldada)", 16, 6400, GeneracionRAM.LPDDR5, FormatoRAM.LPDDR),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Verificar si la RAM es soldada (LPDDR) o modular (SO-DIMM)",
                    "Abrir el panel inferior; si no hay slots visibles, la RAM es LPDDR soldada.",
                    DesafioTecnologicoBooleano(
                        "¿La RAM LPDDR soldada en una laptop puede reemplazarse fácilmente por el usuario?",
                        False, _RAM, M,
                    ),
                ),
                PasoDeReparacion(
                    "Explicar al cliente las opciones disponibles",
                    "Si la RAM es soldada, la única opción es adquirir un equipo con más RAM de fábrica.",
                    DesafioLogicoBooleano(
                        "¿Puede instalarse más RAM en una laptop con memoria LPDDR soldada?",
                        False, _RAM, F,
                    ),
                ),
                PasoDeReparacion(
                    "Calcular la velocidad efectiva de la RAM LPDDR5 instalada",
                    "LPDDR5 a 6400 MT/s es significativamente más rápida que DDR4-3200.",
                    DesafioMatematicoEscritura(
                        "LPDDR5 opera a 6400 MT/s y DDR4-3200 a 3200 MT/s. ¿Cuántos MT/s más rápida es la LPDDR5?",
                        3200, _RAM, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_RAM_5(Problema):
    """PC escritorio: mezcla de módulos DDR4 de diferentes velocidades causa inestabilidad."""

    def __init__(self):
        super().__init__(
            nombre="Mezcla de RAM de distinta velocidad – PC inestable",
            descripcion_email=(
                "La PC fue ensamblada con un módulo DDR4-3200 y otro DDR4-2666; "
                "el sistema es inestable y presenta cuelgues aleatorios."
            ),
            componente_afectado=RAM("RAM DIMM DDR4 8 GB 2666 MHz", 8, 2666, GeneracionRAM.DDR4, FormatoRAM.DIMM),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Identificar la velocidad de cada módulo instalado",
                    "Usar CPU-Z o el BIOS para ver la velocidad real de cada slot RAM.",
                    DesafioTecnologicoBooleano(
                        "¿Mezclar módulos DDR4 de diferente velocidad puede causar inestabilidad?",
                        True, _RAM, M,
                    ),
                ),
                PasoDeReparacion(
                    "Retirar el módulo de menor velocidad (DDR4-2666)",
                    "Para estabilizar el sistema, reemplazar el módulo más lento por uno de igual velocidad al existente.",
                    DesafioLogicoMultiple(
                        "Al mezclar DDR4-3200 con DDR4-2666, ¿a qué velocidad operará el sistema?",
                        [
                            "3200 MHz (el más rápido)",
                            "2933 MHz (promedio)",
                            "2666 MHz (el más lento)",
                            "Depende del fabricante de la placa",
                        ],
                        2, _RAM, D,
                    ),
                ),
                PasoDeReparacion(
                    "Instalar módulo DDR4-3200 homogéneo",
                    "Dos módulos de la misma velocidad aseguran estabilidad y posibilitan dual channel.",
                    DesafioMatematicoEscritura(
                        "Con 2 módulos de 8 GB en dual channel, ¿cuántos GB totales tiene el sistema?",
                        16, _RAM, F,
                    ),
                ),
                PasoDeReparacion(
                    "Activar XMP y verificar estabilidad con MemTest86",
                    "Activar el perfil XMP en BIOS lleva la RAM a su velocidad nominal garantizada.",
                    DesafioMatematicoBooleano(
                        "DDR4 a 1600 MHz de reloj real equivale a 3200 MT/s efectivos. ¿Correcto?",
                        True, _RAM, D,
                    ),
                ),
            ],
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SSD – 5 problemas
# ══════════════════════════════════════════════════════════════════════════════

class ProblemaAleatorio_SSD_1(Problema):
    """PC escritorio: SSD SATA con velocidades degradadas al 40% por firmware viejo."""

    def __init__(self):
        super().__init__(
            nombre="SSD SATA con rendimiento degradado – PC",
            descripcion_email=(
                "El SSD SATA de 500 GB funciona a 200 MB/s cuando debería alcanzar 550 MB/s. "
                "Firmware desactualizado y caché saturada degradan el rendimiento."
            ),
            componente_afectado=SSD("WD Blue 500 GB SATA", 500, InterfazSSD.SATA, 550, 520),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Actualizar el firmware del SSD",
                    "El fabricante publica actualizaciones que corrigen bugs de rendimiento.",
                    DesafioTecnologicoBooleano(
                        "¿Los SSDs no tienen partes móviles, lo que los hace más resistentes a golpes?",
                        True, _SSD, F,
                    ),
                ),
                PasoDeReparacion(
                    "Ejecutar TRIM para recuperar celdas marcadas como usadas",
                    "TRIM libera celdas vacías para que el controlador pueda escribir en ellas directamente.",
                    DesafioTecnologicoMultiple(
                        "¿Cuál es la velocidad máxima aproximada de un SSD SATA III?",
                        ["200 MB/s", "550 MB/s", "3500 MB/s", "7000 MB/s"], 1, _SSD, F,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar velocidades con CrystalDiskMark",
                    "Tras el firmware y el TRIM, las velocidades deben volver a 500+ MB/s de lectura.",
                    DesafioMatematicoEscritura(
                        "El SSD ahora lee a 530 MB/s. ¿Cuántos segundos tarda en leer 5.3 GB?",
                        10, _SSD, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_SSD_2(Problema):
    """Laptop: SSD M.2 NVMe no reconocido tras reinstalación del SO."""

    def __init__(self):
        super().__init__(
            nombre="SSD NVMe no reconocido tras reinstalar SO – Laptop",
            descripcion_email=(
                "Tras reinstalar Windows, el SSD M.2 NVMe aparece en BIOS pero "
                "el instalador no lo detecta. El modo SATA está habilitado en lugar de NVMe."
            ),
            componente_afectado=SSD("Samsung 980 Pro 1 TB", 1000, InterfazSSD.M2_NVME, 7000, 5100),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Cambiar el modo SATA a NVMe en la configuración BIOS",
                    "El slot M.2 puede operar en modo SATA o NVMe; debe configurarse según el SSD instalado.",
                    DesafioTecnologicoBooleano(
                        "¿NVMe utiliza el bus PCIe para comunicarse con la CPU?",
                        True, _SSD, M,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar que el instalador detecta el SSD NVMe",
                    "Tras cambiar el modo, el instalador de Windows debe listar el SSD disponible.",
                    DesafioLogicoBooleano(
                        "¿Un SSD M.2 NVMe puede instalarse en un slot M.2 que solo soporta SATA?",
                        False, _SSD, M,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar velocidades finales del SSD NVMe",
                    "Con el SO instalado y el modo correcto, el SSD debe alcanzar sus velocidades nominales.",
                    DesafioMatematicoBooleano(
                        "Un SSD NVMe con 7000 MB/s de lectura es más rápido que uno SATA con 550 MB/s. ¿Correcto?",
                        True, _SSD, F,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_SSD_3(Problema):
    """PC escritorio: SSD casi lleno causando lentitud extrema del sistema."""

    def __init__(self):
        super().__init__(
            nombre="SSD al 95% de capacidad – PC extremadamente lenta",
            descripcion_email=(
                "La PC va muy lenta porque el SSD de 256 GB está al 95% de su capacidad. "
                "Con menos del 5% libre, el controlador no puede hacer garbage collection."
            ),
            componente_afectado=SSD("Crucial MX500 256 GB SATA", 256, InterfazSSD.SATA, 560, 510),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Liberar espacio eliminando archivos innecesarios",
                    "Mantener al menos 15-20% libre para un rendimiento óptimo del SSD.",
                    DesafioMatematicoEscritura(
                        "El SSD tiene 256 GB y está al 95% lleno. ¿Cuántos GB libres hay?",
                        12, _SSD, F,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar por SSD de mayor capacidad si no hay archivos prescindibles",
                    "Si no hay espacio que liberar, migrar a un SSD de 512 GB o más.",
                    DesafioLogicoMultiple(
                        "¿Qué consecuencia tiene un SSD con menos del 5% de espacio libre?",
                        [
                            "El SSD falla inmediatamente",
                            "El rendimiento de escritura se degrada severamente",
                            "Aumenta la velocidad de lectura",
                            "El sistema operativo lo formatea automáticamente",
                        ],
                        1, _SSD, M,
                    ),
                ),
                PasoDeReparacion(
                    "Ejecutar TRIM y verificar velocidades de escritura",
                    "Después de liberar espacio, TRIM recupera las celdas y el rendimiento mejora.",
                    DesafioMatematicoEscritura(
                        "Ahora el SSD tiene 100 GB libres de 256 GB. ¿Qué porcentaje libre representa?",
                        39, _SSD, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_SSD_4(Problema):
    """Laptop: SSD con sectores dañados detectados en diagnóstico rutinario."""

    def __init__(self):
        super().__init__(
            nombre="Sectores dañados detectados en diagnóstico – Laptop",
            descripcion_email=(
                "En una revisión de rutina se detectó que el SSD M.2 SATA tiene "
                "un 32% de sectores dañados. El sistema lo marca como no funcional."
            ),
            componente_afectado=SSD("Transcend MTS820 256 GB M.2 SATA", 256, InterfazSSD.M2_SATA, 550, 500),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar porcentaje de sectores dañados con CrystalDiskInfo",
                    "Más del 30% de sectores dañados indica que el SSD debe reemplazarse.",
                    DesafioMatematicoBooleano(
                        "¿Si el SSD supera el 30% de sectores dañados el sistema lo considera fuera de servicio?",
                        True, _SSD, F,
                    ),
                ),
                PasoDeReparacion(
                    "Hacer backup urgente de los datos antes del reemplazo",
                    "Un SSD dañado puede fallar en cualquier momento; el backup es la prioridad.",
                    DesafioLogicoMultiple(
                        "¿Cuál es la acción MÁS urgente cuando se detectan sectores dañados en el SSD?",
                        [
                            "Formatear el SSD para limpiar los sectores",
                            "Hacer backup de los datos inmediatamente",
                            "Continuar usando el equipo hasta que falle",
                            "Reinstalar el sistema operativo",
                        ],
                        1, _SSD, F,
                    ),
                ),
                PasoDeReparacion(
                    "Instalar SSD M.2 SATA de reemplazo de igual o mayor capacidad",
                    "El nuevo SSD M.2 SATA debe caber en el mismo slot M.2 SATA de la laptop.",
                    DesafioTecnologicoBooleano(
                        "¿Un SSD con interfaz SATA puede conectarse a un slot M.2 si la placa tiene M.2 SATA?",
                        True, _SSD, D,
                    ),
                ),
                PasoDeReparacion(
                    "Restaurar backup y verificar integridad de archivos",
                    "Comprobar que todos los archivos importantes se recuperaron correctamente.",
                    DesafioMatematicoEscritura(
                        "El nuevo SSD SATA lee a 550 MB/s. ¿Cuántos segundos tarda en leer 5.5 GB de backup?",
                        10, _SSD, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_SSD_5(Problema):
    """PC escritorio: el usuario instaló un SSD NVMe en slot M.2 SATA (incompatible)."""

    def __init__(self):
        super().__init__(
            nombre="SSD NVMe en slot M.2 SATA – No reconocido (PC)",
            descripcion_email=(
                "Se instaló un SSD M.2 NVMe en un slot M.2 que solo soporta SATA; "
                "el BIOS no detecta el dispositivo. El slot es M.2 SATA, no NVMe."
            ),
            componente_afectado=SSD("Kingston NV3 1 TB NVMe", 1000, InterfazSSD.M2_NVME, 3500, 2800),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar la interfaz soportada por el slot M.2 de la placa",
                    "El manual de la placa indica si el slot soporta SATA, NVMe o ambos.",
                    DesafioLogicoBooleano(
                        "¿Un SSD M.2 NVMe funcionará en un slot M.2 que solo soporta SATA?",
                        False, _SSD, M,
                    ),
                ),
                PasoDeReparacion(
                    "Retirar el SSD NVMe del slot SATA incompatible",
                    "El SSD encaja físicamente pero no es funcional al ser el protocolo incompatible.",
                    DesafioTecnologicoBooleano(
                        "¿Un SSD SATA y un SSD M.2 NVMe tienen el mismo protocolo de comunicación?",
                        False, _SSD, M,
                    ),
                ),
                PasoDeReparacion(
                    "Instalar un SSD M.2 SATA compatible en el slot",
                    "El reemplazo debe ser M.2 SATA para que funcione en ese slot específico.",
                    DesafioTecnologicoMultiple(
                        "¿Cuál de estas interfaces es compatible con un slot M.2 SATA?",
                        ["M.2 NVMe PCIe 4.0", "M.2 SATA", "M.2 NVMe PCIe 3.0", "SATA III externo"],
                        1, _SSD, M,
                    ),
                ),
            ],
        )


# ══════════════════════════════════════════════════════════════════════════════
#  BATERÍA – 4 problemas
# ══════════════════════════════════════════════════════════════════════════════

class ProblemaAleatorio_BAT_1(Problema):
    """Laptop: la batería no carga más del 60% aunque pasa horas conectada."""

    def __init__(self):
        super().__init__(
            nombre="Batería que no carga más del 60% – Laptop",
            descripcion_email=(
                "La laptop siempre muestra la batería al 60% aunque esté conectada horas. "
                "La salud es del 28%; el sistema la considera dañada."
            ),
            componente_afectado=Bateria(11.1, FormaBateria.RECTANGULAR, 45.0, 28, True),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Verificar salud con BatteryInfoView",
                    "Con 28% de salud la batería está por debajo del umbral del 30%; debe reemplazarse.",
                    DesafioMatematicoBooleano(
                        "¿Una batería con salud del 28% debe reemplazarse según los criterios del sistema?",
                        True, _BAT, F,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar la batería por una RECTANGULAR de 11.1 V",
                    "Mismo voltaje y misma forma son obligatorios para el reemplazo.",
                    DesafioLogicoMultiple(
                        "¿Qué parámetros son obligatorios al reemplazar una batería?",
                        [
                            "Solo la capacidad en Wh",
                            "Voltaje y forma de la batería",
                            "Solo el voltaje",
                            "Marca y modelo exacto",
                        ],
                        1, _BAT, D,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar autonomía con la nueva batería de 60 Wh",
                    "Con 60 Wh y 15 W de consumo, la laptop debería durar 4 horas.",
                    DesafioMatematicoEscritura(
                        "La nueva batería tiene 60 Wh y el sistema consume 15 W. ¿Cuántas horas dura?",
                        4, _BAT, F,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_BAT_2(Problema):
    """Laptop: se instaló batería con voltaje incorrecto (12.6 V en lugar de 11.1 V)."""

    def __init__(self):
        super().__init__(
            nombre="Batería con voltaje incorrecto instalada – Laptop",
            descripcion_email=(
                "Tras comprar una batería de reemplazo se instaló una de 12.6 V "
                "en un equipo que requiere 11.1 V. El sistema la rechaza por voltaje incorrecto."
            ),
            componente_afectado=Bateria(12.6, FormaBateria.RECTANGULAR, 56.0, 95, False),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar que el sistema rechaza la batería por voltaje incorrecto",
                    "Una batería de 12.6 V puede dañar permanentemente la placa base del equipo.",
                    DesafioLogicoBooleano(
                        "¿Puede instalarse una batería de 12.6 V en un equipo diseñado para 11.1 V?",
                        False, _BAT, M,
                    ),
                ),
                PasoDeReparacion(
                    "Retirar la batería incorrecta antes de encender el equipo",
                    "Si el equipo se enciende con la batería incorrecta puede sufrir daños irreversibles.",
                    DesafioTecnologicoBooleano(
                        "¿El voltaje nominal de una celda de litio típica es de 3.7 V?",
                        True, _BAT, M,
                    ),
                ),
                PasoDeReparacion(
                    "Instalar batería correcta de 11.1 V con la misma forma",
                    "Adquirir la batería correcta con voltaje de 11.1 V (3 celdas en serie a 3.7 V cada una).",
                    DesafioTecnologicoEscritura(
                        "Cada celda de litio tiene 3.7 V. ¿Qué voltaje total entregan 3 celdas en serie?",
                        11.1, _BAT, F,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_BAT_3(Problema):
    """Laptop: batería se descarga al 0% muy rápido aunque el medidor dice 40%."""

    def __init__(self):
        super().__init__(
            nombre="Indicador de batería descalibrado – Apaga sola al 40%",
            descripcion_email=(
                "La laptop se apaga abruptamente cuando el indicador marca 40%. "
                "La batería tiene salud del 35% y el medidor del SO está descalibrado."
            ),
            componente_afectado=Bateria(11.1, FormaBateria.FORMA_L, 48.0, 35, True),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Verificar salud real con software especializado",
                    "La salud del 35% explica por qué la capacidad efectiva es baja.",
                    DesafioMatematicoEscritura(
                        "La batería original era de 48 Wh y tiene salud del 35%. ¿Cuántos Wh efectivos quedan?",
                        16, _BAT, M,
                    ),
                ),
                PasoDeReparacion(
                    "Determinar si la batería aún supera el umbral mínimo del 30%",
                    "Con salud del 35% la batería está por encima del umbral; puede decidirse reemplazarla igualmente.",
                    DesafioLogicoBooleano(
                        "¿Una batería con salud del 35% supera el umbral mínimo del 30% del sistema?",
                        True, _BAT, M,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar la batería FORMA_L por una de igual voltaje y forma",
                    "Con salud marginal y comportamiento errático, lo más prudente es el reemplazo.",
                    DesafioTecnologicoMultiple(
                        "Una batería en forma de 'L' corresponde al tipo:",
                        ["RECTANGULAR", "FORMA_L", "IRREGULAR", "CILÍNDRICA"],
                        1, _BAT, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_BAT_4(Problema):
    """Laptop: batería en buen estado pero el cargador dañado impide la carga."""

    def __init__(self):
        super().__init__(
            nombre="Cargador dañado – Batería sin carga aunque está en buen estado",
            descripcion_email=(
                "La batería tiene 80% de salud pero nunca carga. "
                "El diagnóstico descarta la batería y apunta al cargador como causa."
            ),
            componente_afectado=Bateria(11.1, FormaBateria.RECTANGULAR, 72.0, 80, False),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Probar con un cargador alternativo conocido como bueno",
                    "Si con el cargador alternativo carga, el problema es el cargador original.",
                    DesafioTecnologicoBooleano(
                        "¿Una batería con salud del 80% puede considerarse funcional?",
                        True, _BAT, F,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar el voltaje de salida del cargador con multímetro",
                    "Un cargador dañado puede mostrar voltaje incorrecto o nulo en su salida.",
                    DesafioLogicoMultiple(
                        "Si la batería es buena pero no carga, ¿cuál es el primer elemento a verificar?",
                        [
                            "Reinstalar el sistema operativo",
                            "El cargador y el conector de carga",
                            "La RAM del equipo",
                            "El SSD del equipo",
                        ],
                        1, _BAT, F,
                    ),
                ),
                PasoDeReparacion(
                    "Calcular autonomía real con la batería al 80% de salud",
                    "Con 80% de salud la batería retiene 57.6 Wh de los 72 Wh originales.",
                    DesafioMatematicoEscritura(
                        "Batería de 72 Wh con salud del 80%. ¿Cuántos Wh efectivos tiene?",
                        57, _BAT, M,
                    ),
                ),
            ],
        )


# ══════════════════════════════════════════════════════════════════════════════
#  GPU – 4 problemas
# ══════════════════════════════════════════════════════════════════════════════

class ProblemaAleatorio_GPU_1(Problema):
    """PC escritorio: GPU con ventiladores que no giran causando throttling."""

    def __init__(self):
        super().__init__(
            nombre="Ventiladores de GPU bloqueados – Throttling severo (PC)",
            descripcion_email=(
                "Los ventiladores de la RTX 4070 no giran. La GPU hace throttling "
                "desde 95°C y el rendimiento cae un 60%."
            ),
            componente_afectado=GPU("RTX 4070", 12, TipoMemoriaGPU.GDDR6X, TipoGPU.DEDICADA, InterfazGPU.PCIE, 200),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar que los ventiladores no giran con software de monitoreo",
                    "GPU-Z muestra la velocidad de los fans en RPM; 0 RPM bajo carga indica fallo.",
                    DesafioLogicoBooleano(
                        "¿Un CPU/GPU con sobrecalentamiento puede reducir su frecuencia automáticamente?",
                        True, _GPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Retirar la GPU y limpiar los ventiladores con aire comprimido",
                    "El polvo acumulado puede bloquear los rodamientos de los ventiladores.",
                    DesafioMatematicoBooleano(
                        "¿Una GPU con TDP 300 W consume exactamente 300 W en todo momento?",
                        False, _GPU, M,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar el ventilador dañado si la limpieza no resuelve el problema",
                    "Los ventiladores de GPU se venden por separado; deben coincidir el conector y el tamaño.",
                    DesafioTecnologicoBooleano(
                        "¿Las GPUs dedicadas de escritorio usan la interfaz PCIe x16?",
                        True, _GPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Calcular el consumo energético de la GPU durante 6 horas de gaming",
                    "Con el ventilador reparado, la GPU puede operar a su TDP nominal sin throttling.",
                    DesafioMatematicoEscritura(
                        "La GPU consume 200 W durante 6 horas de gaming. ¿Cuántos Wh consume?",
                        1200, _GPU, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_GPU_2(Problema):
    """PC escritorio: GPU integrada usada como fallback tras fallo de GPU dedicada."""

    def __init__(self):
        super().__init__(
            nombre="GPU dedicada sin señal – Sistema usa iGPU como fallback (PC)",
            descripcion_email=(
                "El monitor conectado a la GPU dedicada no muestra imagen. "
                "El sistema arranca correctamente usando la salida HDMI de la placa base (iGPU)."
            ),
            componente_afectado=GPU("RX 6600", 8, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.PCIE, 132),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar que el monitor funciona conectándolo a la salida HDMI de la placa",
                    "Si hay imagen por la placa, el problema es la GPU dedicada o su conexión.",
                    DesafioLogicoBooleano(
                        "¿Una GPU integrada comparte la RAM del sistema en lugar de tener VRAM dedicada?",
                        True, _GPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar que la GPU PCIe está bien asentada y con cables de alimentación",
                    "Una GPU PCIe mal asentada o sin los cables de poder no genera señal de video.",
                    DesafioTecnologicoMultiple(
                        "¿Qué interfaz usan las GPUs dedicadas en PCs de escritorio?",
                        ["MXM", "SATA", "PCIe x16", "USB4"], 2, _GPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar la GPU PCIe si el problema persiste tras reinsertar",
                    "Si la GPU dedicada continúa sin señal tras reinsertar y reconectar, está dañada.",
                    DesafioLogicoBooleano(
                        "¿Una GPU dedicada PCIe puede reemplazarse en una PC de escritorio si está dañada?",
                        True, _GPU, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_GPU_3(Problema):
    """PC escritorio: GPU con VRAM insuficiente para juegos modernos en 4K."""

    def __init__(self):
        super().__init__(
            nombre="VRAM insuficiente para 4K – Upgrade de GPU (PC)",
            descripcion_email=(
                "La GTX 1070 con 8 GB de GDDR5 ya no es suficiente para juegos en 4K. "
                "Texturas de alta resolución causan stuttering por falta de VRAM."
            ),
            componente_afectado=GPU("GTX 1070", 8, TipoMemoriaGPU.GDDR5, TipoGPU.DEDICADA, InterfazGPU.PCIE, 150),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar que el stuttering es por saturación de VRAM",
                    "GPU-Z muestra el uso de VRAM en tiempo real; si llega al 100% hay saturación.",
                    DesafioMatematicoEscritura(
                        "La GPU tiene 8 GB de VRAM y los juegos 4K usan 10 GB. ¿Cuántos GB faltan?",
                        2, _GPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Seleccionar GPU de reemplazo con ≥12 GB GDDR6 o superior",
                    "Una GPU moderna con 12-16 GB GDDR6X manejará 4K sin saturación de VRAM.",
                    DesafioTecnologicoMultiple(
                        "¿Cuál de estos tipos de memoria GPU tiene mayor ancho de banda?",
                        ["GDDR5", "GDDR6", "GDDR6X", "DDR4"], 2, _GPU, M,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar que la fuente tiene suficiente potencia para la nueva GPU",
                    "Una RTX 4080 consume hasta 320 W; la fuente debe tener margen suficiente.",
                    DesafioLogicoEscritura(
                        "La nueva GPU consume 320 W y la fuente tiene 850 W. El resto del sistema usa 200 W. ¿Cuántos W libres?",
                        330, _GPU, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_GPU_4(Problema):
    """Laptop: GPU MXM dedicada con fallo; debe derivarse a técnico especializado."""

    def __init__(self):
        super().__init__(
            nombre="GPU MXM dedicada con fallo – Laptop gaming",
            descripcion_email=(
                "La laptop gaming muestra artefactos y se reinicia durante los juegos. "
                "La GPU MXM dedicada está fallando y requiere técnico especializado."
            ),
            componente_afectado=GPU("RTX 3060 MXM", 6, TipoMemoriaGPU.GDDR6, TipoGPU.DEDICADA, InterfazGPU.MXM, 115),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar que la GPU MXM está fallando con stress-test",
                    "Ejecutar FurMark; si aparecen artefactos o el sistema se cuelga, la GPU es el problema.",
                    DesafioLogicoBooleano(
                        "¿Una GPU MXM en laptop puede reemplazarse por el usuario sin equipo especializado?",
                        False, _GPU, D,
                    ),
                ),
                PasoDeReparacion(
                    "Derivar al técnico especializado con equipo de reflow/reball",
                    "La GPU MXM requiere equipo BGA especializado para su reemplazo; no es una reparación de usuario.",
                    DesafioLogicoMultiple(
                        "Una laptop con GPU MXM que falla, ¿cuál es la acción correcta?",
                        [
                            "Reemplazarla por cuenta propia",
                            "Llevarla a técnico especializado con equipo BGA",
                            "Instalar GPU PCIe externa",
                            "Formatear el SO",
                        ],
                        1, _GPU, M,
                    ),
                ),
                PasoDeReparacion(
                    "Como alternativa temporal, usar solo la iGPU del procesador",
                    "Desactivar la GPU dedicada en el administrador de dispositivos y usar la iGPU integrada.",
                    DesafioTecnologicoBooleano(
                        "¿Una GPU integrada (iGPU) comparte RAM con el sistema en lugar de VRAM dedicada?",
                        True, _GPU, F,
                    ),
                ),
            ],
        )


# ══════════════════════════════════════════════════════════════════════════════
#  CPU – 4 problemas
# ══════════════════════════════════════════════════════════════════════════════

class ProblemaAleatorio_CPU_1(Problema):
    """PC escritorio: CPU soldada BGA en laptop no puede reemplazarse."""

    def __init__(self):
        super().__init__(
            nombre="CPU BGA soldada – No reemplazable (diagnóstico de laptop)",
            descripcion_email=(
                "El cliente quiere actualizar el CPU de su laptop ultradelgada. "
                "El CPU está soldado (BGA) y no puede reemplazarse sin equipo especializado."
            ),
            componente_afectado=CPU("Core i5-1235U", 10, 1.3, SocketCPU.BGA, 15),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Identificar si el CPU es BGA (soldado) o ZIF (socket)",
                    "En laptops ultradelgadas el CPU es BGA; en laptops gaming algunas tienen socket.",
                    DesafioTecnologicoBooleano(
                        "¿Un CPU soldado (BGA) en una laptop puede reemplazarse sin equipo especializado?",
                        False, _CPU, M,
                    ),
                ),
                PasoDeReparacion(
                    "Informar al cliente que el upgrade de CPU no es viable",
                    "La única opción es adquirir un equipo con el CPU deseado de fábrica.",
                    DesafioTecnologicoMultiple(
                        "¿Cuál de estos sockets es exclusivo de laptops (CPUs soldados)?",
                        ["AM4", "LGA1700", "BGA", "AM5"], 2, _CPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Calcular la diferencia de hilos entre el CPU actual y el deseado",
                    "El cliente consideraba un Core i7 de 12 núcleos; comparar el rendimiento teórico.",
                    DesafioMatematicoEscritura(
                        "El CPU actual tiene 10 núcleos con Hyper-Threading. ¿Cuántos hilos lógicos expone?",
                        20, _CPU, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_CPU_2(Problema):
    """PC escritorio: intento de instalar Ryzen 7000 en placa AM4."""

    def __init__(self):
        super().__init__(
            nombre="CPU incompatible con socket – Ryzen 7000 en placa AM4",
            descripcion_email=(
                "El cliente compró un Ryzen 9 7900X creyendo que era compatible con su placa AM4. "
                "El CPU es AM5 y no puede instalarse en el socket AM4."
            ),
            componente_afectado=CPU("Ryzen 9 7900X", 12, 4.7, SocketCPU.AM5, 170),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar la incompatibilidad de sockets AM4 vs AM5",
                    "AM4 y AM5 son sockets diferentes; físicamente el CPU no encaja.",
                    DesafioTecnologicoBooleano(
                        "¿Un Ryzen 7000 puede instalarse en un socket AM4 sin adaptador?",
                        False, _CPU, M,
                    ),
                ),
                PasoDeReparacion(
                    "Evaluar si actualizar la placa base a AM5 o cambiar el CPU",
                    "Migrar a AM5 es más costoso (placa + RAM DDR5); puede ser mejor comprar un Ryzen 5000.",
                    DesafioLogicoMultiple(
                        "¿En qué placa puede instalarse un Ryzen 9 7900X (AM5)?",
                        [
                            "Placa con socket AM4",
                            "Placa con socket LGA1700",
                            "Placa con socket AM5",
                            "Placa con socket BGA",
                        ],
                        2, _CPU, M,
                    ),
                ),
                PasoDeReparacion(
                    "Instalar CPU AM4 compatible (Ryzen 5000) en la placa existente",
                    "Un Ryzen 7 5800X AM4 es una alternativa potente compatible con la placa actual.",
                    DesafioMatematicoEscritura(
                        "El Ryzen 7 5800X tiene 8 núcleos con SMT. ¿Cuántos hilos lógicos expone?",
                        16, _CPU, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_CPU_3(Problema):
    """PC escritorio: pasta térmica seca; CPU a 90°C en idle."""

    def __init__(self):
        super().__init__(
            nombre="Pasta térmica seca – CPU a 90°C en reposo (PC)",
            descripcion_email=(
                "La PC tiene 5 años y el CPU marca 90°C incluso en el escritorio. "
                "La pasta térmica se secó y debe reemplazarse urgentemente."
            ),
            componente_afectado=CPU("Core i7-10700K", 8, 3.8, SocketCPU.LGA1200, 125),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Retirar el disipador y limpiar la pasta vieja",
                    "Limpiar con alcohol isopropílico al 99% en CPU y base del disipador.",
                    DesafioTecnologicoBooleano(
                        "¿La pasta térmica mejora la conductividad entre el CPU y el disipador?",
                        True, _CPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Aplicar nueva pasta térmica de calidad",
                    "Aplicar una cantidad del tamaño de un guisante en el centro del IHS del CPU.",
                    DesafioLogicoBooleano(
                        "¿Un CPU sobrecalentado puede reducir su frecuencia automáticamente?",
                        True, _CPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar temperatura bajo carga completa",
                    "Con la pasta nueva y el disipador bien montado, la temperatura debe bajar a <75°C bajo carga.",
                    DesafioLogicoEscritura(
                        "El CPU tiene TDP de 125 W y el disipador soporta 200 W. ¿Cuántos W de margen hay?",
                        75, _CPU, F,
                    ),
                ),
                PasoDeReparacion(
                    "Calcular el consumo energético en 8 horas de uso intensivo",
                    "Conocer el consumo ayuda a dimensionar la fuente de poder correctamente.",
                    DesafioMatematicoEscritura(
                        "El CPU consume 125 W durante 8 horas. ¿Cuántos Wh consume?",
                        1000, _CPU, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_CPU_4(Problema):
    """PC escritorio: CPU Intel LGA con pines de socket dañados por herramienta."""

    def __init__(self):
        super().__init__(
            nombre="Socket LGA con pines doblados – Intel (PC)",
            descripcion_email=(
                "Al instalar el CPU con una herramienta incorrecta se doblaron pines "
                "del socket LGA1700. El sistema no arranca y el LED de CPU está encendido."
            ),
            componente_afectado=CPU("Core i9-13900K", 24, 3.0, SocketCPU.LGA1700, 125),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Inspeccionar los pines del socket LGA1700 con lupa",
                    "Los sockets LGA tienen los pines en la placa base, no en el CPU.",
                    DesafioTecnologicoMultiple(
                        "¿Qué generación de Intel usa el socket LGA1700?",
                        ["8ª–9ª gen", "10ª–11ª gen", "12ª–14ª gen", "6ª–7ª gen"],
                        2, _CPU, D,
                    ),
                ),
                PasoDeReparacion(
                    "Intentar enderezar los pines con aguja fina bajo iluminación directa",
                    "Con paciencia, los pines levemente inclinados pueden recuperarse; los rotos no.",
                    DesafioLogicoBooleano(
                        "¿Si el socket LGA tiene pines rotos (no solo doblados) puede repararse sin cambiar la placa?",
                        False, _CPU, D,
                    ),
                ),
                PasoDeReparacion(
                    "Reinstalar el CPU y verificar que el POST lo reconoce",
                    "Tras enderezar los pines, instalar el CPU sin forzar y verificar el arranque.",
                    DesafioMatematicoEscritura(
                        "El Core i9-13900K tiene 24 núcleos con Hyper-Threading. ¿Cuántos hilos lógicos?",
                        48, _CPU, M,
                    ),
                ),
            ],
        )


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA – 3 problemas
# ══════════════════════════════════════════════════════════════════════════════

class ProblemaAleatorio_PAN_1(Problema):
    """Laptop: panel TN con retroiluminación parpadeante."""

    def __init__(self):
        super().__init__(
            nombre="Retroiluminación parpadeante – Panel TN (Laptop)",
            descripcion_email=(
                "La pantalla parpadea constantemente, especialmente con brillo bajo. "
                "El inversor o el cable LVDS puede estar dañado, o el panel mismo."
            ),
            componente_afectado=Pantalla(14, "1366x768", TipoPanel.TN, 60),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Conectar monitor externo para aislar si el problema es el panel o la GPU",
                    "Si el externo no parpadea, el problema es el panel interno o su cable.",
                    DesafioLogicoBooleano(
                        "Si el monitor externo no parpadea pero el interno sí, ¿el problema es el panel interno o su cable?",
                        True, _PAN, F,
                    ),
                ),
                PasoDeReparacion(
                    "Revisar y reconectar el cable EDP/LVDS del panel",
                    "Un cable flojo o dañado puede causar parpadeo intermitente.",
                    DesafioTecnologicoMultiple(
                        "¿Qué tipo de panel es más común en laptops de entrada por bajo costo?",
                        ["IPS", "VA", "OLED", "TN"], 3, _PAN, M,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar el panel TN por uno IPS si el cable no era el problema",
                    "Un panel IPS de 14\" 1920×1080 mejora notablemente la calidad de imagen.",
                    DesafioTecnologicoBooleano(
                        "¿Los paneles IPS ofrecen mejores ángulos de visión que los TN?",
                        True, _PAN, F,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_PAN_2(Problema):
    """Laptop: pixeles muertos en el centro del panel IPS."""

    def __init__(self):
        super().__init__(
            nombre="Píxeles muertos en panel IPS – Laptop",
            descripcion_email=(
                "Aparecieron 5 píxeles muertos en el centro de la pantalla IPS de 15\". "
                "Son visibles sobre fondos blancos y afectan la productividad."
            ),
            componente_afectado=Pantalla(15, "1920x1080", TipoPanel.IPS, 144),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar que son píxeles muertos y no suciedad en el vidrio",
                    "Limpiar la pantalla con paño de microfibra; si persisten, son píxeles muertos.",
                    DesafioLogicoBooleano(
                        "¿Los píxeles muertos pueden eliminarse limpiando la pantalla con paño?",
                        False, _PAN, F,
                    ),
                ),
                PasoDeReparacion(
                    "Intentar herramienta de recuperación de píxeles (JScreenFix)",
                    "Algunos píxeles atascados (no muertos) pueden recuperarse con señal de alta frecuencia.",
                    DesafioTecnologicoBooleano(
                        "¿Los paneles IPS tienen mejores colores y ángulos que los TN?",
                        True, _PAN, F,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar el panel IPS de 15\" 1080p 144 Hz si los píxeles no se recuperan",
                    "El nuevo panel debe tener el mismo tamaño, resolución aproximada y conector EDP compatible.",
                    DesafioMatematicoEscritura(
                        "¿Cuántos píxeles totales tiene una resolución 1920×1080?",
                        2073600, _PAN, M,
                    ),
                ),
            ],
        )


class ProblemaAleatorio_PAN_3(Problema):
    """Laptop: pantalla con imagen solo en la mitad inferior; fallo de controlador TCON."""

    def __init__(self):
        super().__init__(
            nombre="Imagen solo en mitad de pantalla – Fallo de TCON (Laptop)",
            descripcion_email=(
                "La mitad superior de la pantalla está completamente negra. "
                "En monitor externo la imagen es correcta; el panel VA tiene el controlador TCON dañado."
            ),
            componente_afectado=Pantalla(17, "2560x1440", TipoPanel.VA, 165),
            pasos_reparacion=[
                PasoDeReparacion(
                    "Confirmar el fallo en el panel con monitor externo",
                    "Imagen correcta en monitor externo confirma que la GPU y el cable EDP son correctos.",
                    DesafioLogicoBooleano(
                        "Si el monitor externo muestra imagen completa pero el interno solo la mitad, ¿el problema es el panel?",
                        True, _PAN, F,
                    ),
                ),
                PasoDeReparacion(
                    "Reemplazar el panel VA de 17\" 2560×1440 165 Hz",
                    "El TCON dañado no es reparable por separado; debe reemplazarse el panel completo.",
                    DesafioTecnologicoBooleano(
                        "¿Los paneles VA ofrecen mejor contraste que los IPS?",
                        True, _PAN, D,
                    ),
                ),
                PasoDeReparacion(
                    "Verificar la tasa de refresco del nuevo panel con software",
                    "Confirmar que el nuevo panel opera a 165 Hz en la configuración de pantalla del SO.",
                    DesafioMatematicoEscritura(
                        "¿Cuántos fotogramas por segundo puede mostrar un panel de 165 Hz como máximo?",
                        165, _PAN, F,
                    ),
                ),
            ],
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Clase catálogo – punto de acceso único
# ══════════════════════════════════════════════════════════════════════════════

class CatalogoProblemasAleatorios:
    """
    Catálogo de 25 problemas prefabricados que aparecen al azar durante el juego.

    Uso básico:
        from problemas.catalogo_problemas_aleatorios import CatalogoProblemasAleatorios
        from desafios.componente_tematico import ComponenteTematico

        problema = CatalogoProblemasAleatorios.obtener_aleatorio()
        problema_ram = CatalogoProblemasAleatorios.obtener_aleatorio_por_componente(ComponenteTematico.RAM)
        todos = CatalogoProblemasAleatorios.obtener_todos()
    """

    # Registro: componente → lista de clases de problema
    _REGISTRO: dict[ComponenteTematico, list[type]] = {
        ComponenteTematico.RAM: [
            ProblemaAleatorio_RAM_1,
            ProblemaAleatorio_RAM_2,
            ProblemaAleatorio_RAM_3,
            ProblemaAleatorio_RAM_4,
            ProblemaAleatorio_RAM_5,
        ],
        ComponenteTematico.SSD: [
            ProblemaAleatorio_SSD_1,
            ProblemaAleatorio_SSD_2,
            ProblemaAleatorio_SSD_3,
            ProblemaAleatorio_SSD_4,
            ProblemaAleatorio_SSD_5,
        ],
        ComponenteTematico.BATERIA: [
            ProblemaAleatorio_BAT_1,
            ProblemaAleatorio_BAT_2,
            ProblemaAleatorio_BAT_3,
            ProblemaAleatorio_BAT_4,
        ],
        ComponenteTematico.GPU: [
            ProblemaAleatorio_GPU_1,
            ProblemaAleatorio_GPU_2,
            ProblemaAleatorio_GPU_3,
            ProblemaAleatorio_GPU_4,
        ],
        ComponenteTematico.CPU: [
            ProblemaAleatorio_CPU_1,
            ProblemaAleatorio_CPU_2,
            ProblemaAleatorio_CPU_3,
            ProblemaAleatorio_CPU_4,
        ],
        ComponenteTematico.PANTALLA: [
            ProblemaAleatorio_PAN_1,
            ProblemaAleatorio_PAN_2,
            ProblemaAleatorio_PAN_3,
        ],
    }

    # ──────────────────────────────────────────────────────────────────────────

    @classmethod
    def obtener_aleatorio(cls) -> Problema:
        """Devuelve una instancia aleatoria de cualquier problema del catálogo."""
        componente = random.choice(list(cls._REGISTRO.keys()))
        clase = random.choice(cls._REGISTRO[componente])
        return clase()

    @classmethod
    def obtener_aleatorio_por_componente(cls, componente: ComponenteTematico) -> Problema:
        """Devuelve una instancia aleatoria de un problema del componente indicado."""
        if componente not in cls._REGISTRO:
            raise ValueError(
                f"Componente '{componente.value}' no tiene problemas aleatorios. "
                f"Disponibles: {[c.value for c in cls._REGISTRO]}"
            )
        clase = random.choice(cls._REGISTRO[componente])
        return clase()

    @classmethod
    def obtener_todos(cls) -> list[Problema]:
        """Devuelve una lista con una instancia de cada problema del catálogo."""
        resultado = []
        for clases in cls._REGISTRO.values():
            for clase in clases:
                resultado.append(clase())
        return resultado

    @classmethod
    def cantidad_total(cls) -> int:
        """Devuelve el número total de problemas aleatorios disponibles."""
        return sum(len(clases) for clases in cls._REGISTRO.values())

    @classmethod
    def componentes_disponibles(cls) -> list[ComponenteTematico]:
        """Devuelve los componentes que tienen problemas aleatorios registrados."""
        return list(cls._REGISTRO.keys())