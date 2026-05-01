class ResultadoOperacion:
    def __init__(
        self,
        exito_operacion: bool,
        codigo_operacion: str,
        mensaje_sistema: str,
        costo: int = 0,
        experiencia: int = 0
    ):
        self._exito_operacion = exito_operacion
        self._codigo_operacion = codigo_operacion
        self._mensaje_sistema = mensaje_sistema
        self._costo = costo
        self._experiencia = experiencia
    
    @property
    def exito(self) -> bool:
        return self._exito_operacion

    @property
    def codigo(self):
        return self._codigo_operacion

    @property
    def mensaje(self) -> str:
        return self._mensaje_sistema

    @property
    def costo(self) -> int:
        return self._costo

    @property
    def experiencia(self) -> int:
        return self._experiencia