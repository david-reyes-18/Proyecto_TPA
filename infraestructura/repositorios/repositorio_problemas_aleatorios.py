from dominio.repositorios.repositorio_problemas import RepositorioProblemas
from dominio.entidades.problemas.problema import Problema
from dominio.entidades.desafios.componente_tematico import ComponenteTematico
from dominio.entidades.problemas.catalogo_problemas_aleatorios import CatalogoProblemasAleatorios


class RepositorioProblemasAleatorios(RepositorioProblemas):
    """
    Repositorio de problemas aleatorios.
    """
    def obtener_todos(self) -> list[Problema]:
        return CatalogoProblemasAleatorios.obtener_todos()

    def obtener_por_nivel(self, nivel: int) -> Problema | None:
        todos = self.obtener_todos()
        idx = nivel - 1
        return todos[idx] if 0 <= idx < len(todos) else None

    def obtener_por_componente(self, componente: ComponenteTematico) -> list[Problema]:
        return [
            p for p in self.obtener_todos()
            if p.componente_afectado.nombre.upper() == componente.value.upper()
        ]
