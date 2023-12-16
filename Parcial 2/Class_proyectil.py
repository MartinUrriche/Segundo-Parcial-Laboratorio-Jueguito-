import pygame
from Configuraciones import *
from Class_enemigo import *

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y,velocidad,direccion):
        super().__init__()

        self.image = personaje_proyectil.convert()
        self.image = pygame.transform.scale(self.image, (10, 5)) 
        if direccion == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = direccion * velocidad  # Ajustar la velocidad según la dirección

    def actualizar_proyectil(self):
        # Actualiza la posición del proyectil
        self.rect.x += self.velocidad
        if self.rect.x > 800 or self.rect.x < 0:  # Ajusta la condición para ambos lados
            self.kill()

    def verificar_colision_proyectil_enemigo(self,lista_enemigo:list["Enemigo"],pantalla):
        for enemigo in lista_enemigo:
            if self.rect.colliderect(enemigo.rectangulo_principal):
                enemigo.muriendo = True
                enemigo.rectangulo_principal.y +=20
                enemigo.animacion_actual = enemigo.animaciones["aplasta"]
                enemigo.animar(pantalla)
                self.kill()
    