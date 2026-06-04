
import pygame


class Paleta:
    
    """
    Paleta de colores de todo el juego, donde se pueden seleccionar colores
    de fondo, botones, sliders, texto, etc.
    """
    
    #   Fondos
    FONDO_PANTALLA               = pygame.Color("#0D1B2A")
    FONDO_PANEL                  = pygame.Color("#132339")
    FONDO_PANEL_CLARO            = pygame.Color("#1A304E")
    FONDO_BARRA_TITULO           = pygame.Color("#0F1E37")
    
    #   Bordes y líneas decorativas
    BORDE_ACTIVO                 = pygame.Color("#00C2D1")
    BORDE_INACTIVO               = pygame.Color("#28466E")
    BORDE_SUTIL                  = pygame.Color("#1E3250")
    LINEA_DECORATIVA             = pygame.Color("#00C2D1")
    
    """Botones"""
    
    # Colores para todos los botones
    BOTON_TEXTO                  = pygame.Color("#E8F1FF")
    BOTON_TEXTO_HOVER            = pygame.Color("#FFFFFF")
    BOTON_BORDER_COLOR           = pygame.Color("#E8F1FF")
    BOTON_BORDER_HOVER_COLOR     = pygame.Color("#FFFFFF")
    
    # Botones Menú Principal 
    BOTON_MENU_FONDO             = pygame.Color("#132339")
    BOTON_MENU_HOVER             = pygame.Color("#1E4B8C")
    
    # Botones — Configuración
    BOTON_CONFIG_FONDO           = pygame.Color("#162841")
    BOTON_CONFIG_HOVER           = pygame.Color("#00788C")
    
    # Botones Acción positiva
    BOTON_OK_FONDO               = pygame.Color("#006450")
    BOTON_OK_HOVER               = pygame.Color("#00B476")
    BOTON_OK_TEXTO               = pygame.Color("#C8FFE6")
    
    # Botones Acción peligrosa
    BOTON_PELIGRO_FONDO          = pygame.Color("#5A1414")
    BOTON_PELIGRO_HOVER          = pygame.Color("#C83232")
    BOTON_PELIGRO_TEXTO          = pygame.Color("#FFD2D2")
    
    #   Texto 
    TEXTO_TITULO                 = pygame.Color("#00C2D1")
    TEXTO_SUBTITULO              = pygame.Color("#4FC3F7")
    TEXTO_PRINCIPAL              = pygame.Color("#E8F1FF")
    TEXTO_SECUNDARIO             = pygame.Color("#8BAABF")
    TEXTO_DESACTIVADO            = pygame.Color("#445566")
    TEXTO_DORADO                 = pygame.Color("#FFD54F")
    TEXTO_ROJO                   = pygame.Color("#FF5252")
    TEXTO_VERDE                  = pygame.Color("#00E676")
    TEXTO_MORADO                 = pygame.Color("#A908FF")
    
    #   Sliders
    SLIDER_FONDO                 = pygame.Color("#1E2D46")
    SLIDER_KNOB_BORDER_COLOR     = pygame.Color("#FFFFFF")
    
    SLIDER_MUSICA_RELLENO        = pygame.Color("#00C2D1")
    SLIDER_MUSICA_KNOB_CENTRO    = pygame.Color("#00C2D1")
    
    SLIDER_SONIDO_RELLENO        = pygame.Color("#A908FF")
    SLIDER_SONIDO_KNOB_CENTRO    = pygame.Color("#8503CB")
    
    # Feedback y estados del juego
    ESTADO_CORRECTO              = pygame.Color("#00E676")
    ESTADO_INCORRECTO            = pygame.Color("#FF5252")
    ESTADO_ADVERTENCIA           = pygame.Color("#FFD54F")
    ESTADO_LOGICA                = pygame.Color("#B388FF")
    
    # Decoraciones pequeñas
    DECO_PUNTO_NO_LEIDO          = pygame.Color("#00C2D1")
    DECO_SEPARADOR               = pygame.Color("#1E3250")
    DECO_SELECCION               = pygame.Color("#1E4B8C")
    DECO_SELECCION_ALPHA         = 100

    # Colores específicos para la escena de inventario (estilo Pokémon)
    INVENTARIO_FONDO             = pygame.Color("#1E1E28")  # Fondo principal oscuro
    INVENTARIO_PANEL             = pygame.Color("#282832")  # Fondos de paneles
    INVENTARIO_BORDE             = pygame.Color("#3C3C46")  # Bordes y separadores
    INVENTARIO_TEXTO             = pygame.Color("#C8C8C8")  # Texto normal
    INVENTARIO_TEXTO_DESTACADO   = pygame.Color("#FFFFFF")  # Texto destacado/seleccionado
    INVENTARIO_SELECCION         = pygame.Color("#4682B4")  # Color de selección (azul Pokémon)
    INVENTARIO_CURSOR            = pygame.Color("#FFFFFF")    # Color del cursor de selección
    INVENTARIO_TEXTO_DESCRIPCION = pygame.Color("#FFFFFF")  # Texto en área de descripción
    INVENTARIO_TEXTO_PISTA       = pygame.Color("#B4B4B4")   # Texto de pistas/hints
    INVENTARIO_SCROLL            = pygame.Color("#646478")       # Indicadores de scroll