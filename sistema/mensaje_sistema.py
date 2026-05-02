class MensajesSistema:
    #Mensajes para operaciónes exitosas
    EXITO_REPARACION = "Reparación realizada con éxito."
    EXITO_REEMPLAZO = "Componente reemplazado correctamente."
    EXITO_INSTALACION = "Instalación completada correctamente."
    COMPONENTE_FUNCIONAL = "El componente se encuentra totalmente funcional"
    
    #RAM
    SLOT_OCUPADO = "El slot en donde se quiere poner la memoria RAM ya se encuentra en uso"
    CAPACIDAD_MAXIMA_GB_EXCEDIDA = "la cantidad de gb que se desea agregar excede el limite del slot"
    RAM_INCOMPATIBLE = "La memoria RAM no es compatible con la placa base."
    
    #PANTALLA
    TAMANO_PANTALLA_INCORRECTA = "La pantalla no posee el tamaño correcto."
    PANTALLA_ROTA = "La pantalla presenta daño físico."
    
    #BATERIA
    BATERIA_DESCONECTADA = "La bateria se encuentra desconectada"
    BATERIA_CONECTADA = "La bateria se encuentra conectada"
    VOLTAJE_BATERIA_INCORRECTO = "El voltaje de la nueva bateria no es el indicado para la laptop"
    FORMA_BATERIA_INCORRECTA = "La forma de la bateria no coincide con la del dispositivo"
    BATERIA_DEGRADADA = "La batería presenta desgaste severo."

    #CPU
    CPU_SOBRECALENTADO = "El procesador supera temperaturas seguras."
    CPU_INCOMPATIBLE = "La cpu es incompatible"
    
    #GPU
    GPU_FALLA = "La tarjeta gráfica presenta fallas."
    GPU_INCOMPATIBLE = "La GPU es incompatible"
    
    #SSD
    SSD_DANADO = "La unidad de almacenamiento presenta errores."
    SSD_INTERFAZ_INCOMPATIBLE = "La interfaz del SSD no es compatible con este dispositivo."
    SSD_CAPACIDAD_INSUFICIENTE = "La capacidad del nuevo SSD es menor que la del actual."

    #Mensajes para errores
    NO_REEMPLAZABLE = "Este componente no puede ser reemplazado."
    NO_REPARABLE = "Este componente no se puede reparar"
    ERROR_COMPONENTE_FUNCIONAL = "El componente ya funciona correctamente."
    ERROR_INCOMPATIBILIDAD = "El componente es incompatible."
    ERROR_INSTALACION = "La instalación ha fallado."
    ERROR_GENERAL = "Ha ocurrido un error en la operación."