import pygame
from Modo import obtener_modo
from Class_limites import Limite


class Plataforma:
    def __init__(self, visible, tamaño, x, y, path="", movible=False, rango_y=(0, 0), rango_x=(0, 0)):
        self.superficie = self._cargar_superficie(visible, tamaño, path)
        self.rectangulo = self.superficie.get_rect() 
        self.rectangulo.topleft = (x, y)

        self.inicializar_limites()
        self.movible = movible

        if self.movible:
            self.velocidad = 3
            self.rango_y = rango_y  
            self.rango_x = rango_x
            self.inicializar_limites()
        

    def inicializar_limites(self):
        altura_limites = 20

        # Crear límite izquierdo
        self.limite_izquierdo = Limite(self.rectangulo.left, self.rectangulo.top - altura_limites, 5, altura_limites)

        # Crear límite derecho
        self.limite_derecho = Limite(self.rectangulo.right - 5, self.rectangulo.top - altura_limites, 5, altura_limites)

    def _cargar_superficie(self, visible, tamaño, path):
        if visible:
            superficie = pygame.image.load(path)
            return pygame.transform.scale(superficie, tamaño)
        else:
            return pygame.Surface(tamaño)

    def dibujar(self, pantalla):
        grosor_borde = 3
        pygame.draw.rect(pantalla, "red", self.rectangulo, grosor_borde)

    def ajustar_posicion_inicial(self, nueva_altura):
        self.rectangulo.bottom = nueva_altura
        self.limite_izquierdo.rect.top = self.rectangulo.top
        self.limite_derecho.rect.top = self.rectangulo.top

    def mover_verticalmente(self):
        if self.movible:
            self.rectangulo.y += self.velocidad
            self.limite_izquierdo.rect.top = self.rectangulo.top
            self.limite_derecho.rect.top = self.rectangulo.top

            if self.velocidad > 0 and self.rectangulo.bottom >= self.rango_y[1]:
                self.velocidad *= -1
            elif self.velocidad < 0 and self.rectangulo.top <= self.rango_y[0]:
                self.velocidad *= -1

    def mover_horizontalmente(self):
        if self.movible:
            self.rectangulo.x += self.velocidad
            self.limite_izquierdo.rect.top = self.rectangulo.top
            self.limite_derecho.rect.top = self.rectangulo.top

            if self.velocidad> 0 and self.rectangulo.right >= self.rango_x[1]:
                self.velocidad*= -1
            elif self.velocidad < 0 and self.rectangulo.left <= self.rango_x[0]:
                self.velocidad*= -1

def crear_plataforma(visible, tamaño, x, y, path="",movible = False, rango_y = (0,0), rango_x=(0, 0)):
    return Plataforma(visible, tamaño, x, y, path,movible = False, rango_y = (0,0), rango_x=(0, 0))