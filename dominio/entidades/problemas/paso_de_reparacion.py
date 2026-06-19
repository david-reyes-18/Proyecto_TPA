from dominio.entidades.desafios.desafio import Desafio
from dominio.valores.resultado_operaciones import ResultadoOperacion
from dominio.valores.codigo_operacion import CodigoOperacion
from dominio.valores.mensaje_sistema import MensajesSistema


class PasoDeReparacion:
    def __init__(
            self, 
            descripcion_accion: str, 
            explicacion: str, 
            desafio: Desafio
        ) -> None:
        
        self._descripcion_accion = descripcion_accion
        self._explicacion = explicacion
        self._desafio = desafio
        self._completado = False
        
    #   Propiedades
        
    @property
    def descripcion_accion(self) -> str:
        return self._descripcion_accion
    
    @property
    def explicacion(self) -> str:
        return self._explicacion
    
    @property
    def desafio(self) -> Desafio:
        return self._desafio
    
    @property
    def completado(self) -> bool:
        return self._completado
    
    
    #   Metodos
    
    def verificar_respuesta(self, respuesta_usuario: float) -> ResultadoOperacion:
        resultado = self._desafio.verificar_respuesta(respuesta_usuario)
        if resultado.exito_operacion:
            self._completado = True
        return resultado