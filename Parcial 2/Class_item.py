import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, puntos=10, vidas = 1, imagenes=None):
        super().__init__()
        self.imagenes = imagenes
        self.indice_imagen = 0
        self.image = self.imagenes[self.indice_imagen].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.puntos = puntos
        self.vidas = vidas

    def ajustar_posicion_inicial(self, nueva_altura):
        self.rect.bottom = nueva_altura

    def actualizar(self, pantalla):
        self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
        self.image = self.imagenes[self.indice_imagen].convert_alpha()
        pantalla.blit(self.image, self.rect)

    def verificar_colision_y_eliminar(self, jugador):
        if self.rect.colliderect(jugador.rectangulo_principal):
            jugador.recoger_item(self)
            self.kill()

    def aplicar_efecto(self, jugador):
        pass  # Cada tipo de item puede tener su propia lógica de efecto


class Moneda(Item):
    def aplicar_efecto(self, jugador):
        jugador.incrementar_puntuacion(self.puntos)


class VidaExtra(Item):
    def aplicar_efecto(self, jugador):
        jugador.incrementar_vida(self.vidas)
