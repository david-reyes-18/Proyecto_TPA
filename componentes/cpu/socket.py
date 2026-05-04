from enum import Enum

class SocketCPU(Enum):
    # AMD
    AM4 = "AM4"
    AM5 = "AM5"
    #INTEL
    LGA1151 = "LGA1151"
    LGA1200 = "LGA1200"
    LGA1700 = "LGA1700"
    #LAPTOPS
    BGA = "BGA"