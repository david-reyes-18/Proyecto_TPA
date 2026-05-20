"""
Catálogo estático de ejercicios.

Cada ejercicio recibe explícitamente su NivelDificultad:
FACIL   → concepto directo, sin cálculo, dato único
MEDIA   → requiere relacionar dos conceptos o un cálculo simple
DIFICIL → cálculo compuesto, concepto técnico profundo o trampa conceptual

Convención de nombres de listas:
_<CAT>_<COMP>_<TIPO>_<NIV>
Ej: _MAT_CPU_BOOL_F  → Matemático / CPU / Booleano / Fácil
"""

from desafios.dificultad_desafio import NivelDificultad
from desafios.componente_tematico import ComponenteTematico
from desafios.categoria_desafio import CategoriaDesafio
from desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio

from desafios.desafio_matematico.desafio_matematico_booleano  import DesafioMatematicoBooleano
from desafios.desafio_matematico.desafio_matematico_multiple  import DesafioMatematicoMultiple
from desafios.desafio_matematico.desafio_matematico_escritura import DesafioMatematicoEscritura

from desafios.desafio_logico.desafio_logico_booleano   import DesafioLogicoBooleano
from desafios.desafio_logico.desafio_logico_multiple   import DesafioLogicoMultiple
from desafios.desafio_logico.desafio_logico_escritura  import DesafioLogicoEscritura

from desafios.desafio_tecnologico.desafio_tecnologico_booleano   import DesafioTecnologicoBooleano
from desafios.desafio_tecnologico.desafio_tecnologico_multiple   import DesafioTecnologicoMultiple
from desafios.desafio_tecnologico.desafio_tecnologico_escritura  import DesafioTecnologicoEscritura

F = NivelDificultad.FACIL
M = NivelDificultad.MEDIA
D = NivelDificultad.DIFICIL

_CPU = ComponenteTematico.CPU
_RAM = ComponenteTematico.RAM
_SSD = ComponenteTematico.SSD
_GPU = ComponenteTematico.GPU
_BAT = ComponenteTematico.BATERIA
_PAN = ComponenteTematico.PANTALLA
_GEN = ComponenteTematico.GENERAL


# ══════════════════════════════════════════════════════════════════════════════
#  CPU
# ══════════════════════════════════════════════════════════════════════════════

_MAT_CPU_BOOL = [
    DesafioMatematicoBooleano(
        "Un procesador a 3.5 GHz ejecuta 3 500 000 000 ciclos por segundo. ¿Correcto?",
        True, _CPU, F,
    ),
    DesafioMatematicoBooleano(
        "Un CPU de 4 núcleos con Hyper-Threading expone 8 hilos lógicos al SO. ¿Correcto?",
        True, _CPU, M,
    ),
    DesafioMatematicoBooleano(
        "Un CPU con TDP de 65 W consume exactamente 65 W en todo momento. ¿Verdadero?",
        False, _CPU, M,
    ),
    DesafioMatematicoBooleano(
        "Duplicar los núcleos siempre duplica el rendimiento de cualquier aplicación. ¿Correcto?",
        False, _CPU, D,
    ),
    DesafioMatematicoBooleano(
        "Un proceso de fabricación de 5 nm es más pequeño que uno de 7 nm. ¿Verdadero?",
        True, _CPU, F,
    ),
]

_MAT_CPU_MULT = [
    DesafioMatematicoMultiple(
        "Un CPU a 4.2 GHz ejecuta ¿cuántos ciclos de reloj por segundo?",
        ["420 000", "4 200 000", "4 200 000 000", "420 000 000"],
        2, _CPU, F,
    ),
    DesafioMatematicoMultiple(
        "Un CPU de 8 núcleos puede completar 1 tarea por núcleo por segundo. "
        "¿Cuántas tareas completa en 3 segundos?",
        ["8", "11", "24", "16"],
        2, _CPU, M,
    ),
    DesafioMatematicoMultiple(
        "Un CPU con TDP 125 W funciona 24 horas. ¿Cuántos Wh consume como máximo?",
        ["125 Wh", "1 500 Wh", "3 000 Wh", "2 400 Wh"],
        2, _CPU, M,
    ),
    DesafioMatematicoMultiple(
        "La latencia de caché L1 es 1 ns y la de RAM es 100 ns. "
        "¿Cuántas veces más rápida es la caché?",
        ["10 veces", "100 veces", "1 000 veces", "50 veces"],
        1, _CPU, D,
    ),
]

_MAT_CPU_ESC = [
    DesafioMatematicoEscritura(
        "Un CPU a 3.0 GHz, ¿cuántos millones de ciclos por segundo ejecuta?",
        3000, _CPU, F,
    ),
    DesafioMatematicoEscritura(
        "Un CPU de 6 núcleos con Hyper-Threading, ¿cuántos hilos lógicos expone al SO?",
        12, _CPU, M,
    ),
    DesafioMatematicoEscritura(
        "Si un proceso tarda 8 s en 1 núcleo, ¿cuántos segundos tardaría idealmente en 4 núcleos?",
        2, _CPU, M,
    ),
    DesafioMatematicoEscritura(
        "Un CPU opera a 2 500 MHz. Expresa esa frecuencia en GHz.",
        2.5, _CPU, D, tolerancia=0.01,
    ),
]

