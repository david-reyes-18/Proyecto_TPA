from __future__ import annotations
from componentes.base.componente import Componente
from componentes.base.reemplazable import Reemplazable
from componentes.bateria.forma_bateria import FormaBateria
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema



class Bateria(Componente, Reemplazable):
    
    """
    Moldea una bateria de laptop
    """
    
    def __init__(
            self, 
            voltaje_v: float,
            forma_bateria: FormaBateria,
            capacidad_wh: float,
            salud: int, 
        ) -> None:
        
        super().__init__(nombre="Bateria", es_reemplazable=True, es_reparable=False)
        
        self._voltaje_v = voltaje_v
        self._forma_bateria = forma_bateria
        self._capacidad_wh = capacidad_wh
        self._salud = salud
        self._esta_conectada: bool = True
        
        if self._salud < 30:
            self._esta_funcionando = False
    
    
    #   Getters
    
    @property
    def voltaje_v(self) -> float:
        return self._voltaje_v
    
    @property
    def forma_bateria(self) -> FormaBateria:
        return self._forma_bateria
    
    @property
    def capacidad_wh(self) -> float:
        return self._capacidad_wh
    
    @property
    def salud(self) -> int:
        return self._salud
    
    @property
    def esta_conectada(self) -> bool:
        return self._esta_conectada
    
    @property
    def esta_funcionando(self) -> bool:
        return self._salud >= 30
    
    
    #   Métodos
    
    # Desconectar la bateria
    def desconectar(self) -> ResultadoOperacion:
        
        if self._esta_conectada:
            self._esta_conectada = False
            return ResultadoOperacion(
                exito_operacion = True,
                codigo_operacion = CodigoOperacion.BATERIA_DESCONECTADA,
                mensaje_sistema = MensajesSistema.BATERIA_DESCONECTADA
            )
        
        else:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.BATERIA_CONECTADA,
                mensaje_sistema = MensajesSistema.BATERIA_CONECTADA
            )
    
    # Conectar bateria
    def conectar(self) -> ResultadoOperacion:
        
        if not self._esta_conectada:
            self._esta_conectada = True
            return ResultadoOperacion(
                exito_operacion = True,
                codigo_operacion = CodigoOperacion.BATERIA_CONECTADA,
                mensaje_sistema = MensajesSistema.BATERIA_CONECTADA
            )
        
        else:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.BATERIA_DESCONECTADA,
                mensaje_sistema = MensajesSistema.BATERIA_DESCONECTADA
            )
    
    # Reemplazar la bateria por una nueva
    def reemplazar(self, nueva_bateria: Bateria, costo: int) -> ResultadoOperacion:
        
        # Si se encuentra funcional no hay nesesidad de un cambio
        if self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
                mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
            )
        
        # Si el voltaje de la nueva bateria y la actual es diferente, entonces no son compatibles
        if nueva_bateria.voltaje_v != self._voltaje_v:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.VOLTAJE_BATERIA_INCORRECTO,
                mensaje_sistema = MensajesSistema.VOLTAJE_BATERIA_INCORRECTO
            )
        
        # Si la forma de ambas baterias no son iguales entonces la nueva bateria no es compatible
        if nueva_bateria.forma_bateria != self._forma_bateria:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.FORMA_BATERIA_INCORRECTA,
                mensaje_sistema = MensajesSistema.FORMA_BATERIA_INCORRECTA
            )
        
        # Si todo resultó bien entonces se reemplaza
        self._capacidad_wh = nueva_bateria.capacidad_wh
        self._voltaje_v = nueva_bateria.voltaje_v
        self._salud = 100
        self._forma_bateria = nueva_bateria._forma_bateria
        self._esta_funcionando = True
        
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.EXITO_REEMPLAZO,
            mensaje_sistema = MensajesSistema.EXITO_REEMPLAZO,
            costo = costo
        )
    
    # Diagnostica si el componente se encuentra funcional
    def diagnosticar(self) -> ResultadoOperacion:
        
        if self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion = True,
                codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
                mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
            )
        
        else:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.BATERIA_DEGRADADA,
                mensaje_sistema = MensajesSistema.BATERIA_DEGRADADA
            )