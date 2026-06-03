"""
Catálogo de Problemas del Modo Historia
========================================
Cada nivel del modo historia presenta un problema concreto de hardware
(laptop o PC de escritorio) con sus pasos de reparación y desafíos asociados.

Niveles disponibles:
  1  – RAM dañada (Laptop)            → Reemplazo de módulo SO-DIMM DDR4
  2  – SSD con sectores dañados (PC)  → Reemplazo de SSD M.2 NVMe
  3  – Batería hinchada (Laptop)      → Reemplazo de batería Li-Ion
  4  – GPU sobrecalentada (PC)        → Reemplazo de GPU PCIe
  5  – CPU throttling (PC)            → Reemplazo de pasta térmica + CPU
  6  – Pantalla rota (Laptop)         → Reemplazo de panel IPS
  7  – RAM incompatible (PC)          → Upgrade de DDR4 a DDR5
  8  – SSD SATA lento (Laptop)        → Migración a NVMe
  9  – Batería agotada (Laptop)       → Diagnóstico y reemplazo avanzado
  10 – CPU socket dañado (PC)         → Diagnóstico y reemplazo avanzado

Uso:
    from problemas.catalogo_problemas_historia import CatalogoProblemasHistoria
    problema_nivel_1 = CatalogoProblemasHistoria.obtener_problema(nivel=1)
    todos = CatalogoProblemasHistoria.obtener_todos()
"""

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
#  Clases concretas de Problema por nivel
# ══════════════════════════════════════════════════════════════════════════════

