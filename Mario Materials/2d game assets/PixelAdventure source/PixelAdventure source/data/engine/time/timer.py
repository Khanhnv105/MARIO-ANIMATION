
class Timer:
    
    """
    Clase que controla el tiempo de la simulacion,
    a diferencia del loop(), a este se le puede
    modificar la velocidad
    """
    
    def __init__(self):
        self._actual_time = 0
        self._time_speed = 1.0
        
    def tick(self, dt) -> float:
        
        """Hace un tick y retorna delta_time"""
        
        delta_time = self._get_delta_time(dt)
        self._actual_time += 1 * delta_time
        return delta_time
        
    def get_ticks(self) -> float:
        return self._actual_time
    
    def get_speed(self) -> float:
        return self._time_speed
    
    def _get_delta_time(self, dt: float) -> float:
        """Retorna delta_time en base a la velocidad del timer"""
        return self._time_speed * dt
    
    def set_speed(self, speed: float): 
        self._time_speed = speed