_LOG_CPU_BOOL = [
    DesafioLogicoBooleano(
        "Si el socket del CPU nuevo es diferente al de la placa base, ¿puede instalarse sin adaptador?",
        False, _CPU, F,
    ),
    DesafioLogicoBooleano(
        "La pasta térmica mejora la conductividad entre el CPU y el disipador. ¿Verdadero?",
        True, _CPU, F,
    ),
    DesafioLogicoBooleano(
        "Un CPU soldado (BGA) en una laptop puede reemplazarse sin equipo especializado. ¿Correcto?",
        False, _CPU, M,
    ),
    DesafioLogicoBooleano(
        "Si el CPU está sobrecalentado, el SO puede reducir su frecuencia automáticamente. ¿Verdadero?",
        True, _CPU, D,
    ),
]

_LOG_CPU_MULT = [
    DesafioLogicoMultiple(
        "El técnico va a reemplazar un CPU en una laptop. ¿Cuál es el primer paso lógico?",
        ["Instalar el nuevo CPU directamente",
        "Desconectar la batería primero",
        "Aplicar pasta térmica sin desmontar",
        "Encender el equipo para diagnosticar"],
        1, _CPU, F,
    ),
    DesafioLogicoMultiple(
        "Un CPU con socket AM4, ¿en qué placa base puede instalarse?",
        ["Placa con socket LGA1700",
        "Placa con socket AM5",
        "Placa con socket AM4",
        "Placa con socket BGA"],
        2, _CPU, M,
    ),
    DesafioLogicoMultiple(
        "Para diagnosticar si el CPU está fallando, ¿qué herramienta es más adecuada?",
        ["Multímetro en los pines del socket",
        "Software de prueba de estrés (stress test)",
        "Observar visualmente el CPU",
        "Medir el voltaje de la batería"],
        1, _CPU, D,
    ),
]

_LOG_CPU_ESC = [
    DesafioLogicoEscritura(
        "¿Qué tipo de socket usan los CPUs de laptop soldados a la placa? (sigla en mayúsculas)",
        "BGA", _CPU, F, ignorar_mayusculas=True,
    ),
    DesafioLogicoEscritura(
        "Si un CPU genera 95 W de calor y el disipador solo puede disipar 65 W, "
        "¿qué problema ocurrirá? Responde en una palabra.",
        "sobrecalentamiento", _CPU, D, ignorar_mayusculas=True,
    ),
]

_TEC_CPU_BOOL = [
    DesafioTecnologicoBooleano(
        "El socket LGA1700 de Intel es compatible con CPUs Ryzen de AMD. ¿Correcto?",
        False, _CPU, F,
    ),
    DesafioTecnologicoBooleano(
        "Hyper-Threading permite que un núcleo físico ejecute dos hilos simultáneamente. ¿Verdadero?",
        True, _CPU, M,
    ),
    DesafioTecnologicoBooleano(
        "Un Ryzen 7000 puede instalarse en una placa con socket AM4 sin adaptador. ¿Correcto?",
        False, _CPU, M,
    ),
    DesafioTecnologicoBooleano(
        "La caché L3 es más lenta que la L1 pero tiene mayor capacidad. ¿Verdadero?",
        True, _CPU, D,
    ),
]

_TEC_CPU_MULT = [
    DesafioTecnologicoMultiple(
        "¿Cuál de estos sockets es exclusivo de laptops (CPUs soldados)?",
        ["AM4", "LGA1700", "BGA", "AM5"],
        2, _CPU, F,
    ),
    DesafioTecnologicoMultiple(
        "¿Qué significa TDP en el contexto de un CPU?",
        ["Temperatura De Proceso",
        "Thermal Design Power (potencia de diseño térmico)",
        "Transferencia De Procesamiento",
        "Total De Pines"],
        1, _CPU, M,
    ),
    DesafioTecnologicoMultiple(
        "Los Ryzen 7000 de AMD utilizan el socket:",
        ["AM4", "LGA1700", "LGA1200", "AM5"],
        3, _CPU, M,
    ),
    DesafioTecnologicoMultiple(
        "¿Qué generación de Intel usa el socket LGA1700?",
        ["8ª–9ª gen", "10ª–11ª gen", "12ª–14ª gen", "6ª–7ª gen"],
        2, _CPU, D,
    ),
]

