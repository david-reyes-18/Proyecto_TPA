from enum import Enum


class TipoPanel(Enum):
    
    """
    Clase de enumeración que guarda los tipos de paneles para laptops
    """
    
    # Rápido, ángulos pobres – básica/gamer entrada
    TN = "TN"
    
    # Colores, ángulos amplios – intermedia/workstation
    IPS = "IPS" 
    
    # Alto contraste – nicho
    VA = "VA" 
    
    # Premium, profundidad de negros – gamer premium
    OLED = "OLED" 