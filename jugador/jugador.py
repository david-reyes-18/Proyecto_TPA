import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0)) # Cuadrado rojo temporal
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.tamano_casilla = 32
        self.velocidad = 4
        
        self.en_movimiento = False
        self.destino_x = x
        self.destino_y = y
        self.direccion_actual = 'abajo'

    def actualizar(self, teclas, grupo_colisiones):
        # 1. Si NO se está moviendo, calculamos a dónde quiere ir
        if not self.en_movimiento:
            nuevo_destino_x = self.destino_x
            nuevo_destino_y = self.destino_y
            intenta_moverse = False

            if teclas[pygame.K_LEFT]:
                self.direccion_actual = 'izquierda'
                nuevo_destino_x -= self.tamano_casilla
                intenta_moverse = True
            elif teclas[pygame.K_RIGHT]:
                self.direccion_actual = 'derecha'
                nuevo_destino_x += self.tamano_casilla
                intenta_moverse = True
            elif teclas[pygame.K_UP]:
                self.direccion_actual = 'arriba'
                nuevo_destino_y -= self.tamano_casilla
                intenta_moverse = True
            elif teclas[pygame.K_DOWN]:
                self.direccion_actual = 'abajo'
                nuevo_destino_y += self.tamano_casilla
                intenta_moverse = True

            # 2. Verificar colisiones ANTES de confirmar el movimiento
            if intenta_moverse:
                # Creamos un rectángulo invisible (hitbox) en la casilla de destino
                rect_futuro = pygame.Rect(nuevo_destino_x, nuevo_destino_y, self.tamano_casilla, self.tamano_casilla)
                
                colision = False
                for obstaculo in grupo_colisiones:
                    if rect_futuro.colliderect(obstaculo.rect):
                        colision = True
                        break # Si chocamos con uno, no hace falta comprobar el resto
                
                # 3. Si la casilla está libre, autorizamos el movimiento
                if not colision:
                    self.destino_x = nuevo_destino_x
                    self.destino_y = nuevo_destino_y
                    self.en_movimiento = True

        # 4. Si SÍ se está moviendo, desplazamos el personaje hacia el destino
        else:
            if self.rect.x < self.destino_x:
                self.rect.x += self.velocidad
            elif self.rect.x > self.destino_x:
                self.rect.x -= self.velocidad
                
            if self.rect.y < self.destino_y:
                self.rect.y += self.velocidad
            elif self.rect.y > self.destino_y:
                self.rect.y -= self.velocidad
                
            if self.rect.x == self.destino_x and self.rect.y == self.destino_y:
                self.en_movimiento = False