_TEC_CPU_ESC = [
    DesafioTecnologicoEscritura(
        "¿Cómo se llama la tecnología de Intel que permite 2 hilos por núcleo físico?",
        "Hyper-Threading", _CPU, F, ignorar_mayusculas=True,
    ),
    DesafioTecnologicoEscritura(
        "¿Qué socket usan los Ryzen 5000 de AMD para escritorio?",
        "AM4", _CPU, M, ignorar_mayusculas=True,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  RAM
# ══════════════════════════════════════════════════════════════════════════════

_MAT_RAM_BOOL = [
    DesafioMatematicoBooleano(
        "Dos módulos RAM de 8 GB en dual channel suman 16 GB de capacidad. ¿Correcto?",
        True, _RAM, F,
    ),
    DesafioMatematicoBooleano(
        "Una RAM de 3200 MHz transfiere exactamente 3 200 datos por segundo. ¿Verdadero?",
        False, _RAM, D,  # son 3 200 millones de transferencias por segundo
    ),
    DesafioMatematicoBooleano(
        "DDR5 tiene mayor ancho de banda que DDR4 a la misma frecuencia de reloj. ¿Correcto?",
        True, _RAM, M,
    ),
]

_MAT_RAM_MULT = [
    DesafioMatematicoMultiple(
        "Un equipo tiene 4 slots RAM, cada módulo es de 16 GB. ¿Cuánta RAM máxima puede tener?",
        ["32 GB", "48 GB", "64 GB", "128 GB"],
        2, _RAM, F,
    ),
    DesafioMatematicoMultiple(
        "RAM a 3200 MT/s con bus de 64 bits. El ancho de banda pico es aproximadamente:",
        ["12.8 GB/s", "25.6 GB/s", "6.4 GB/s", "51.2 GB/s"],
        1, _RAM, D,
    ),
    DesafioMatematicoMultiple(
        "Un sistema tiene 8 GB de RAM. El SO usa 2 GB y cada app usa 1.5 GB. "
        "¿Cuántas apps pueden abrirse simultáneamente?",
        ["3", "4", "5", "6"],
        1, _RAM, M,
    ),
]

_MAT_RAM_ESC = [
    DesafioMatematicoEscritura(
        "Un sistema tiene 2 módulos de 8 GB y 1 módulo de 16 GB. ¿Cuántos GB totales?",
        32, _RAM, F,
    ),
    DesafioMatematicoEscritura(
        "Si la RAM DDR4 opera a 1600 MHz de reloj real, ¿cuál es su velocidad efectiva en MT/s?",
        3200, _RAM, D,
    ),
]

_LOG_RAM_BOOL = [
    DesafioLogicoBooleano(
        "Si instalas un módulo DDR5 en una placa que solo soporta DDR4, ¿funcionará?",
        False, _RAM, F,
    ),
    DesafioLogicoBooleano(
        "La RAM SO-DIMM se usa principalmente en laptops. ¿Verdadero?",
        True, _RAM, F,
    ),
    DesafioLogicoBooleano(
        "La RAM LPDDR soldada en una laptop puede reemplazarse fácilmente por el usuario. ¿Correcto?",
        False, _RAM, M,
    ),
]

_LOG_RAM_MULT = [
    DesafioLogicoMultiple(
        "Un técnico instala un módulo DDR4 SO-DIMM en una placa que acepta DDR5 SO-DIMM. ¿Qué ocurre?",
        ["Funciona con velocidad reducida",
        "No encaja físicamente y no funciona",
        "Funciona normalmente",
        "El sistema lo detecta como DDR5"],
        1, _RAM, M,
    ),
    DesafioLogicoMultiple(
        "Para aprovechar el dual channel, los módulos RAM deben instalarse en:",
        ["Cualquier par de slots",
        "Los slots del mismo color / slots emparejados",
        "Siempre en los slots 1 y 2 consecutivos",
        "Un solo slot con el doble de capacidad"],
        1, _RAM, D,
    ),
]

_LOG_RAM_ESC = [
    DesafioLogicoEscritura(
        "¿Qué formato de RAM usan las laptops ultradelgadas soldada a la placa? (sigla)",
        "LPDDR", _RAM, F, ignorar_mayusculas=True,
    ),
]

_TEC_RAM_BOOL = [
    DesafioTecnologicoBooleano(
        "DDR significa Double Data Rate. ¿Correcto?",
        True, _RAM, F,
    ),
    DesafioTecnologicoBooleano(
        "Un módulo SO-DIMM tiene el mismo tamaño físico que un DIMM estándar. ¿Verdadero?",
        False, _RAM, F,
    ),
    DesafioTecnologicoBooleano(
        "La RAM DDR5 introduce dos canales independientes de 32 bits por módulo. ¿Correcto?",
        True, _RAM, D,
    ),
]

_TEC_RAM_MULT = [
    DesafioTecnologicoMultiple(
        "¿Qué formato de RAM se usa en PCs de escritorio convencionales?",
        ["SO-DIMM", "LPDDR", "DIMM", "MXM"],
        2, _RAM, F,
    ),
    DesafioTecnologicoMultiple(
        "¿Cuál generación de RAM es la más reciente de estas opciones?",
        ["DDR3", "DDR4", "LPDDR4X", "DDR5"],
        3, _RAM, M,
    ),
    DesafioTecnologicoMultiple(
        "¿Qué ventaja principal ofrece el modo dual channel?",
        ["Mayor capacidad de almacenamiento",
        "Mayor ancho de banda de memoria",
        "Menor consumo de energía",
        "Compatibilidad con más CPUs"],
        1, _RAM, D,
    ),
]

_TEC_RAM_ESC = [
    DesafioTecnologicoEscritura(
        "¿Qué significa la sigla DDR en memorias RAM?",
        "Double Data Rate", _RAM, F, ignorar_mayusculas=True,
    ),
    DesafioTecnologicoEscritura(
        "¿Qué generación de RAM usa la plataforma AM5 de AMD de forma nativa?",
        "DDR5", _RAM, M, ignorar_mayusculas=True,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  SSD
# ══════════════════════════════════════════════════════════════════════════════

_MAT_SSD_BOOL = [
    DesafioMatematicoBooleano(
        "Un SSD NVMe con 3500 MB/s de lectura es más rápido que un SSD SATA con 550 MB/s. ¿Correcto?",
        True, _SSD, F,
    ),
    DesafioMatematicoBooleano(
        "Copiar 7 GB a un SSD SATA de 500 MB/s tarda aproximadamente 14 segundos. ¿Verdadero?",
        True, _SSD, M,
    ),
    DesafioMatematicoBooleano(
        "Un SSD de 1 TB tiene exactamente 1 000 000 000 000 bytes según los fabricantes. ¿Correcto?",
        True, _SSD, D,
    ),
]

_MAT_SSD_MULT = [
    DesafioMatematicoMultiple(
        "Un SSD SATA transfiere a 550 MB/s. ¿Cuántos segundos tarda en copiar 2.75 GB?",
        ["2 s", "5 s", "10 s", "20 s"],
        1, _SSD, M,
    ),
    DesafioMatematicoMultiple(
        "Un SSD NVMe lee a 3000 MB/s. ¿Cuánto tiempo tarda en leer 9 GB?",
        ["1 s", "2 s", "3 s", "6 s"],
        2, _SSD, M,
    ),
    DesafioMatematicoMultiple(
        "Si un SSD tiene 30% de sectores dañados, ¿qué ocurre según el sistema?",
        ["Funciona con advertencia",
        "Se activa el modo de solo lectura",
        "Deja de funcionar (falla)",
        "Se repara automáticamente"],
        2, _SSD, F,
    ),
]

_MAT_SSD_ESC = [
    DesafioMatematicoEscritura(
        "Un SSD SATA escribe a 520 MB/s. ¿Cuántos segundos tarda en escribir 5.2 GB?",
        10, _SSD, M,
    ),
    DesafioMatematicoEscritura(
        "¿A qué porcentaje de sectores dañados el SSD deja de funcionar según el sistema?",
        30, _SSD, F,
    ),
]

_LOG_SSD_BOOL = [
    DesafioLogicoBooleano(
        "¿Se puede instalar un SSD M.2 NVMe en un slot M.2 que solo soporta SATA?",
        False, _SSD, M,
    ),
    DesafioLogicoBooleano(
        "Si un SSD está funcionando correctamente, ¿el sistema permite reemplazarlo?",
        False, _SSD, F,
    ),
    DesafioLogicoBooleano(
        "Un SSD con interfaz SATA puede conectarse a un slot M.2 si la placa tiene M.2 SATA. ¿Verdadero?",
        True, _SSD, D,
    ),
]

_LOG_SSD_MULT = [
    DesafioLogicoMultiple(
        "El SSD está dañado. El técnico quiere reemplazarlo por uno de menor capacidad. ¿Qué pasa?",
        ["Se instala normalmente",
        "El sistema rechaza por capacidad insuficiente",
        "Funciona a velocidad reducida",
"El sistema lo acepta con advertencia"],
        1, _SSD, M,
    ),
    DesafioLogicoMultiple(
        "Para verificar si un SSD está dañado, lo más lógico es:",
        ["Mirarlo visualmente",
        "Medir la temperatura con un termómetro",
        "Ejecutar un diagnóstico de sectores",
        "Pesar el dispositivo"],
        2, _SSD, F,
    ),
]

_LOG_SSD_ESC = [
    DesafioLogicoEscritura(
        "¿Qué interfaz de SSD ofrece mayor velocidad: SATA o NVMe?",
        "NVMe", _SSD, F, ignorar_mayusculas=True,
    ),
]

_TEC_SSD_BOOL = [
    DesafioTecnologicoBooleano(
        "NVMe utiliza el bus PCIe para comunicarse con la CPU. ¿Correcto?",
        True, _SSD, M,
    ),
    DesafioTecnologicoBooleano(
        "Un SSD SATA y un SSD M.2 NVMe tienen el mismo protocolo de comunicación. ¿Verdadero?",
        False, _SSD, M,
    ),
    DesafioTecnologicoBooleano(
        "Los SSDs no tienen partes móviles, lo que los hace más resistentes a golpes que los HDDs. ¿Correcto?",
        True, _SSD, F,
    ),
]

_TEC_SSD_MULT = [
    DesafioTecnologicoMultiple(
        "¿Cuál de estas interfaces SSD es la más rápida?",
        ["SATA III", "M.2 SATA", "M.2 NVMe PCIe 4.0", "USB 3.0"],
        2, _SSD, M,
    ),
    DesafioTecnologicoMultiple(
        "¿Qué significa NVMe?",
        ["Non-Volatile Memory Express",
        "New Volume Memory Extension",
        "Network Virtual Memory Engine",
        "Nano Volatile Module Express"],
        0, _SSD, D,
    ),
    DesafioTecnologicoMultiple(
        "¿Cuál es la velocidad máxima aproximada de un SSD SATA III?",
        ["200 MB/s", "550 MB/s", "3 500 MB/s", "7 000 MB/s"],
        1, _SSD, F,
    ),
]

_TEC_SSD_ESC = [
    DesafioTecnologicoEscritura(
        "¿Qué sigla identifica la interfaz más rápida para SSDs en formato M.2?",
        "NVMe", _SSD, F, ignorar_mayusculas=True,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  GPU
# ══════════════════════════════════════════════════════════════════════════════

_MAT_GPU_BOOL = [
    DesafioMatematicoBooleano(
        "Una GPU con 8 GB GDDR6 tiene más VRAM que una con 6 GB GDDR6X. ¿Correcto?",
        True, _GPU, F,
    ),
    DesafioMatematicoBooleano(
        "Una GPU con TDP 300 W siempre rinde mejor que una con TDP 250 W. ¿Verdadero?",
        False, _GPU, M,
    ),
    DesafioMatematicoBooleano(
        "El ancho de banda de memoria de una GPU afecta su rendimiento en texturas. ¿Correcto?",
        True, _GPU, D,
    ),
]

_MAT_GPU_MULT = [
    DesafioMatematicoMultiple(
        "Una GPU con TDP 350 W funciona 8 horas al día. ¿Cuántos kWh consume?",
        ["2.4 kWh", "2.8 kWh", "3.5 kWh", "4.2 kWh"],
        1, _GPU, M,
    ),
    DesafioMatematicoMultiple(
        "Una GPU tiene bus de 256 bits y opera a 2000 MHz GDDR6. "
        "El ancho de banda aproximado es:",
        ["32 GB/s", "64 GB/s", "128 GB/s", "256 GB/s"],
        2, _GPU, D,
    ),
]

_MAT_GPU_ESC = [
    DesafioMatematicoEscritura(
        "Una GPU con TDP de 200 W funciona 5 horas. ¿Cuántos Wh consume?",
        1000, _GPU, M,
    ),
]

_LOG_GPU_BOOL = [
    DesafioLogicoBooleano(
        "Una GPU integrada comparte la RAM del sistema en lugar de tener VRAM dedicada. ¿Correcto?",
        True, _GPU, F,
    ),
    DesafioLogicoBooleano(
        "Si la GPU está funcionando correctamente, ¿el sistema permite reemplazarla?",
        False, _GPU, F,
    ),
    DesafioLogicoBooleano(
        "Una GPU dedicada PCIe puede reemplazarse en una PC de escritorio si está dañada. ¿Correcto?",
        True, _GPU, M,
    ),
    DesafioLogicoBooleano(
        "Una GPU con interfaz MXM en laptop puede reemplazarse por el usuario sin soldadura. ¿Verdadero?",
        False, _GPU, D,
    ),
]

_LOG_GPU_MULT = [
    DesafioLogicoMultiple(
        "El usuario tiene una laptop con GPU dedicada MXM que falla. ¿Cuál es la acción correcta?",
        ["Reemplazarla por cuenta propia",
        "Llevarla a un técnico especializado con equipo de soldadura",
        "Instalar una GPU PCIe externa",
        "Formatear el sistema operativo"],
        1, _GPU, M,
    ),
    DesafioLogicoMultiple(
        "Para que una GPU nueva sea compatible con la placa base, deben coincidir:",
        ["El modelo exacto de la GPU",
        "La interfaz (PCIe, MXM, etc.)",
        "La marca del fabricante",
        "El color del PCB"],
        1, _GPU, D,
    ),
]

_LOG_GPU_ESC = [
    DesafioLogicoEscritura(
        "¿Qué tipo de GPU usa la RAM del sistema en lugar de VRAM dedicada? (una palabra)",
        "integrada", _GPU, F, ignorar_mayusculas=True,
    ),
]

_TEC_GPU_BOOL = [
    DesafioTecnologicoBooleano(
        "GDDR6X es un tipo de memoria más rápida que GDDR6. ¿Correcto?",
        True, _GPU, M,
    ),
    DesafioTecnologicoBooleano(
        "Una GPU integrada tiene su propio banco de memoria física separada de la RAM. ¿Verdadero?",
        False, _GPU, M,
    ),
    DesafioTecnologicoBooleano(
        "PCIe x16 es la interfaz estándar para GPUs dedicadas en PCs de escritorio. ¿Correcto?",
        True, _GPU, F,
    ),
]

_TEC_GPU_MULT = [
    DesafioTecnologicoMultiple(
        "¿Qué interfaz usan las GPUs dedicadas en PCs de escritorio?",
        ["MXM", "SATA", "PCIe x16", "USB4"],
        2, _GPU, F,
    ),
    DesafioTecnologicoMultiple(
        "¿Cuál de estos tipos de memoria GPU tiene mayor ancho de banda?",
        ["GDDR5", "GDDR6", "GDDR6X", "DDR4"],
        2, _GPU, M,
    ),
    DesafioTecnologicoMultiple(
        "¿Qué significa iGPU?",
        ["GPU industrial",
        "GPU integrada en el procesador",
        "GPU independiente",
        "GPU inteligente"],
        1, _GPU, D,
    ),
]

_TEC_GPU_ESC = [
    DesafioTecnologicoEscritura(
        "¿Cómo se llama la memoria dedicada de una GPU? (sigla de 4 letras)",
        "VRAM", _GPU, F, ignorar_mayusculas=True,
    ),
    DesafioTecnologicoEscritura(
        "¿Qué interfaz usan laptops de gama alta con GPU dedicada soldada a la placa? (una palabra)",
        "SOLDADA", _GPU, D, ignorar_mayusculas=True,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  BATERÍA
# ══════════════════════════════════════════════════════════════════════════════

_MAT_BAT_BOOL = [
    DesafioMatematicoBooleano(
        "Una batería de 72 Wh dura el doble que una de 36 Wh en las mismas condiciones. ¿Correcto?",
        True, _BAT, F,
    ),
    DesafioMatematicoBooleano(
        "Si el sistema consume 18 W y la batería tiene 54 Wh, ¿dura exactamente 3 horas?",
        True, _BAT, M,
    ),
    DesafioMatematicoBooleano(
        "Una batería con salud del 25% puede reemplazarse según el sistema del juego. ¿Correcto?",
        True, _BAT, D,
    ),
]

_MAT_BAT_MULT = [
    DesafioMatematicoMultiple(
        "Una laptop consume 15 W y su batería tiene 60 Wh. ¿Cuántas horas de autonomía tiene?",
        ["2 h", "3 h", "4 h", "5 h"],
        2, _BAT, F,
    ),
    DesafioMatematicoMultiple(
        "Una batería de 11.1 V y 4400 mAh tiene una capacidad aproximada en Wh de:",
        ["24 Wh", "35 Wh", "49 Wh", "60 Wh"],
        2, _BAT, D,
    ),
    DesafioMatematicoMultiple(
        "Si una batería tiene salud del 60%, su capacidad efectiva de 80 Wh originales es:",
        ["32 Wh", "40 Wh", "48 Wh", "60 Wh"],
        2, _BAT, M,
    ),
]

_MAT_BAT_ESC = [
    DesafioMatematicoEscritura(
        "Una laptop usa 20 W y la batería tiene 100 Wh. ¿Cuántas horas dura?",
        5, _BAT, F,
    ),
    DesafioMatematicoEscritura(
        "¿Por debajo de qué porcentaje de salud el sistema considera la batería dañada?",
        30, _BAT, M,
    ),
]

_LOG_BAT_BOOL = [
    DesafioLogicoBooleano(
        "Antes de reemplazar la batería de una laptop, ¿se debe desconectar primero?",
        True, _BAT, F,
    ),
    DesafioLogicoBooleano(
        "¿Puede instalarse una batería de voltaje diferente si tiene la misma forma?",
        False, _BAT, M,
    ),
    DesafioLogicoBooleano(
        "Una batería con salud al 15% puede usarse indefinidamente sin riesgo. ¿Correcto?",
        False, _BAT, F,
    ),
]

_LOG_BAT_MULT = [
    DesafioLogicoMultiple(
        "El técnico quiere instalar una batería de 12.6 V en un equipo que usa 11.1 V. ¿Resultado?",
        ["Funciona normalmente",
         "El sistema rechaza por voltaje incorrecto",
         "Funciona con velocidad reducida",
         "El sistema la acepta con advertencia"],
        1, _BAT, M,
    ),
    DesafioLogicoMultiple(
        "¿Qué parámetros deben coincidir obligatoriamente al reemplazar una batería?",
        ["Solo la capacidad en Wh",
         "Voltaje y forma de la batería",
         "Solo el voltaje",
         "Marca y modelo exacto"],
        1, _BAT, D,
    ),
]

_LOG_BAT_ESC = [
    DesafioLogicoEscritura(
        "¿Qué debe hacer el técnico ANTES de desmontar la batería? (una palabra)",
        "desconectar", _BAT, F, ignorar_mayusculas=True,
    ),
]

_TEC_BAT_BOOL = [
    DesafioTecnologicoBooleano(
        "Las baterías de laptop modernas son mayormente de Ion de Litio. ¿Correcto?",
        True, _BAT, F,
    ),
    DesafioTecnologicoBooleano(
        "El voltaje nominal de una celda de litio típica es de 3.7 V. ¿Verdadero?",
        True, _BAT, M,
    ),
    DesafioTecnologicoBooleano(
        "Una batería hinchada (swollen) es segura de continuar usando. ¿Correcto?",
        False, _BAT, F,
    ),
]

_TEC_BAT_MULT = [
    DesafioTecnologicoMultiple(
        "¿Qué unidad se usa para medir la capacidad de energía de una batería de laptop?",
        ["mAh únicamente", "Voltios (V)", "Watt-hora (Wh)", "Amperios (A)"],
        2, _BAT, F,
    ),
    DesafioTecnologicoMultiple(
        "Una batería de laptop con forma en 'L' es de tipo:",
        ["RECTANGULAR", "FORMA_L", "IRREGULAR", "CILÍNDRICA"],
        1, _BAT, M,
    ),
    DesafioTecnologicoMultiple(
        "¿Qué indica el porcentaje de 'salud' de una batería?",
        ["El nivel de carga actual",
         "La capacidad máxima restante vs. capacidad original",
         "La temperatura de la batería",
         "El voltaje actual"],
        1, _BAT, D,
    ),
]

_TEC_BAT_ESC = [
    DesafioTecnologicoEscritura(
        "¿Qué tecnología de batería se usa en la mayoría de laptops modernas? (Ion de ...)",
        "Ion de Litio", _BAT, M, ignorar_mayusculas=True,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA
# ══════════════════════════════════════════════════════════════════════════════

_MAT_PAN_BOOL = [
    DesafioMatematicoBooleano(
        "Una pantalla 1920×1080 tiene más píxeles que una 1280×720. ¿Correcto?",
        True, _PAN, F,
    ),
    DesafioMatematicoBooleano(
        "Una tasa de refresco de 144 Hz produce más fotogramas por segundo que 60 Hz. ¿Verdadero?",
        True, _PAN, F,
    ),
    DesafioMatematicoBooleano(
        "Una pantalla de 15\" puede reemplazarse por una de 17\" en la misma laptop. ¿Correcto?",
        False, _PAN, M,
    ),
]

_MAT_PAN_MULT = [
    DesafioMatematicoMultiple(
        "¿Cuántos píxeles totales tiene una resolución 1920×1080?",
        ["1 036 800", "2 073 600", "4 147 200", "921 600"],
        1, _PAN, M,
    ),
    DesafioMatematicoMultiple(
        "Una pantalla de 60 Hz muestra un nuevo fotograma cada:",
        ["8.3 ms", "16.7 ms", "33.3 ms", "1 ms"],
        1, _PAN, D,
    ),
    DesafioMatematicoMultiple(
        "¿Cuántos fotogramas por segundo puede mostrar una pantalla de 144 Hz?",
        ["60", "120", "144", "240"],
        2, _PAN, F,
    ),
]

_MAT_PAN_ESC = [
    DesafioMatematicoEscritura(
        "Una pantalla de 60 Hz muestra ¿cuántos fotogramas por segundo?",
        60, _PAN, F,
    ),
    DesafioMatematicoEscritura(
        "¿Cuántos píxeles tiene una pantalla 2560×1440? (en millones, con 1 decimal)",
        3.7, _PAN, D, tolerancia=0.1,
    ),
]

_LOG_PAN_BOOL = [
    DesafioLogicoBooleano(
        "Si la pantalla de una laptop está rota, ¿el sistema permite reemplazarla?",
        True, _PAN, F,
    ),
    DesafioLogicoBooleano(
        "¿Puede instalarse una pantalla de 17\" en un chasis diseñado para 15\"?",
        False, _PAN, F,
    ),
    DesafioLogicoBooleano(
        "Una pantalla IPS tiene mejores ángulos de visión que una TN. ¿Correcto?",
        True, _PAN, M,
    ),
]

_LOG_PAN_MULT = [
    DesafioLogicoMultiple(
        "Al reemplazar la pantalla de una laptop, ¿qué medida debe coincidir obligatoriamente?",
        ["La resolución exacta",
         "El tamaño en pulgadas",
         "La tasa de refresco",
         "El tipo de panel"],
        1, _PAN, M,
    ),
    DesafioLogicoMultiple(
        "¿Para qué tipo de usuario es más recomendable un panel OLED?",
        ["Trabajo de oficina básico con presupuesto ajustado",
         "Gaming de entrada sin importar calidad de imagen",
         "Edición de color profesional y multimedia premium",
         "Uso exclusivo en entornos muy iluminados"],
        2, _PAN, D,
    ),
]

_LOG_PAN_ESC = [
    DesafioLogicoEscritura(
        "¿Qué tipo de panel apaga píxeles individualmente para lograr negros perfectos?",
        "OLED", _PAN, M, ignorar_mayusculas=True,
    ),
]

_TEC_PAN_BOOL = [
    DesafioTecnologicoBooleano(
        "Los paneles TN tienen tiempos de respuesta más rápidos que los IPS en general. ¿Correcto?",
        True, _PAN, M,
    ),
    DesafioTecnologicoBooleano(
        "Los paneles VA ofrecen mejor contraste que los IPS. ¿Verdadero?",
        True, _PAN, D,
    ),
    DesafioTecnologicoBooleano(
        "Los paneles OLED usan retroiluminación LED igual que los LCD. ¿Correcto?",
        False, _PAN, D,
    ),
]

_TEC_PAN_MULT = [
    DesafioTecnologicoMultiple(
        "¿Qué tipo de panel es más común en laptops gaming de entrada por rapidez y bajo costo?",
        ["IPS", "VA", "OLED", "TN"],
        3, _PAN, M,
    ),
    DesafioTecnologicoMultiple(
        "¿Qué ventaja principal tiene un panel IPS frente a un TN?",
        ["Mayor tasa de refresco máxima",
         "Mejor ángulo de visión y reproducción de color",
         "Menor tiempo de respuesta siempre",
         "Menor consumo eléctrico"],
        1, _PAN, M,
    ),
    DesafioTecnologicoMultiple(
        "¿Cuál es la resolución conocida como Full HD?",
        ["1280×720", "1920×1080", "2560×1440", "3840×2160"],
        1, _PAN, F,
    ),
]

_TEC_PAN_ESC = [
    DesafioTecnologicoEscritura(
        "¿Cómo se llama la resolución 3840×2160? (sigla de 2 caracteres)",
        "4K", _PAN, F, ignorar_mayusculas=True,
    ),
    DesafioTecnologicoEscritura(
        "¿Qué tipo de panel se usa en workstations por colores precisos y amplios ángulos? (sigla)",
        "IPS", _PAN, M, ignorar_mayusculas=True,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  GENERAL
# ══════════════════════════════════════════════════════════════════════════════

_MAT_GEN_BOOL = [
    DesafioMatematicoBooleano(
        "1 GB equivale exactamente a 1 000 MB en el sistema binario. ¿Correcto?",
        False, _GEN, D,
    ),
    DesafioMatematicoBooleano(
        "Un equipo con 16 GB de RAM y 512 GB de SSD tiene más almacenamiento que memoria. ¿Verdadero?",
        True, _GEN, F,
    ),
]

_TEC_GEN_BOOL = [
    DesafioTecnologicoBooleano(
        "PCIe 4.0 ofrece el doble de ancho de banda que PCIe 3.0. ¿Correcto?",
        True, _GEN, M,
    ),
    DesafioTecnologicoBooleano(
        "USB4 y Thunderbolt 4 comparten la misma especificación base. ¿Verdadero?",
        True, _GEN, D,
    ),
]

_LOG_GEN_MULT = [
    DesafioLogicoMultiple(
        "Antes de abrir cualquier equipo electrónico para repararlo, ¿qué debe hacerse primero?",
        ["Encender el equipo para diagnosticar",
         "Apagar y desenchufar / desconectar la batería",
         "Instalar el componente nuevo directamente",
         "Formatear el sistema operativo"],
        1, _GEN, F,
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  ÍNDICE MAESTRO
#  { ComponenteTematico → { CategoriaDesafio → { NombreTipoDesafio → [lista] } } }
# ══════════════════════════════════════════════════════════════════════════════

CATALOGO: dict = {
    _CPU: {
        CategoriaDesafio.MATEMATICO:  {NombreTipoDesafio.BOOLEANO: _MAT_CPU_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _MAT_CPU_MULT,
                                       NombreTipoDesafio.ESCRITURA: _MAT_CPU_ESC},
        CategoriaDesafio.LOGICO:      {NombreTipoDesafio.BOOLEANO: _LOG_CPU_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _LOG_CPU_MULT,
                                       NombreTipoDesafio.ESCRITURA: _LOG_CPU_ESC},
        CategoriaDesafio.TECNOLOGICO: {NombreTipoDesafio.BOOLEANO: _TEC_CPU_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _TEC_CPU_MULT,
                                       NombreTipoDesafio.ESCRITURA: _TEC_CPU_ESC},
    },
    _RAM: {
        CategoriaDesafio.MATEMATICO:  {NombreTipoDesafio.BOOLEANO: _MAT_RAM_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _MAT_RAM_MULT,
                                       NombreTipoDesafio.ESCRITURA: _MAT_RAM_ESC},
        CategoriaDesafio.LOGICO:      {NombreTipoDesafio.BOOLEANO: _LOG_RAM_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _LOG_RAM_MULT,
                                       NombreTipoDesafio.ESCRITURA: _LOG_RAM_ESC},
        CategoriaDesafio.TECNOLOGICO: {NombreTipoDesafio.BOOLEANO: _TEC_RAM_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _TEC_RAM_MULT,
                                       NombreTipoDesafio.ESCRITURA: _TEC_RAM_ESC},
    },
    _SSD: {
        CategoriaDesafio.MATEMATICO:  {NombreTipoDesafio.BOOLEANO: _MAT_SSD_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _MAT_SSD_MULT,
                                       NombreTipoDesafio.ESCRITURA: _MAT_SSD_ESC},
        CategoriaDesafio.LOGICO:      {NombreTipoDesafio.BOOLEANO: _LOG_SSD_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _LOG_SSD_MULT,
                                       NombreTipoDesafio.ESCRITURA: _LOG_SSD_ESC},
        CategoriaDesafio.TECNOLOGICO: {NombreTipoDesafio.BOOLEANO: _TEC_SSD_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _TEC_SSD_MULT,
                                       NombreTipoDesafio.ESCRITURA: _TEC_SSD_ESC},
    },
    _GPU: {
        CategoriaDesafio.MATEMATICO:  {NombreTipoDesafio.BOOLEANO: _MAT_GPU_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _MAT_GPU_MULT,
                                       NombreTipoDesafio.ESCRITURA: _MAT_GPU_ESC},
        CategoriaDesafio.LOGICO:      {NombreTipoDesafio.BOOLEANO: _LOG_GPU_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _LOG_GPU_MULT,
                                       NombreTipoDesafio.ESCRITURA: _LOG_GPU_ESC},
        CategoriaDesafio.TECNOLOGICO: {NombreTipoDesafio.BOOLEANO: _TEC_GPU_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _TEC_GPU_MULT,
                                       NombreTipoDesafio.ESCRITURA: _TEC_GPU_ESC},
    },
    _BAT: {
        CategoriaDesafio.MATEMATICO:  {NombreTipoDesafio.BOOLEANO: _MAT_BAT_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _MAT_BAT_MULT,
                                       NombreTipoDesafio.ESCRITURA: _MAT_BAT_ESC},
        CategoriaDesafio.LOGICO:      {NombreTipoDesafio.BOOLEANO: _LOG_BAT_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _LOG_BAT_MULT,
                                       NombreTipoDesafio.ESCRITURA: _LOG_BAT_ESC},
        CategoriaDesafio.TECNOLOGICO: {NombreTipoDesafio.BOOLEANO: _TEC_BAT_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _TEC_BAT_MULT,
                                       NombreTipoDesafio.ESCRITURA: _TEC_BAT_ESC},
    },
    _PAN: {
        CategoriaDesafio.MATEMATICO:  {NombreTipoDesafio.BOOLEANO: _MAT_PAN_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _MAT_PAN_MULT,
                                       NombreTipoDesafio.ESCRITURA: _MAT_PAN_ESC},
        CategoriaDesafio.LOGICO:      {NombreTipoDesafio.BOOLEANO: _LOG_PAN_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _LOG_PAN_MULT,
                                       NombreTipoDesafio.ESCRITURA: _LOG_PAN_ESC},
        CategoriaDesafio.TECNOLOGICO: {NombreTipoDesafio.BOOLEANO: _TEC_PAN_BOOL,
                                       NombreTipoDesafio.MULTIPLE: _TEC_PAN_MULT,
                                       NombreTipoDesafio.ESCRITURA: _TEC_PAN_ESC},
    },
    _GEN: {
        CategoriaDesafio.MATEMATICO:  {NombreTipoDesafio.BOOLEANO: _MAT_GEN_BOOL,
                                       NombreTipoDesafio.MULTIPLE: [],
                                       NombreTipoDesafio.ESCRITURA: []},
        CategoriaDesafio.LOGICO:      {NombreTipoDesafio.BOOLEANO: [],
                                       NombreTipoDesafio.MULTIPLE: _LOG_GEN_MULT,
                                       NombreTipoDesafio.ESCRITURA: []},
        CategoriaDesafio.TECNOLOGICO: {NombreTipoDesafio.BOOLEANO: _TEC_GEN_BOOL,
                                       NombreTipoDesafio.MULTIPLE: [],
                                       NombreTipoDesafio.ESCRITURA: []},
    },
}