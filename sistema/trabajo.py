"""
Sistema de trabajos y correos para el modo historia
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from dominio.entidades.problemas.problema import Problema
from dominio.entidades.dispositivos.laptop import Laptop
from fabricas.dispositivos.fabrica_laptop import FabricaLaptop


if TYPE_CHECKING:
    from core.juego import Juego


class Trabajo:
    """
    Representa un trabajo de reparación que llega por correo electrónico
    """

    def __init__(self, problema: Problema, recompensa_dinero: int = 100,
                recompensa_experiencia: int = 50):
        self.problema = problema
        self.recompensa_dinero = recompensa_dinero
        self.recompensa_experiencia = recompensa_experiencia
        self.aceptado = False
        self.completado = False

    def get_descripcion_email(self) -> str:
        """Returns the email description for this trabajo"""
        return self.problema.descripcion_email

    def get_asunto_email(self) -> str:
        """Returns the email subject for this trabajo"""
        return f"Trabajo de reparación: {self.problema.nombre}"

    def aceptar(self, juego: 'Juego') -> Laptop | None:
        """
        Acepta el trabajo y crea la laptop correspondiente
        Returns: La laptop creada para reparar, o None si ya fue aceptado
        """
        if self.aceptado:
            return None

        self.aceptado = True

        # Crear la laptop usando la fábrica apropiada según el tipo de problema
        fabrica = FabricaLaptop()

        # Determinar el tipo de laptop basado en el problema
        if "Laptop" in self.problema.nombre:
            # Es una laptop, usar fábrica básica/intermedia/gamer según la complejidad
            if any(dificultad in self.problema.nombre.lower() for dificultad in ["avanzado", "socket"]):
                laptop = fabrica.crear_dispositivo_gamer(self.problema)
            elif any(dificultad in self.problema.nombre.lower() for dificultad in ["upgrade", "migracion"]):
                laptop = fabrica.crear_dispositivo_intermedio(self.problema)
            else:
                laptop = fabrica.crear_dispositivo_basico(self.problema)
        else:
            # Para PCs de escritorio, por ahora retornamos None (implementar después si se necesita)
            return None

        return laptop

    def completar(self):
        """Marca el trabajo como completado"""
        self.completado = True

    def __str__(self) -> str:
        estado = "Aceptado" if self.aceptado else "Pendiente"
        if self.completado:
            estado = "Completado"
        return f"Trabajo: {self.problema.nombre} - {estado}"


class EmailUsuario:
    """
    Gestiona la bandeja de entrada del usuario con trabajos disponibles
    """

    def __init__(self):
        self.bandeja_entrada: list[dict] = []
        self.trabajos_disponibles: list[Trabajo] = []
        self._generar_trabajos_iniciales()

    def _generar_trabajos_iniciales(self):
        """Genera trabajos iniciales desde el catálogo de problemas historia"""
        from dominio.entidades.problemas.catalogo_problemas_historia import CatalogoProblemasHistoria

        # Tomar los primeros 3 problemas para trabajos iniciales
        problemas_iniciales = CatalogoProblemasHistoria.obtener_todos()[:3]

        for i, problema_instancia in enumerate(problemas_iniciales):
            # Variar las recompensas según el nivel
            nivel = i + 1
            recompensa_dinero = 50 + (nivel * 25)  # 75, 100, 125
            recompensa_exp = 25 + (nivel * 15)     # 40, 55, 70

            trabajo = Trabajo(
                problema=problema_instancia,
                recompensa_dinero=recompensa_dinero,
                recompensa_experiencia=recompensa_exp
            )

            self.trabajos_disponibles.append(trabajo)

            # Convertir a formato de email para la bandeja
            email_dict = {
                "de": "sistema@innomath.cl",
                "asunto": trabajo.get_asunto_email(),
                "fecha": "30/05/2026",  # fecha fija por ahora
                "leido": False,
                "trabajo": trabajo,  # Referencia al trabajo real
                "cuerpo": [
                    "Hola tecnico,",
                    "",
                    trabajo.get_descripcion_email(),
                    "",
                    f"Recompensa: ${trabajo.recompensa_dinero} + {trabajo.recompensa_experiencia} XP",
                    "",
                    "Por favor confirma si puedes realizar este trabajo.",
                    "",
                    "Saludos,",
                    "-- Sistema InnoMath"
                ],
            }
            self.bandeja_entrada.append(email_dict)

    def get_trabajo_por_indice(self, indice: int) -> Trabajo | None:
        """Obtiene el trabajo asociado a un índice de correo"""
        if 0 <= indice < len(self.bandeja_entrada):
            return self.bandeja_entrada[indice].get("trabajo")
        return None

    def marcar_como_leido(self, indice: int):
        """Marca un correo como leído"""
        if 0 <= indice < len(self.bandeja_entrada):
            self.bandeja_entrada[indice]["leido"] = True

    def agregar_trabajo(self, trabajo: Trabajo):
        """Agrega un nuevo trabajo a la bandeja"""
        self.trabajos_disponibles.append(trabajo)

        email_dict = {
            "de": "sistema@innomath.cl",
            "asunto": trabajo.get_asunto_email(),
            "fecha": "30/05/2026",
            "leido": False,
            "trabajo": trabajo,
            "cuerpo": [
                "Hola tecnico,",
                "",
                trabajo.get_descripcion_email(),
                "",
                f"Recompensa: ${trabajo.recompensa_dinero} + {trabajo.recompensa_experiencia} XP",
                "",
                "Por favor confirma si puedes realizar este trabajo.",
                "",
                "Saludos,",
                "-- Sistema InnoMath"
            ],
        }
        self.bandeja_entrada.append(email_dict)