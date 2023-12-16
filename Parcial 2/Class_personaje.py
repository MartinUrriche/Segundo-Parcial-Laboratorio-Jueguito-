from Configuraciones import *
from Class_enemigo import *
from Class_plataforma import *
from Class_proyectil import Proyectil
from Class_item import *
import pygame

class Personaje:
    def __init__(self, animaciones, velocidad, tamaño, pos_x, pos_y):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, *tamaño)

        # Rectangulos
        self.rectangulo_principal = self.animaciones["Quieto"][0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.rectangulo_pies = pygame.Rect(self.rectangulo_principal.x, self.rectangulo_principal.y, self.rectangulo_principal.width, self.rectangulo_principal.height // 6)
        self.rectangulo_pies.bottom = self.rectangulo_principal.bottom
        self.rectangulo_cabeza = pygame.Rect(self.rectangulo_principal.x, self.rectangulo_principal.y, self.rectangulo_principal.width, 5)
        self.rectangulo_brazo_derecho = pygame.Rect(self.rectangulo_principal.x + self.rectangulo_principal.width, pos_y, 5, self.rectangulo_principal.height)
        self.rectangulo_brazo_izquierdo = pygame.Rect(self.rectangulo_principal.x - 5, self.rectangulo_principal.y, 5, self.rectangulo_principal.height)

        #
        self.velocidad = velocidad
        self.que_hace = "Quieto"
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["Quieto"]
        self.ultimo_estado = "Derecha"
        # Salto
        self.desplazamiento_y = 0
        self.potencia_salto = -10
        self.limite_velocidad_salto = 10
        self.gravedad = 1
        self.esta_saltando = False
        self.en_el_aire = False
        # Disparo
        self.offset_pistola_x = 50
        self.offset_pistola_y = 15
        self.velocidad_proyectil = 10
        self.lista_proyectiles = pygame.sprite.Group()
        self.tiempo_entre_disparo = 500
        self.ultimo_disparo = pygame.time.get_ticks()
        #Usuario inactivo
        #self.tiempo_inactivo = 0
        #self.TIEMPO_AFK = 3000 
        #Puntuacion
        self.puntuacion = 0
        self.puntuacion_total = 0
        #Vidas
        self.vidas = 3

    def actualizar(self, pantalla, piso):
        self.rectangulo_pies.topleft = (self.rectangulo_principal.left, self.rectangulo_principal.bottom)
        self.rectangulo_cabeza.topleft = (self.rectangulo_principal.left, self.rectangulo_principal.top)
        self.rectangulo_brazo_derecho.topleft = (self.rectangulo_principal.right, self.rectangulo_principal.top)
        self.rectangulo_brazo_izquierdo.topleft = (self.rectangulo_principal.left - self.rectangulo_brazo_izquierdo.width, self.rectangulo_principal.top)
        match self.que_hace:
            
            case "Derecha":             
                
                if not self.esta_saltando:   
                    self.animacion_actual = self.animaciones["Derecha"]
                    self.animar(pantalla)

                self.caminar(pantalla)
                
            case "Izquierda":  
                
                if not self.esta_saltando:                                 
                    self.animacion_actual = self.animaciones["Izquierda"]
                    self.animar(pantalla)
                    
                self.caminar(pantalla)

            case "Quieto":
                self.animacion_actual = self.animaciones["Quieto"]
                self.animar(pantalla)

            case "QuietoIzquierda":
                self.animacion_actual = self.animaciones["QuietoIzquierda"]
                self.animar(pantalla)

            # case "AFK":
            #     self.animacion_actual = self.animaciones["AFK"]
            #     self.animar(pantalla)

            case "Salta":
                
                if not self.esta_saltando:                    
                    self.esta_saltando = True
                    self.desplazamiento_y = self.potencia_salto
                    self.animacion_actual = self.animaciones["Salta"]
                    self.animar(pantalla)

            case "Dispara":
                self.animacion_actual = self.animaciones["Dispara"]
                self.animar(pantalla)

            case "DisparaIzquierda":
                self.animacion_actual = self.animaciones["DisparaIzquierda"]
                self.animar(pantalla)

        self.aplicar_gravedad(pantalla, piso)
        
    def animar(self, pantalla):
        if self.en_el_aire:
            # Si está en el aire pero no está saltando, mostrar el último sprite de la animación de salto
            pantalla.blit(self.animaciones["Salta"][-1], self.rectangulo_principal)
        else:
            largo = len(self.animacion_actual)

            if largo > 0:  # Asegurémonos de que haya al menos un elemento en la lista
                if self.contador_pasos >= largo:
                    self.contador_pasos = 0

                pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
                self.contador_pasos += 1


    def caminar(self, pantalla):
        velocidad_actual = self.velocidad
        
        if self.que_hace == "Izquierda":
            velocidad_actual *= -1
            
        nueva_x = self.rectangulo_principal.x + velocidad_actual
        
        if nueva_x >= 0 and nueva_x <= pantalla.get_width() - self.rectangulo_principal.width:
            self.rectangulo_principal.x += velocidad_actual

    def aplicar_gravedad(self,pantalla, plataformas):  
        if self.esta_saltando:
            self.animar(pantalla)
            self.rectangulo_principal.y += self.desplazamiento_y - 2
            self.en_el_aire = True
            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_salto:
                self.desplazamiento_y += self.gravedad
        for top in plataformas:
            if self.rectangulo_pies.colliderect(top.rectangulo):
                self.en_el_aire = False
                pisa_plataforma = True
                if self.rectangulo_pies.bottom > top.rectangulo.top:
                    self.desplazamiento_y = 0
                    self.esta_saltando = False
                break
        else:
            self.esta_saltando = True


    def verificar_colision_enemigo(self, lista_enemigo:list["Enemigo"]):
        for enemigo in lista_enemigo:
            if self.rectangulo_principal.colliderect(enemigo.rectangulo_principal):
                self.perder_vida()

    def disparar(self, grupo_proyectiles):
        tiempo_actual = pygame.time.get_ticks()
        direccion_proyectil = 1  # 1 para derecha, -1 para izquierda
        if tiempo_actual - self.ultimo_disparo > self.tiempo_entre_disparo:
            if self.que_hace == "Dispara":
                direccion_proyectil = 1
            elif self.que_hace == "DisparaIzquierda":
                direccion_proyectil = -1
            nuevo_proyectil = Proyectil(self.rectangulo_principal.x + self.offset_pistola_x,
                                        self.rectangulo_principal.y + self.offset_pistola_y,
                                        self.velocidad_proyectil, direccion_proyectil)
            grupo_proyectiles.add(nuevo_proyectil)
            
            self.contador_pasos = 0  
            self.ultimo_disparo = tiempo_actual


    def incrementar_puntuacion(self, puntos):
        self.puntuacion += puntos
        self.puntuacion_total += puntos

    
    def incrementar_vida(self, vidas):
        self.vidas += vidas

    def recoger_item(self, item):
        item.aplicar_efecto(self)

    def perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            pass
        else:
            # Restablecer la posición inicial
            self.rectangulo_principal.x = 100  # Ajusta la posición inicial en x según tus necesidades
            self.rectangulo_principal.y = 475  # Ajusta la posición inicial en y según tus necesidades
    
    def dibujar_vidas(self, pantalla, corazon_imagen):
        x = 10
        y = 40
        for i in range(self.vidas):
            x_corazon = x + i * (corazon_imagen.get_width() + 5)
            pantalla.blit(corazon_imagen, (x_corazon, y))