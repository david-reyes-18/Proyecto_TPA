from enum import Enum

class NombreTipoDesafio(Enum):
    
    #Tipo de desafio en el cual se escribira la respuesta en un campo
    ESCRITURA = "ESCRITURA"
    
    #Tipo de ejercicio donde se tendra que escoger la respuesta dentro de multiples respuestas
    MULTIPLE = "MULTIPLE"
    
    #Tipo de desafio que tendra la posibilidad de decir si es verdadero o falso
    BOOLEANO = "BOOLEANO"