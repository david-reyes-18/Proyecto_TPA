from componente.componente import Componente
from forma_bateria import FormaBateria
from sistema.resultado_operaciones import ResultadoOperacion
from sistema.codigo_operacion import CodigoOperacion
from sistema.mensaje_sistema import MensajesSistema


class Bateria(Componente):
    def __init__(self, 
                voltaje: float,
                forma_bateria: FormaBateria,
                capacidad_mah: int,
                salud: int, 
                esta_conectada: bool,
            ):
        super().__init__(nombre = "Bateria", es_reemplazable = True, es_reparable = False)
        self._voltaje = voltaje
        self._forma_bateria = forma_bateria
        self._capacidad_mah = capacidad_mah
        self._salud = salud
        self._esta_conectada = esta_conectada
        
        if self._salud < 30:
            self._esta_funcionando = False
    
    @property
    def voltaje(self) -> float:
        return self._voltaje
    
    @property
    def forma_bateria(self) -> FormaBateria:
        return self._forma_bateria
    
    @property
    def capacidad_mah(self) -> int:
        return self._capacidad_mah
    
    @property
    def salud(self) -> int:
        return self._salud
    
    @property
    def esta_conectada(self) -> bool:
        return self._esta_conectada
    
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
    
    def reparar(self) -> ResultadoOperacion:
        return ResultadoOperacion(
            exito_operacion = False,
            codigo_operacion = CodigoOperacion.NO_REPARABLE,
            mensaje_sistema = MensajesSistema.NO_REPARABLE
        )
    
    def reemplazar(self, nueva_bateria: Bateria, costo: int) -> ResultadoOperacion:
        if self._esta_funcionando:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.COMPONENTE_FUNCIONAL,
                mensaje_sistema = MensajesSistema.COMPONENTE_FUNCIONAL
            )
        
        if nueva_bateria.voltaje != self._voltaje:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.VOLTAJE_BATERIA_INCORRECTO,
                mensaje_sistema = MensajesSistema.VOLTAJE_BATERIA_INCORRECTO
            )
        
        if nueva_bateria.forma_bateria != self._forma_bateria:
            return ResultadoOperacion(
                exito_operacion = False,
                codigo_operacion = CodigoOperacion.FORMA_BATERIA_INCORRECTA,
                mensaje_sistema = MensajesSistema.FORMA_BATERIA_INCORRECTA
            )
        
        self._capacidad_mah = nueva_bateria.capacidad_mah
        self._voltaje = nueva_bateria.voltaje
        self._salud = 100
        self._forma_bateria = nueva_bateria._forma_bateria
        self._esta_funcionando = True
        
        return ResultadoOperacion(
            exito_operacion = True,
            codigo_operacion = CodigoOperacion.EXITO_REEMPLAZO,
            mensaje_sistema = MensajesSistema.EXITO_REEMPLAZO,
            costo = costo
        )
    
    def diagnosticar(self):
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