class ProblemaNivel1_RAM_Laptop(Problema):
    """
    Nivel 1 – La laptop no arranca y emite pitidos POST.
    Diagnóstico: módulo RAM SO-DIMM DDR4 defectuoso.
    Solución: reemplazar por un módulo compatible.
    """

    def __init__(self):
        componente = RAM(
            nombre="RAM SO-DIMM DDR4 8 GB",
            capacidad_gb=8,
            velocidad_mhz=3200,
            generacion=GeneracionRAM.DDR4,
            formato=FormatoRAM.SO_DIMM,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Apagar la laptop y desconectar el cargador",
                explicacion=(
                    "Antes de tocar cualquier componente interno hay que cortar "
                    "toda fuente de energía para evitar descargas eléctricas."
                ),
                desafio=DesafioLogicoBooleano(
                    "¿Es obligatorio apagar y desenchufar la laptop antes de abrir el panel inferior?",
                    True, _GEN, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Retirar la batería interna",
                explicacion=(
                    "Aunque la laptop esté apagada, la batería puede suministrar "
                    "corriente residual; desconectarla es el segundo paso de seguridad."
                ),
                desafio=DesafioLogicoMultiple(
                    "¿Cuál es el segundo paso de seguridad antes de manipular la RAM?",
                    [
                        "Instalar el nuevo módulo directamente",
                        "Desconectar la batería interna",
                        "Formatear el disco duro",
                        "Actualizar el BIOS",
                    ],
                    1, _RAM, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Identificar el slot RAM defectuoso con prueba swap",
                explicacion=(
                    "Si hay 2 slots, retirar un módulo a la vez y encender para "
                    "identificar cuál causa los pitidos POST."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Los pitidos durante el POST pueden indicar un problema de RAM?",
                    True, _RAM, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Retirar el módulo defectuoso presionando las pestañas laterales",
                explicacion=(
                    "Las pestañas metálicas a ambos lados del slot se presionan "
                    "simultáneamente; el módulo salta a 45° y se extrae."
                ),
                desafio=DesafioLogicoMultiple(
                    "Al extraer un módulo SO-DIMM, ¿qué ángulo adopta al liberar las pestañas?",
                    ["90°", "45°", "180°", "30°"],
                    1, _RAM, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar el nuevo módulo DDR4 SO-DIMM",
                explicacion=(
                    "El módulo nuevo debe ser DDR4 SO-DIMM compatible. Se inserta "
                    "a 45° alineando la muesca y se presiona hasta que las pestañas hacen clic."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Un módulo DDR5 SO-DIMM puede instalarse en un slot DDR4 SO-DIMM?",
                    False, _RAM, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Verificar capacidad total de RAM reconocida por el sistema",
                explicacion=(
                    "Al encender, el POST o el SO deben reportar la nueva capacidad total."
                ),
                desafio=DesafioMatematicoEscritura(
                    "La laptop tenía 8 GB y se instaló un segundo módulo de 8 GB. "
                    "¿Cuántos GB en total reporta el sistema?",
                    16, _RAM, F,
                ),
            ),
        ]

        super().__init__(
            nombre="RAM defectuosa – Laptop no arranca",
            descripcion_email=(
                "Mi laptop emite pitidos al encender y no llega al sistema operativo. "
                "El técnico confirmó que uno de los módulos RAM SO-DIMM DDR4 está dañado."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel2_SSD_PC(Problema):
    """
    Nivel 2 – PC de escritorio con errores de lectura/escritura y pantallazos azules.
    Diagnóstico: SSD M.2 NVMe con sectores dañados (>30%).
    Solución: reemplazar por un SSD NVMe de mayor o igual capacidad.
    """

    def __init__(self):
        componente = SSD(
            modelo="Samsung 970 Evo 512 GB",
            capacidad_gb=512,
            interfaz=InterfazSSD.M2_NVME,
            velocidad_lectura_mbps=3500,
            velocidad_escritura_mbps=2300,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Apagar el PC y desconectar el cable de alimentación",
                explicacion="Siempre cortar la corriente antes de abrir el gabinete.",
                desafio=DesafioLogicoBooleano(
                    "¿Debe desconectarse el cable de alimentación antes de abrir el gabinete?",
                    True, _GEN, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Ejecutar diagnóstico de sectores dañados",
                explicacion=(
                    "Herramientas como CrystalDiskInfo muestran el porcentaje de sectores "
                    "dañados; si supera el 30% el SSD debe reemplazarse."
                ),
                desafio=DesafioMatematicoBooleano(
                    "¿Si el SSD tiene 35% de sectores dañados el sistema lo considera fuera de servicio?",
                    True, _SSD, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Localizar el slot M.2 en la placa base y retirar el tornillo de sujeción",
                explicacion=(
                    "El SSD M.2 se sujeta con un único tornillo en el extremo opuesto "
                    "al conector; sin retirarlo el módulo no puede extraerse."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Un SSD M.2 NVMe usa el bus PCIe para comunicarse con la CPU?",
                    True, _SSD, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Retirar el SSD dañado e instalar el nuevo",
                explicacion=(
                    "El nuevo SSD debe tener capacidad ≥ la del original; "
                    "un NVMe más lento puede instalarse pero limitará el rendimiento."
                ),
                desafio=DesafioLogicoMultiple(
                    "El técnico quiere instalar un SSD de 256 GB donde había uno de 512 GB dañado. ¿Qué ocurre?",
                    [
                        "Se instala sin problemas",
                        "El sistema rechaza por capacidad insuficiente",
                        "Funciona a la mitad de velocidad",
                        "El sistema lo acepta con advertencia de tamaño",
                    ],
                    1, _SSD, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular tiempo de copia de respaldo al nuevo SSD",
                explicacion=(
                    "Conocer la velocidad de escritura del SSD permite estimar "
                    "cuánto tardará la clonación o restauración de datos."
                ),
                desafio=DesafioMatematicoEscritura(
                    "El nuevo SSD escribe a 2300 MB/s. ¿Cuántos segundos tarda en escribir 11.5 GB?",
                    5, _SSD, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Verificar que el BIOS detecta el nuevo SSD",
                explicacion=(
                    "Entrar al BIOS/UEFI y confirmar que el nuevo dispositivo aparece "
                    "en la lista de almacenamiento antes de instalar el SO."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "¿Cuál es la interfaz más rápida para un SSD en un PC moderno?",
                    ["SATA III", "M.2 SATA", "M.2 NVMe PCIe 4.0", "USB 3.2"],
                    2, _SSD, F,
                ),
            ),
        ]

        super().__init__(
            nombre="SSD con sectores dañados – PC con pantallazos azules",
            descripcion_email=(
                "Mi PC de escritorio muestra pantallazos azules frecuentes y los archivos "
                "se corrompen. El diagnóstico indica que el SSD M.2 NVMe tiene más del 30% "
                "de sus sectores dañados y debe reemplazarse."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel3_Bateria_Laptop(Problema):
    """
    Nivel 3 – Laptop con batería hinchada que no carga y deforma el chasis.
    Diagnóstico: batería Li-Ion con salud <30% e hinchazón visible.
    Solución: reemplazo de batería con mismo voltaje y forma.
    """

    def __init__(self):
        componente = Bateria(
            voltaje_v=11.1,
            forma_bateria=FormaBateria.RECTANGULAR,
            capacidad_wh=54.0,
            salud=15,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Evaluar visualmente la batería para detectar hinchazón",
                explicacion=(
                    "Una batería hinchada es peligrosa (riesgo de incendio); "
                    "debe manipularse con precaución y no perforarla."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Una batería hinchada (swollen) es segura de seguir usando?",
                    False, _BAT, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Verificar el porcentaje de salud de la batería",
                explicacion=(
                    "Con software (BatteryInfoView, coconutBattery) se comprueba "
                    "la salud; bajo 30% el sistema la marca como fuera de servicio."
                ),
                desafio=DesafioMatematicoBooleano(
                    "¿Una batería con salud del 15% debe reemplazarse según los criterios del sistema?",
                    True, _BAT, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Desconectar el conector de la batería de la placa base",
                explicacion=(
                    "El conector tipo ZIF o JST debe desconectarse tirando del conector "
                    "y nunca del cable para no dañar los pines."
                ),
                desafio=DesafioLogicoMultiple(
                    "Al desconectar la batería de la placa, ¿de qué parte se debe tirar?",
                    ["Del cable directamente", "Del conector plástico", "Del cable y el conector a la vez", "No importa"],
                    1, _BAT, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar la batería de reemplazo con voltaje y forma correctos",
                explicacion=(
                    "El voltaje y la forma deben coincidir exactamente; "
                    "una batería de 12.6 V en lugar de 11.1 V puede dañar la placa."
                ),
                desafio=DesafioLogicoBooleano(
                    "¿Puede instalarse una batería de 12.6 V en un equipo diseñado para 11.1 V?",
                    False, _BAT, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular la nueva autonomía con la batería instalada",
                explicacion=(
                    "Con la capacidad nueva y el consumo conocido se estima la autonomía "
                    "real del equipo para validar la reparación."
                ),
                desafio=DesafioMatematicoEscritura(
                    "La nueva batería tiene 54 Wh y la laptop consume 18 W. ¿Cuántas horas de autonomía?",
                    3, _BAT, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Hacer un ciclo completo de carga y verificar la salud reportada",
                explicacion=(
                    "Cargar al 100% y descargar al 20% una vez calibra el indicador "
                    "del SO y permite confirmar que la nueva batería funciona correctamente."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "¿Qué indica el porcentaje de 'salud' de una batería?",
                    [
                        "El nivel de carga actual",
                        "La capacidad máxima restante respecto a la original",
                        "La temperatura de la batería",
                        "El voltaje instantáneo",
                    ],
                    1, _BAT, M,
                ),
            ),
        ]

        super().__init__(
            nombre="Batería hinchada – Laptop con chasis deformado",
            descripcion_email=(
                "Mi laptop ya no enciende con batería, el touchpad se levanta y hay "
                "una protuberancia visible bajo el chasis. La batería está hinchada "
                "y su salud es de apenas el 15%; necesita reemplazarse urgentemente."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel4_GPU_PC(Problema):
    """
    Nivel 4 – PC gamer con GPU PCIe que genera artefactos visuales y se apaga sola.
    Diagnóstico: GPU dedicada con fallo por sobrecalentamiento.
    Solución: reemplazar por GPU PCIe compatible.
    """

    def __init__(self):
        componente = GPU(
            modelo="RTX 3070",
            memoria_gb=8,
            tipo_memoria=TipoMemoriaGPU.GDDR6,
            tipo_gpu=TipoGPU.DEDICADA,
            interfaz=InterfazGPU.PCIE,
            tdp_watts=220,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Ejecutar stress-test de GPU para confirmar el fallo",
                explicacion=(
                    "Herramientas como FurMark generan carga máxima; si la GPU produce "
                    "artefactos o el sistema se cuelga, el hardware está fallando."
                ),
                desafio=DesafioLogicoMultiple(
                    "¿Qué herramienta es más adecuada para diagnosticar un fallo de GPU bajo carga?",
                    ["Multímetro en los pines PCIe", "Software de stress-test (FurMark)", "Observación visual", "Test de memoria RAM"],
                    1, _GPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Apagar el PC, desconectar la corriente y retirar la GPU",
                explicacion=(
                    "La GPU PCIe se fija con un tornillo en el bracket y una pestaña "
                    "de seguridad en el slot PCIe x16; ambos deben liberarse."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Las GPUs dedicadas de escritorio usan la interfaz PCIe x16?",
                    True, _GPU, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Seleccionar GPU de reemplazo compatible con el slot PCIe",
                explicacion=(
                    "La nueva GPU debe usar interfaz PCIe; si necesita conectores de "
                    "alimentación de 8-pin, la fuente debe tenerlos disponibles."
                ),
                desafio=DesafioLogicoBooleano(
                    "¿Una GPU PCIe puede reemplazarse en una PC de escritorio sin soldadura?",
                    True, _GPU, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular consumo total del sistema con la nueva GPU",
                explicacion=(
                    "La fuente de poder debe tener suficiente potencia para el nuevo TDP; "
                    "se suma el consumo de CPU + GPU + resto del sistema."
                ),
                desafio=DesafioMatematicoEscritura(
                    "La nueva GPU consume 250 W y la fuente tiene 750 W. "
                    "El resto del sistema usa 200 W. ¿Cuántos W libres quedan?",
                    300, _GPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar la nueva GPU y conectar los cables de alimentación PCIe",
                explicacion=(
                    "Insertar la GPU con firmeza hasta que la pestaña de seguridad "
                    "haga clic y conectar todos los cables de poder requeridos."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "¿Qué tipo de memoria usa una GPU de gama alta moderna?",
                    ["DDR4", "GDDR5", "GDDR6X", "SO-DIMM DDR5"],
                    2, _GPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar drivers y verificar temperatura bajo carga",
                explicacion=(
                    "Instalar los drivers oficiales y monitorear con GPU-Z / HWMonitor "
                    "que la temperatura bajo carga no supere los 85°C."
                ),
                desafio=DesafioMatematicoBooleano(
                    "Una GPU con TDP 300 W consume exactamente 300 W en todo momento. ¿Correcto?",
                    False, _GPU, M,
                ),
            ),
        ]

        super().__init__(
            nombre="GPU con artefactos – PC gamer con apagados repentinos",
            descripcion_email=(
                "Mi PC gamer muestra píxeles de colores aleatorios en pantalla y se apaga "
                "sola durante las partidas. La RTX 3070 está fallando por sobrecalentamiento "
                "y necesita reemplazarse por una GPU PCIe compatible."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel5_CPU_PC(Problema):
    """
    Nivel 5 – PC de escritorio con CPU en throttling severo y temperaturas de 100°C.
    Diagnóstico: pasta térmica seca + CPU con núcleos dañados.
    Solución: aplicar nueva pasta térmica; si persiste, reemplazar CPU.
    """

    def __init__(self):
        componente = CPU(
            modelo="Ryzen 5 5600X",
            nucleos=6,
            frecuencia_ghz=3.7,
            socket=SocketCPU.AM4,
            tdp_watts=65,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Monitorear temperaturas con HWMonitor bajo carga",
                explicacion=(
                    "Si la temperatura supera los 95°C el CPU hace throttling automático "
                    "reduciendo su frecuencia para protegerse."
                ),
                desafio=DesafioLogicoBooleano(
                    "¿Un CPU con sobrecalentamiento puede reducir su frecuencia automáticamente?",
                    True, _CPU, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Retirar el disipador y limpiar la pasta térmica vieja",
                explicacion=(
                    "La pasta envejecida pierde conductividad; se limpia con alcohol "
                    "isopropílico al 99% en ambas superficies (CPU y base del disipador)."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿La pasta térmica mejora la transferencia de calor entre el CPU y el disipador?",
                    True, _CPU, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Aplicar nueva pasta térmica y reinstalar el disipador",
                explicacion=(
                    "Se aplica una pequeña cantidad (tamaño de un guisante) en el centro "
                    "del IHS; el disipador la distribuirá al presionar."
                ),
                desafio=DesafioLogicoMultiple(
                    "Tras aplicar pasta nueva el CPU sigue a 100°C bajo carga leve. ¿Qué implica?",
                    [
                        "La pasta necesita más tiempo para curar",
                        "El problema es del SO, no del hardware",
                        "El CPU puede estar dañado y necesitar reemplazo",
                        "El disipador es decorativo",
                    ],
                    2, _CPU, D,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Verificar compatibilidad del CPU de reemplazo con el socket AM4",
                explicacion=(
                    "El socket AM4 es compatible con Ryzen 1000 a 5000; "
                    "un Ryzen 7000 usa AM5 y no encajará."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Un Ryzen 7000 puede instalarse en un socket AM4 sin adaptador?",
                    False, _CPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar el nuevo CPU en el socket AM4",
                explicacion=(
                    "Alinear la flecha del CPU con la del socket, bajar la palanca ZIF "
                    "y fijarla; nunca forzar el CPU si no cae por gravedad."
                ),
                desafio=DesafioMatematicoEscritura(
                    "El nuevo Ryzen 5 5600X tiene 6 núcleos con SMT. ¿Cuántos hilos lógicos expone al SO?",
                    12, _CPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular capacidad térmica disponible del disipador",
                explicacion=(
                    "El disipador debe soportar el TDP del nuevo CPU; "
                    "si el disipador soporta 125 W y el CPU tiene 65 W TDP, hay margen."
                ),
                desafio=DesafioLogicoEscritura(
                    "El CPU tiene TDP de 65 W y el disipador soporta 150 W. ¿Cuántos W de margen hay?",
                    85, _CPU, F,
                ),
            ),
        ]

        super().__init__(
            nombre="CPU en throttling – PC lenta con temperaturas críticas",
            descripcion_email=(
                "Mi PC de escritorio va muy lenta; el CPU Ryzen 5 5600X marca 100°C "
                "incluso en tareas simples y el sistema se congela. Primero se intentará "
                "reemplazar la pasta térmica; si falla el CPU, se instalará uno nuevo."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel6_Pantalla_Laptop(Problema):
    """
    Nivel 6 – Laptop con pantalla IPS rota tras caída.
    Diagnóstico: panel LCD físicamente quebrado con líneas de color.
    Solución: reemplazar por panel IPS de mismo tamaño.
    """

    def __init__(self):
        componente = Pantalla(
            pulgadas=15,
            resolucion="1920x1080",
            tipo_panel=TipoPanel.IPS,
            tasa_refresco_hz=60,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Confirmar que el daño es en el panel y no en el cable de video",
                explicacion=(
                    "Conectar un monitor externo; si la imagen sale bien, el problema "
                    "es el panel interno y no la GPU ni la placa base."
                ),
                desafio=DesafioLogicoBooleano(
                    "Si la laptop muestra imagen correcta en un monitor externo, ¿el problema es el panel interno?",
                    True, _PAN, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Conseguir panel IPS de 15\" de reemplazo con mismo conector",
                explicacion=(
                    "El panel debe coincidir en pulgadas y tipo de conector (30-pin o 40-pin EDP); "
                    "la resolución y Hz pueden variar si el conector es compatible."
                ),
                desafio=DesafioLogicoMultiple(
                    "¿Qué medida es OBLIGATORIA que coincida al reemplazar la pantalla de una laptop?",
                    ["La resolución exacta", "El tamaño en pulgadas", "La tasa de refresco", "El tipo de panel"],
                    1, _PAN, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Retirar la bisel y desmontar el panel roto",
                explicacion=(
                    "El bisel suele estar fijado con clips de plástico; se levanta con "
                    "una pala de plástico para no rayar. El panel va atornillado al marco."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "¿Qué ventaja tiene un panel IPS frente a uno TN?",
                    [
                        "Mayor tasa de refresco siempre",
                        "Mejores ángulos de visión y reproducción de color",
                        "Menor consumo eléctrico",
                        "Mayor brillo máximo siempre",
                    ],
                    1, _PAN, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Desconectar el cable EDP del panel roto",
                explicacion=(
                    "El cable EDP es muy delgado; tirar del conector con cuidado "
                    "usando una pinza de punta fina para no romper la cinta adhesiva."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Los paneles IPS tienen mejores ángulos de visión que los TN?",
                    True, _PAN, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar el nuevo panel y conectar el cable EDP",
                explicacion=(
                    "Conectar primero el cable EDP, verificar que encaja con un clic suave, "
                    "luego encender para probar antes de cerrar el bisel."
                ),
                desafio=DesafioMatematicoEscritura(
                    "El nuevo panel tiene resolución 1920×1080. ¿Cuántos píxeles totales tiene?",
                    2073600, _PAN, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Encender y verificar imagen sin líneas ni manchas",
                explicacion=(
                    "Ejecutar un test de píxeles muertos (pantalla completamente blanca, "
                    "roja, verde, azul, negra) para confirmar que el panel es correcto."
                ),
                desafio=DesafioMatematicoBooleano(
                    "¿Una pantalla de 60 Hz muestra 60 fotogramas por segundo como máximo?",
                    True, _PAN, F,
                ),
            ),
        ]

        super().__init__(
            nombre="Pantalla IPS rota – Laptop con líneas y manchas tras caída",
            descripcion_email=(
                "Mi laptop cayó al suelo y la pantalla muestra líneas de color y una "
                "mancha negra que crece. El panel IPS de 15\" está físicamente dañado "
                "y debe reemplazarse por uno compatible."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel7_RAM_Upgrade_PC(Problema):
    """
    Nivel 7 – PC de escritorio con 8 GB DDR4 insuficientes para cargas de trabajo modernas.
    Diagnóstico: RAM saturada (uso >95%) causando swapping constante.
    Solución: upgrade a 2 módulos DDR4 de 16 GB en dual channel.
    """

    def __init__(self):
        componente = RAM(
            nombre="RAM DIMM DDR4 8 GB",
            capacidad_gb=8,
            velocidad_mhz=2666,
            generacion=GeneracionRAM.DDR4,
            formato=FormatoRAM.DIMM,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Confirmar que la placa base soporta más RAM y velocidades",
                explicacion=(
                    "El manual de la placa indica la cantidad máxima de GB y las velocidades "
                    "DDR4 soportadas (XMP); instalar más de lo soportado impide el arranque."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Es necesario verificar la especificación de la placa antes de instalar más RAM?",
                    True, _RAM, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Planificar la configuración dual channel",
                explicacion=(
                    "Para dual channel los módulos deben instalarse en los slots emparejados "
                    "(generalmente A2 y B2 según el manual de la placa)."
                ),
                desafio=DesafioLogicoMultiple(
                    "¿En qué slots deben instalarse dos módulos para activar dual channel?",
                    [
                        "Slots 1 y 2 consecutivos siempre",
                        "Los slots del mismo color / slots emparejados (A2-B2)",
                        "Cualquier par de slots libres",
                        "Solo en el slot 1",
                    ],
                    1, _RAM, D,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular la nueva capacidad total tras el upgrade",
                explicacion=(
                    "Retirar el módulo de 8 GB e instalar 2 × 16 GB = 32 GB; "
                    "verificar que el SO reconoce la nueva capacidad."
                ),
                desafio=DesafioMatematicoEscritura(
                    "Se retira 1 módulo de 8 GB y se instalan 2 módulos de 16 GB. ¿Total de GB?",
                    32, _RAM, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar los módulos en los slots correctos para dual channel",
                explicacion=(
                    "Insertar cada módulo DIMM alineando la muesca y presionar uniformemente "
                    "hasta que las dos pestañas blancas hagan clic simultáneamente."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "¿Qué ventaja principal ofrece el modo dual channel?",
                    [
                        "Mayor capacidad de almacenamiento",
                        "Mayor ancho de banda de memoria",
                        "Menor consumo eléctrico",
                        "Compatibilidad con más CPUs",
                    ],
                    1, _RAM, D,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Activar perfil XMP en BIOS para velocidad correcta",
                explicacion=(
                    "Sin XMP la RAM corre a velocidad base (2133 MHz); activar XMP/DOCP "
                    "lleva los módulos a su velocidad nominal (ej. 3200 MHz)."
                ),
                desafio=DesafioMatematicoBooleano(
                    "DDR4 a 1600 MHz de reloj real equivale a 3200 MT/s efectivos. ¿Correcto?",
                    True, _RAM, D,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular el ancho de banda teórico en dual channel",
                explicacion=(
                    "Dual channel duplica el ancho de banda respecto a single channel; "
                    "es importante para cargas de trabajo con RAM intensiva."
                ),
                desafio=DesafioLogicoEscritura(
                    "En single channel el ancho de banda es 25 GB/s. ¿Cuánto entrega en dual channel?",
                    50, _RAM, D,
                ),
            ),
        ]

        super().__init__(
            nombre="RAM insuficiente – PC con swapping y lentitud extrema",
            descripcion_email=(
                "Mi PC de trabajo con 8 GB DDR4 se queda sin memoria con tres programas "
                "abiertos y el HDD/SSD trabaja constantemente haciendo swapping. "
                "Se planifica un upgrade a 32 GB en configuración dual channel."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel8_SSD_Laptop_Migracion(Problema):
    """
    Nivel 8 – Laptop con SSD SATA lento que limita la productividad.
    Diagnóstico: SSD SATA III de 128 GB casi lleno y velocidades de 400 MB/s.
    Solución: migrar a SSD M.2 NVMe de 512 GB.
    """

    def __init__(self):
        componente = SSD(
            modelo="Kingston A400 128 GB SATA",
            capacidad_gb=128,
            interfaz=InterfazSSD.M2_SATA,
            velocidad_lectura_mbps=500,
            velocidad_escritura_mbps=350,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Verificar si la laptop tiene slot M.2 NVMe disponible",
                explicacion=(
                    "Algunas laptops tienen dos slots M.2: uno SATA y otro NVMe. "
                    "Si solo hay uno, el SSD actual debe retirarse para instalar el NVMe."
                ),
                desafio=DesafioLogicoBooleano(
                    "¿Un SSD M.2 NVMe puede instalarse en un slot M.2 que solo soporta SATA?",
                    False, _SSD, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Clonar el SSD SATA al nuevo NVMe con software de clonación",
                explicacion=(
                    "Herramientas como Macrium Reflect o Clonezilla copian el SO y los "
                    "datos al nuevo SSD; el tiempo depende de la cantidad de datos."
                ),
                desafio=DesafioMatematicoEscritura(
                    "El SSD SATA actual tiene 100 GB de datos. Clonando a 350 MB/s de escritura, ¿cuántos segundos aproximados tarda?",
                    286, _SSD, D,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Retirar el SSD SATA e instalar el NVMe en el slot M.2",
                explicacion=(
                    "El M.2 NVMe se inserta a 30° en el slot, se baja y se asegura "
                    "con el tornillo M2×3 mm en el extremo del módulo."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "¿Qué protocolo de comunicación usa un SSD NVMe?",
                    ["AHCI sobre SATA", "NVMe sobre PCIe", "SCSI sobre USB", "IDE sobre PATA"],
                    1, _SSD, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Comparar las velocidades teóricas del nuevo SSD",
                explicacion=(
                    "El NVMe PCIe 3.0 alcanza ~3500 MB/s de lectura vs 500 MB/s del SATA; "
                    "eso se traduce en arranques y cargas de aplicaciones 5–7× más rápidos."
                ),
                desafio=DesafioMatematicoBooleano(
                    "Un SSD NVMe con 3500 MB/s de lectura es más rápido que un SATA con 550 MB/s. ¿Correcto?",
                    True, _SSD, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Arrancar desde el nuevo NVMe y validar el sistema",
                explicacion=(
                    "Configurar el orden de arranque en BIOS para que el NVMe sea el "
                    "primer dispositivo; verificar que el SO arranca correctamente."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Los SSDs no tienen partes móviles, lo que los hace más resistentes a golpes que los HDDs?",
                    True, _SSD, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular cuánto tiempo tarda en leer 7 GB con el nuevo NVMe",
                explicacion=(
                    "Con 3500 MB/s de lectura el nuevo SSD lee 7 GB en 2 segundos; "
                    "el SATA anterior tardaba más de 14 segundos para la misma operación."
                ),
                desafio=DesafioMatematicoEscritura(
                    "El nuevo NVMe lee a 3500 MB/s. ¿Cuántos segundos tarda en leer 7 GB?",
                    2, _SSD, F,
                ),
            ),
        ]

        super().__init__(
            nombre="SSD SATA lento – Migración a NVMe en laptop",
            descripcion_email=(
                "Mi laptop de trabajo tarda 2 minutos en arrancar y los programas "
                "se abren muy lento. El SSD SATA de 128 GB está casi lleno y su "
                "velocidad de 500 MB/s ya no es suficiente. Se migra a un NVMe de 512 GB."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel9_Bateria_Avanzado_Laptop(Problema):
    """
    Nivel 9 – Laptop con batería que se descarga al 0% en 20 minutos y apaga sola.
    Diagnóstico: batería Li-Ion con salud del 18% y voltaje irregular.
    Solución: diagnóstico avanzado + reemplazo de batería con forma en L.
    """

    def __init__(self):
        componente = Bateria(
            voltaje_v=11.4,
            forma_bateria=FormaBateria.FORMA_L,
            capacidad_wh=72.0,
            salud=18,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Medir el voltaje real de la batería con multímetro",
                explicacion=(
                    "Una batería de 11.4 V nominal que mide solo 8 V en reposo está "
                    "profundamente descargada o tiene celdas dañadas."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿El voltaje nominal de una celda de litio típica es de 3.7 V?",
                    True, _BAT, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Verificar la salud con software especializado (BatteryInfoView)",
                explicacion=(
                    "La salud del 18% indica que la batería retiene menos de 1/5 de "
                    "su capacidad original; el sistema la marca como no funcional."
                ),
                desafio=DesafioMatematicoEscritura(
                    "La batería original era de 72 Wh y tiene salud del 18%. ¿Cuántos Wh efectivos quedan?",
                    12, _BAT, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Identificar la forma especial FORMA_L del compartimento",
                explicacion=(
                    "Esta laptop tiene chasis delgado con batería en forma de L; "
                    "el reemplazo DEBE tener la misma forma para encajar en el chasis."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "Una batería con forma en 'L' corresponde al tipo:",
                    ["RECTANGULAR", "FORMA_L", "IRREGULAR", "CILÍNDRICA"],
                    1, _BAT, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Adquirir batería de reemplazo con igual voltaje y forma L",
                explicacion=(
                    "El voltaje debe coincidir exactamente (11.4 V); "
                    "la nueva capacidad puede ser igual o mayor si la forma encaja."
                ),
                desafio=DesafioLogicoBooleano(
                    "¿Puede instalarse una batería de voltaje diferente si tiene la misma forma?",
                    False, _BAT, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar la nueva batería y verificar conexión al BMS",
                explicacion=(
                    "El conector del BMS (Battery Management System) debe encajar "
                    "correctamente; un BMS roto impide la carga aunque la batería sea nueva."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿Las baterías modernas de laptop usan tecnología de Ion de Litio principalmente?",
                    True, _BAT, F,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular la nueva autonomía con la batería de reemplazo de 80 Wh",
                explicacion=(
                    "Con la nueva batería de 80 Wh y el consumo del sistema, "
                    "se puede estimar cuánto durará antes de necesitar el cargador."
                ),
                desafio=DesafioMatematicoEscritura(
                    "La nueva batería tiene 80 Wh y el sistema consume 20 W. ¿Cuántas horas de autonomía?",
                    4, _BAT, F,
                ),
            ),
        ]

        super().__init__(
            nombre="Batería agotada – Laptop que dura 20 minutos y apaga sola",
            descripcion_email=(
                "Mi laptop ultrafina se descarga en 20 minutos desde el 100% y se apaga "
                "de golpe al llegar al 5%. La batería con forma de L tiene una salud "
                "del 18% y voltaje irregular; necesita reemplazo urgente."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


class ProblemaNivel10_CPU_Socket_PC(Problema):
    """
    Nivel 10 – PC de escritorio con socket AM5 dañado tras instalación incorrecta.
    Diagnóstico: pines del socket LGA doblados; CPU no reconocida por el sistema.
    Solución: enderezar pines (si es posible) o reemplazar la placa base; instalar CPU.
    """

    def __init__(self):
        componente = CPU(
            modelo="Ryzen 7 7700X",
            nucleos=8,
            frecuencia_ghz=4.5,
            socket=SocketCPU.AM5,
            tdp_watts=105,
        )

        pasos = [
            PasoDeReparacion(
                descripcion_accion="Diagnosticar si el CPU es reconocido en el POST",
                explicacion=(
                    "Si la placa no pasa el POST y el LED de diagnóstico indica 'CPU', "
                    "el problema puede ser el socket dañado o el CPU incompatible."
                ),
                desafio=DesafioTecnologicoMultiple(
                    "¿Qué socket usan los procesadores Ryzen 7000 de AMD?",
                    ["AM4", "LGA1700", "LGA1200", "AM5"],
                    3, _CPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Inspeccionar visualmente los pines del socket AM5",
                explicacion=(
                    "Los sockets LGA tienen pines en la placa, no en el CPU; "
                    "un pin doblado puede causar fallo de contacto o cortocircuito."
                ),
                desafio=DesafioLogicoBooleano(
                    "¿En el socket AM5 (LGA), los pines están en la placa base y no en el CPU?",
                    True, _CPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Intentar enderezar los pines doblados con pinza de punta fina",
                explicacion=(
                    "Con mucha precaución y buena iluminación, un pin levemente doblado "
                    "puede recuperarse; si está roto el socket debe reemplazarse."
                ),
                desafio=DesafioLogicoMultiple(
                    "Si los pines del socket están rotos (no solo doblados), ¿cuál es la solución correcta?",
                    [
                        "Aplicar soldadura en el pin roto",
                        "Reemplazar la placa base completa",
                        "Continuar usando el equipo con el pin roto",
                        "Instalar un CPU de socket diferente",
                    ],
                    1, _CPU, D,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Instalar el CPU Ryzen 7 7700X en el socket AM5 reparado",
                explicacion=(
                    "Alinear el triángulo del CPU con el del socket, bajar la palanca "
                    "de retención; en AM5 el CPU cae por gravedad sin forzar."
                ),
                desafio=DesafioTecnologicoBooleano(
                    "¿El socket AM5 es compatible con CPUs Ryzen de la serie 1000-5000?",
                    False, _CPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular los hilos lógicos del nuevo CPU",
                explicacion=(
                    "El Ryzen 7 7700X tiene 8 núcleos físicos con SMT (Simultaneous "
                    "Multi-Threading), exponiendo 16 hilos lógicos al sistema operativo."
                ),
                desafio=DesafioMatematicoEscritura(
                    "El Ryzen 7 7700X tiene 8 núcleos con SMT (2 hilos por núcleo). ¿Cuántos hilos lógicos?",
                    16, _CPU, M,
                ),
            ),
            PasoDeReparacion(
                descripcion_accion="Calcular el consumo energético máximo en carga sostenida",
                explicacion=(
                    "El TDP de 105 W indica el consumo térmico de diseño; "
                    "con overboost el CPU puede superar eso temporalmente."
                ),
                desafio=DesafioMatematicoEscritura(
                    "El CPU consume 105 W durante 8 horas continuas. ¿Cuántos Wh consume?",
                    840, _CPU, M,
                ),
            ),
        ]

        super().__init__(
            nombre="Socket dañado – PC que no arranca tras mala instalación del CPU",
            descripcion_email=(
                "Mi PC no arranca y el LED de diagnóstico de la placa indica fallo de CPU. "
                "Al inspeccionar el socket AM5 se encontraron pines doblados tras una "
                "instalación incorrecta del Ryzen 7 7700X. Se repararán los pines y se "
                "reinstalará el CPU correctamente."
            ),
            componente_afectado=componente,
            pasos_reparacion=pasos,
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Clase catálogo – punto de acceso único
# ══════════════════════════════════════════════════════════════════════════════

class CatalogoProblemasHistoria:
    """
    Catálogo estático de los 10 niveles del Modo Historia.

    Uso:
        problema = CatalogoProblemasHistoria.obtener_problema(nivel=3)
        todos    = CatalogoProblemasHistoria.obtener_todos()
        total    = CatalogoProblemasHistoria.cantidad_niveles()
    """

    _NIVELES: dict[int, type] = {
        1:  ProblemaNivel1_RAM_Laptop,
        2:  ProblemaNivel2_SSD_PC,
        3:  ProblemaNivel3_Bateria_Laptop,
        4:  ProblemaNivel4_GPU_PC,
        5:  ProblemaNivel5_CPU_PC,
        6:  ProblemaNivel6_Pantalla_Laptop,
        7:  ProblemaNivel7_RAM_Upgrade_PC,
        8:  ProblemaNivel8_SSD_Laptop_Migracion,
        9:  ProblemaNivel9_Bateria_Avanzado_Laptop,
        10: ProblemaNivel10_CPU_Socket_PC,
    }

    @classmethod
    def obtener_problema(cls, nivel: int) -> Problema:
        """Devuelve una nueva instancia del problema correspondiente al nivel dado."""
        if nivel not in cls._NIVELES:
            raise ValueError(
                f"Nivel {nivel} no existe. Niveles válidos: {list(cls._NIVELES.keys())}"
            )
        return cls._NIVELES[nivel]()

    @classmethod
    def obtener_todos(cls) -> list[Problema]:
        """Devuelve una lista con una instancia de cada problema en orden de nivel."""
        return [cls._NIVELES[n]() for n in sorted(cls._NIVELES)]

    @classmethod
    def cantidad_niveles(cls) -> int:
        """Devuelve el número total de niveles disponibles."""
        return len(cls._NIVELES)