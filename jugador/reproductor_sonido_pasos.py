from core.manejador_sonidos import ManejadorSonidos


class ReproductorSonidosPasos:
    
    def __init__(self, intervalo_pasos: float = 0.35) -> None:
        
        self._timer_pasos = 0.0
        self._intervalo_pasos = intervalo_pasos
    
    def actualizar_y_reproducir(self, moviendose: bool, dt: float) -> bool:
        """
        Actualiza el temporizador de pasos y reproduce el sonido si es necesario.
        """
        if not moviendose:
            self._timer_pasos = 0
            return False
        
        self._timer_pasos -= dt
        if self._timer_pasos <= 0:
            ManejadorSonidos.reproducir("pasos.ogg")
            self._timer_pasos = self._intervalo_pasos
            return True
        return False