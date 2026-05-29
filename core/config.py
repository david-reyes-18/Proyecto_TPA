"""
Archivo que guarda configuraciónes globales y constantes
para usarse en todo el proyecto
"""

# Ancho y alto de la ventana al iniciar el juego
ANCHO = 1200
ALTO = 800

# Cuadros por segundo que máximos que aparecerán en el juego
FPS = 60

# Posibles resoluciones de pantalla
RESOLUCIONES = [
    (800,  600,  "800 x 600"),
    (1024, 768,  "1024 x 768"),
    (1200, 800,  "1200 x 800"),
    (1280, 720,  "1280 x 720 (HD)")
]

# Escalas globales y por el jugador
ESCALA_GLOB = 3
ESCALA_JUGADOR = 4

# Cuadros por segundo que tendrá el personaje en reposo (estático) y en movimiento
FPS_ESTATICO = 4
FPS_CORRIENDO = 10

# Ancho y alto de cada frame del jugador (en px)
FRAME_ANCHO = 16
FRAME_ALTO = 24

# Frames que hay por cada spritesheet (en spritesheet estático y corriendo)
FRAMES_ESTATICO = 4
FRAMES_POR_DIRECCION = 6

# filas del spritesheet run
DIRECCIONES = {
    "DERECHA": 0,
    "ARRIBA": 1,
    "IZQUIERDA": 2,
    "ABAJO": 3,
}
