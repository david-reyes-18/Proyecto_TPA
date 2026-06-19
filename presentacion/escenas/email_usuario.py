"""
Presentación: bandeja de entrada del correo del jugador.

Responsabilidad (SRP):
    Gestionar la lista de correos y su formato visual (dicts para la escena).
    La creación de trabajos delega en ServicioGestorTrabajos.
"""

from __future__ import annotations

from dominio.entidades.problemas.catalogo_problemas_historia import CatalogoProblemasHistoria
from dominio.servicios.gestor_trabajos import ServicioGestorTrabajos, Trabajo


class EmailUsuario:
    """Bandeja de entrada con trabajos disponibles."""

    def __init__(self, gestor: ServicioGestorTrabajos | None = None) -> None:
        self._gestor = gestor or ServicioGestorTrabajos()
        self.bandeja_entrada: list[dict] = []
        self.trabajos_disponibles: list[Trabajo] = []
        self._generar_trabajos_iniciales()

    def _generar_trabajos_iniciales(self) -> None:
        problemas_iniciales = CatalogoProblemasHistoria.obtener_todos()[:3]

        for i, problema in enumerate(problemas_iniciales):
            nivel = i + 1
            trabajo = self._gestor.crear_trabajo_desde_problema(
                problema=problema,
                recompensa_dinero=50 + (nivel * 25),
                recompensa_experiencia=25 + (nivel * 15),
            )
            self.trabajos_disponibles.append(trabajo)
            self.bandeja_entrada.append(self._trabajo_a_email(trabajo))

    def _trabajo_a_email(self, trabajo: Trabajo) -> dict:
        return {
            "de": "sistema@innomath.cl",
            "asunto": trabajo.asunto_email,
            "fecha": "30/05/2026",
            "leido": False,
            "trabajo": trabajo,
            "cuerpo": [
                "Hola tecnico,",
                "",
                trabajo.descripcion_email,
                "",
                f"Recompensa: ${trabajo.recompensa_dinero} + {trabajo.recompensa_experiencia} XP",
                "",
                "Por favor confirma si puedes realizar este trabajo.",
                "",
                "Saludos,",
                "-- Sistema InnoMath",
            ],
        }

    def get_trabajo_por_indice(self, indice: int) -> Trabajo | None:
        if 0 <= indice < len(self.bandeja_entrada):
            return self.bandeja_entrada[indice].get("trabajo")
        return None

    def marcar_como_leido(self, indice: int) -> None:
        if 0 <= indice < len(self.bandeja_entrada):
            self.bandeja_entrada[indice]["leido"] = True

    def agregar_trabajo(self, trabajo: Trabajo) -> None:
        self.trabajos_disponibles.append(trabajo)
        self.bandeja_entrada.append(self._trabajo_a_email(trabajo))
