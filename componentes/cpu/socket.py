from enum import Enum


class SocketCPU(Enum):
    
    """
    Clase de enumeracion para ordenar los posibles sockets
    que puede tener una laptop y pc de escritorio
    """
    
    # AMD PC escritorio
    AM4 = "AM4" # Ryzen 1000–5000, Athlon 3000G
    AM5 = "AM5" # Ryzen 7000–9000
    
    # Intel PC escritorio
    LGA1151 = "LGA1151" # 6.ª–9.ª gen
    LGA1200 = "LGA1200" # 10.ª–11.ª gen
    LGA1700 = "LGA1700" # 12.ª–14.ª gen
    
    # Laptops: todos los CPUs móviles van soldados (BGA)
    BGA = "BGA"