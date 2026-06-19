from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from presentacion.escenas.escena_base import EscenaBase
from infraestructura.texto.fuente import Fuente
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.tipo_desafio.tipo_multiple import TipoMultiple
from dominio.entidades.dispositivos.dispositivo import Dispositivo
from dominio.servicios.diagnostico import InformeDiagnostico, ServicioDiagnostico
from dominio.servicios.gestor_trabajos import ServicioGestorTrabajos
from dominio.servicios.reparacion import ServicioReparacion

if TYPE_CHECKING:
    from presentacion.juego import Juego


class EscenaTaller(EscenaBase):
    """Escena de reparación: diagnóstico y pasos del problema activo."""

    def __init__(self, juego: Juego) -> None:
        super().__init__(juego)

        self.servicio_diagnostico = ServicioDiagnostico()
        self.servicio_reparacion = ServicioReparacion()
        self.gestor_trabajos = ServicioGestorTrabajos()

        self.dispositivo: Dispositivo | None = self._resolver_dispositivo()
        self.informe: InformeDiagnostico | None = None
        self.mensaje_feedback = ""
        self.temporizador_feedback = 0

        self.fuente_titulo = Fuente.obtener(32)
        self.fuente_info = Fuente.obtener(18)
        self.fuente_paso = Fuente.obtener(16)
        self.fuente_pequena = Fuente.obtener(14)

    def _resolver_dispositivo(self) -> Dispositivo | None:
        if self.juego.trabajo_activo and self.juego.trabajo_activo.dispositivo:
            return self.juego.trabajo_activo.dispositivo
        return self.juego.jugador.inventario.obtener_dispositivo_pendiente()

    def manejar_eventos(self, eventos: list[pygame.event.Event]) -> None:
        for evento in eventos:
            if evento.type != pygame.KEYDOWN:
                continue

            if evento.key == pygame.K_ESCAPE:
                from presentacion.escenas.escena_juego import EscenaJuego
                self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))
            elif evento.key == pygame.K_d:
                self._ejecutar_diagnostico()
            elif self.dispositivo is not None:
                self._manejar_respuesta(evento)

    def _ejecutar_diagnostico(self) -> None:
        if self.dispositivo is None:
            self._mostrar_feedback("No hay dispositivo para diagnosticar. Acepta un trabajo primero.")
            return

        self.informe = self.servicio_diagnostico.diagnosticar(self.dispositivo)
        confirmacion = self.servicio_diagnostico.confirmar_falla_reportada(self.informe)
        self._mostrar_feedback(confirmacion.mensaje_sistema)

    def _manejar_respuesta(self, evento: pygame.event.Event) -> None:
        paso = self.servicio_reparacion.obtener_paso_actual(self.dispositivo.problema)
        if paso is None:
            if not self.dispositivo.esta_reparado:
                resultado = self.servicio_reparacion.finalizar(self.dispositivo)
                self._mostrar_feedback(resultado.mensaje_sistema)
                if resultado.exito_operacion:
                    self._completar_trabajo()
            return

        desafio = paso.desafio
        respuesta = None

        if desafio.tipo == NombreTipoDesafio.BOOLEANO:
            if evento.key == pygame.K_s:
                respuesta = True
            elif evento.key == pygame.K_n:
                respuesta = False
        elif desafio.tipo == NombreTipoDesafio.MULTIPLE and isinstance(desafio, TipoMultiple):
            teclas = {
                pygame.K_1: 0,
                pygame.K_2: 1,
                pygame.K_3: 2,
                pygame.K_4: 3,
            }
            if evento.key in teclas and teclas[evento.key] < len(desafio.alternativas):
                respuesta = teclas[evento.key]
        elif desafio.tipo == NombreTipoDesafio.ESCRITURA:
            if evento.key == pygame.K_RETURN:
                self._mostrar_feedback("Desafíos de escritura: próximamente con campo de texto.")

        if respuesta is None:
            return

        resultado = self.servicio_reparacion.responder_paso(paso, respuesta)
        self._mostrar_feedback(resultado.mensaje_sistema)

        if self.servicio_reparacion.reparacion_completa(self.dispositivo.problema):
            resultado_final = self.servicio_reparacion.finalizar(self.dispositivo)
            self._mostrar_feedback(resultado_final.mensaje_sistema)
            if resultado_final.exito_operacion:
                self._completar_trabajo()

    def _completar_trabajo(self) -> None:
        trabajo = self.juego.trabajo_activo
        if trabajo is None:
            return

        resultado = self.gestor_trabajos.completar(trabajo, self.juego.jugador.stats)
        self._mostrar_feedback(resultado.mensaje_sistema, duracion=240)

    def _mostrar_feedback(self, mensaje: str, duracion: int = 120) -> None:
        self.mensaje_feedback = mensaje
        self.temporizador_feedback = duracion

    def actualizar(self, dt: float) -> None:
        if self.temporizador_feedback > 0:
            self.temporizador_feedback -= 1

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((30, 18, 10))
        centro_x = pantalla.get_width() // 2

        titulo = self.fuente_titulo.render("TALLER", False, (255, 180, 60))
        pantalla.blit(titulo, titulo.get_rect(centerx=centro_x, y=40))

        if self.dispositivo is None:
            self._dibujar_lineas(pantalla, centro_x, 140, [
                "No hay trabajos activos.",
                "Acepta un correo en la laptop y vuelve aquí.",
                "",
                "[ ESC ] Volver al mapa",
            ])
            return

        problema = self.dispositivo.problema
        completados, total = self.servicio_reparacion.progreso(problema)
        modelo = getattr(self.dispositivo, "modelo", "Dispositivo")

        self._dibujar_lineas(pantalla, centro_x, 100, [
            f"Equipo: {modelo}",
            f"Problema: {problema.nombre}",
            f"Progreso: {completados}/{total} pasos",
            "",
            "[ D ] Diagnosticar",
            "[ ESC ] Volver al mapa",
        ])

        if self.informe is not None:
            y = 220
            for linea in self._lineas_informe():
                surf = self.fuente_pequena.render(linea, False, (200, 200, 160))
                pantalla.blit(surf, surf.get_rect(centerx=centro_x, y=y))
                y += 22

        paso = self.servicio_reparacion.obtener_paso_actual(problema)
        y_paso = 320
        if paso is None:
            if self.dispositivo.esta_reparado:
                texto = "Reparación completada."
            else:
                texto = "Todos los pasos listos. Presiona cualquier tecla de respuesta."
            surf = self.fuente_paso.render(texto, False, (120, 255, 120))
            pantalla.blit(surf, surf.get_rect(centerx=centro_x, y=y_paso))
        else:
            self._dibujar_paso_actual(pantalla, centro_x, y_paso, paso)

        if self.mensaje_feedback and self.temporizador_feedback > 0:
            color = (255, 255, 100) if "incorrecta" in self.mensaje_feedback.lower() else (180, 255, 180)
            surf = self.fuente_pequena.render(self.mensaje_feedback, False, color)
            pantalla.blit(surf, surf.get_rect(centerx=centro_x, y=pantalla.get_height() - 60))

    def _lineas_informe(self) -> list[str]:
        if self.informe is None:
            return []
        lineas = [f"Diagnóstico: {self.informe.resumen}"]
        for nombre, resultado in self.informe.fallas[:3]:
            lineas.append(f"  - {nombre}: {resultado.mensaje_sistema}")
        return lineas

    def _dibujar_paso_actual(self, pantalla: pygame.Surface, centro_x: int, y: int, paso) -> None:
        lineas = [
            f"Paso: {paso.descripcion_accion}",
            "",
            paso.desafio.enunciado,
            "",
        ]

        desafio = paso.desafio
        if desafio.tipo == NombreTipoDesafio.BOOLEANO:
            lineas.append("[ S ] Sí    [ N ] No")
        elif desafio.tipo == NombreTipoDesafio.MULTIPLE and isinstance(desafio, TipoMultiple):
            for i, alt in enumerate(desafio.alternativas):
                lineas.append(f"  [ {i + 1} ] {alt}")
        elif desafio.tipo == NombreTipoDesafio.ESCRITURA:
            lineas.append("[ ENTER ] (escritura próximamente)")

        self._dibujar_lineas(pantalla, centro_x, y, lineas, self.fuente_paso, (255, 220, 160))

    def _dibujar_lineas(
        self,
        pantalla: pygame.Surface,
        centro_x: int,
        y: int,
        lineas: list[str],
        fuente=None,
        color=(255, 220, 160),
    ) -> None:
        fuente = fuente or self.fuente_info
        for linea in lineas:
            surf = fuente.render(linea, False, color)
            pantalla.blit(surf, surf.get_rect(centerx=centro_x, y=y))
            y += fuente.get_height() + 8
