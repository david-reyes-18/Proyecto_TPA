import pygame
from core.juego import Juego

def main():
    pygame.init()
    
    juego = Juego()
    juego.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()