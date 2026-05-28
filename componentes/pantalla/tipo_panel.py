from enum import Enum

"""
Clase de enumeración que guarda los tipos de paneles para laptops
"""

class TipoPanel(Enum):
    TN = "TN" # Rápido, ángulos pobres – básica/gamer entrada
    IPS = "IPS" # Colores, ángulos amplios – intermedia/workstation
    VA = "VA" # Alto contraste – nicho
    OLED = "OLED" # Premium, profundidad de negros – gamer premium