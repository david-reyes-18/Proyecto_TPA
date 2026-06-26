from dominio.repositorios.repositorio_problemas import RepositorioProblemas
from dominio.entidades.problemas.problema import Problema
from dominio.entidades.desafios.componente_tematico import ComponenteTematico
from dominio.entidades.problemas.catalogo_problemas_historia import CatalogoProblemasHistoria


class RepositorioProblemasHistoria(RepositorioProblemas):
    """
    Repositorio de problemas de modo historia.
    """

    def obtener_todos(self) -> list[Problema]:
        return CatalogoProblemasHistoria.obtener_todos()

    def obtener_por_nivel(self, nivel: int) -> Problema | None:
        return CatalogoProblemasHistoria.obtener_problema(nivel)

    def obtener_por_componente(self, componente: ComponenteTematico) -> list[Problema]:
        return [
            p for p in self.obtener_todos()
            if p.componente_afectado.nombre.upper() == componente.value.upper()
        ]
