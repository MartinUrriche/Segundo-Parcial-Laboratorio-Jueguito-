import pygame
from pygame.locals import *
import sys

BLANCO = (255, 255, 255)

class OpcionMenu:
    def __init__(self, texto, posicion):
        self.texto = texto
        self.fuente = pygame.font.Font(None, 36)
        self.superficie_texto = self.fuente.render(texto, True, "black")
        self.rect = self.superficie_texto.get_rect(center=posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.superficie_texto, self.rect)

class Menu:
    def __init__(self, opciones, resolucion_pantalla):
        self.opciones = opciones
        self.resolucion_pantalla = resolucion_pantalla

    def __iter__(self):
        return iter(self.opciones)
    
    def mostrar(self, pantalla):
        pantalla.fill(BLANCO)

        fondo = pygame.image.load(r"Parcial 2\img_menus/fondo_menu_principal.png").convert()
        fondo = pygame.transform.scale(fondo, self.resolucion_pantalla)
        pantalla.blit(fondo, (0, 0))

        for opcion in self.opciones:
            opcion.dibujar(pantalla)
    
        pygame.display.flip()
class MenuNiveles(Menu):
    def __init__(self, opciones, resolucion_pantalla, cantidad_niveles, tamaño_boton=50):
        super().__init__(opciones, resolucion_pantalla)
        self.cantidad_niveles = cantidad_niveles
        self.tamaño_boton = tamaño_boton

    def mostrar(self, pantalla):
        super().mostrar(pantalla)

        # Dibujar rectángulos para los niveles
        for i in range(self.cantidad_niveles):
            rectangulo = pygame.Rect(150 * i + 200, 200, self.tamaño_boton, self.tamaño_boton)
            pygame.draw.rect(pantalla, (0,0,0), rectangulo, 2)

            # Dibujar el número del nivel
            fuente = pygame.font.Font(None, 24)
            superficie_texto = fuente.render(f"N-{i + 1 }", True,  (0,0,0))
            rect_texto = superficie_texto.get_rect(center=rectangulo.center)
            pantalla.blit(superficie_texto, rect_texto)

    def manejar_evento_clic(self, evento):
        if evento.button == 1:  
            for i, rectangulo in enumerate(self.obtener_rectangulos()):
                if rectangulo.collidepoint(evento.pos):
                    return i + 1  
                
    def obtener_rectangulos(self):
        rectangulos = []

        for i in range(self.cantidad_niveles):
            rectangulo = pygame.Rect(150 * i + 200, 200, self.tamaño_boton, self.tamaño_boton)
            rectangulos.append(rectangulo)

        return rectangulos
    
class MenuPausa(Menu):
    def __init__(self, resolucion_pantalla):
        opciones = [
            OpcionMenu("Continuar", (resolucion_pantalla[0] // 2, 200)),
            OpcionMenu("Salir al Menú Principal", (resolucion_pantalla[0] // 2, 300)),
        ]
        super().__init__(opciones, resolucion_pantalla)
        self.opcion_seleccionada = None

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    for opcion in self:
                        if opcion.rect.collidepoint(evento.pos):
                            return opcion.texto
        return None

    def mostrar(self, pantalla):
        super().mostrar(pantalla)
        pygame.display.update()