import sys
import pygame
from presentacion.juego import Juego

sys.dont_write_bytecode = True

def main():
    pygame.init()
    
    juego = Juego()
    juego.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()