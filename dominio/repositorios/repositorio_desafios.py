from abc import ABC, abstractmethod
import random
from dominio.entidades.desafios.desafio import Desafio
from dominio.entidades.desafios.categoria_desafio import CategoriaDesafio
from dominio.entidades.desafios.componente_tematico import ComponenteTematico
from dominio.entidades.desafios.tipo_desafio.nombre_tipo_desafio import NombreTipoDesafio
from dominio.entidades.desafios.dificultad_desafio import NivelDificultad


class RepositorioDesafios(ABC):
    """
    Puerto (interfaz) para acceder al banco de desafíos.
    
    Implementado en infraestructura por RepositorioDesafiosJson.
    Separado de RepositorioProblemas (ISP): no todos los consumidores
    necesitan ambas interfaces.
    """
    
    @abstractmethod
    def obtener_todos(self) -> list[Desafio]:
        """Devuelve todos los desafíos del banco."""
    
    @abstractmethod
    def obtener_por_componente(self, componente: ComponenteTematico) -> list[Desafio]:
        """Devuelve todos los desafíos de un componente específico."""
    
    @abstractmethod
    def obtener_por_categoria(self, categoria: CategoriaDesafio) -> list[Desafio]:
        """Devuelve todos los desafíos de una categoría (lógico, matemático, tecnológico)."""
    
    @abstractmethod
    def obtener_por_tipo(self, tipo: NombreTipoDesafio) -> list[Desafio]:
        """Devuelve todos los desafíos de un tipo (booleano, multiple, escritura)."""
        
    @abstractmethod
    def obtener_filtrado(
        self,
        componente: ComponenteTematico,
        categoria: CategoriaDesafio,
        tipo: NombreTipoDesafio,
        dificultad: NivelDificultad,
    ) -> list[Desafio]:
        """
        Devuelve desafíos que cumplen exactamente los cuatro criterios.
        La implementación concreta lee los JSONs de fabricas/desafios/datos/.
        """
    
    def obtener_aleatorio(
        self,
        componente: ComponenteTematico,
        categoria: CategoriaDesafio,
        tipo: NombreTipoDesafio,
        dificultad: NivelDificultad,
    ) -> Desafio | None:
        """
        Devuelve un desafío al azar que cumple los cuatro criterios.
        Retorna None si no hay candidatos.
        """
        candidatos = self.obtener_filtrado(componente, categoria, tipo, dificultad)
        return random.choice(candidatos) if candidatos else None
    
    def obtener_aleatorio_por_componente_y_dificultad(
        self,
        componente: ComponenteTematico,
        dificultad: NivelDificultad,
    ) -> Desafio | None:
        """
        Devuelve un desafío al azar de cualquier categoría/tipo,
        filtrado solo por componente y dificultad.
        """
        todos = self.obtener_por_componente(componente)
        candidatos = [d for d in todos if d.dificultad == dificultad]
        return random.choice(candidatos) if candidatos else None
    
    def cantidad_por_componente(self, componente: ComponenteTematico) -> int:
        """Devuelve cuántos desafíos hay para un componente."""
        return len(self.obtener_por_componente(componente))
    
    def componentes_disponibles(self) -> list[ComponenteTematico]:
        """Devuelve los componentes que tienen al menos un desafío."""
        vistos: set[ComponenteTematico] = set()
        for desafio in self.obtener_todos():
            vistos.add(desafio.componente)
        return list(vistos)