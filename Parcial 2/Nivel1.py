import pygame
from Class_personaje import Personaje
from Class_proyectil import Proyectil
from Class_plataforma import Plataforma, crear_plataforma
from Class_enemigo import Enemigo
from Class_item import *
from Configuraciones import *
from Modo import *
from Manejo_de_eventos import manejar_eventos_personaje  # Importar la función de manejo de eventos

class Nivel1:
    def __init__(self, pantalla, grupo_proyectiles):
        self.pantalla = pantalla
        self.grupo_proyectiles = grupo_proyectiles

        W, H = pantalla.get_size()
        self.fondo = pygame.image.load(r"Parcial 2\fondo niveles\fondo.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (W, H))

        # Crear plataformas
        self.piso = crear_plataforma(False, (W, 10), 0, 535)
        self.plataforma_movible = crear_plataforma(True, (90, 80), 550, 460, r"Parcial 2\plataformas\1.png")
        self.plataforma_movible.ajustar_posicion_inicial(self.piso.rectangulo.top)
        self.plataforma_flotante = crear_plataforma(True, (350, 80), 100, 350, r"Parcial 2\plataformas\2.png")
        self.plataforma_flotante_x = self.plataforma_flotante.rectangulo.x
        self.plataforma_flotante_2 = crear_plataforma(True, (350, 80), 450, 200, r"Parcial 2\plataformas\2.png")
        self.plataforma_flotante_3 = crear_plataforma(True, (90, 80), 10, 200, r"Parcial 2\plataformas\1.png")
        self.plataforma_movible_horizontal = Plataforma(True,(90, 80), 100, 236, r"Parcial 2\plataformas\1.png",True,(0,0),(100,440))
        self.plataformas = [self.piso, self.plataforma_movible, self.plataforma_flotante, self.plataforma_flotante_2,
                            self.plataforma_flotante_3,self.plataforma_movible_horizontal]

        self.pausa_imagen = pygame.image.load(r"Parcial 2\img pausa\boton_pausa.png")
        self.pausa_imagen = pygame.transform.scale(self.pausa_imagen, (30, 30))
        self.rectangulo_pausa = self.pausa_imagen.get_rect(topleft=(760, 10))
        self.centro_circulo = (
            self.rectangulo_pausa.left + self.rectangulo_pausa.width // 2,
            self.rectangulo_pausa.top + self.rectangulo_pausa.height // 2
        )
        self.radio_circulo = self.rectangulo_pausa.width // 2
        self.juego_pausado = False
        self.estado_pausado = None

        self.tiempo_restante = 45  # Tiempo en segundos
        self.font_tiempo = pygame.font.Font(None, 36)
        self.color_tiempo = (255, 255, 255)

        self.corazon_imagen = pygame.image.load(r"Parcial 2\img corazones\corazon.png").convert_alpha()
        self.corazon_imagen = pygame.transform.scale(self.corazon_imagen,(57, 60))

        self.puerta_abierta = False
        self.puerta_abierta_img = puerta_abierta_img
        self.puerta_cerrada_img = puerta_cerrada_img
        self.posicion_puerta_y = (self.plataforma_flotante_2.rectangulo.top - self.puerta_abierta_img.get_height()) + 25
        self.posicion_puerta = (700, self.posicion_puerta_y)
        puerta_ancho = 100  
        puerta_alto = 160 
        self.rectangulo_puerta = pygame.Rect(self.posicion_puerta, (puerta_ancho, puerta_alto))


        


        # Crear personaje
        acciones = {}
        acciones["Quieto"] = personaje_quieto
        acciones["QuietoIzquierda"] = personaje_quieto_izquierda
        acciones["Derecha"] = personaje_camina_derecha
        acciones["Izquierda"] = personaje_camina_izquierda
        acciones["Salta"] = personaje_salta
        acciones["Dispara"] = personaje_dispara_derecha
        acciones["DisparaIzquierda"] = personaje_dispara_izquierda

        personaje = Personaje(acciones, 5, (70, 60), 100, 475)

        # Crear enemigos
        self.diccionario_animaciones = {"izquierda": [pygame.image.load(r"Parcial 2\img enemigos\ene1.png"),
                                                pygame.image.load(r"Parcial 2\img enemigos\ene2.png")],
                                "aplasta": [pygame.image.load(r"Parcial 2\img enemigos\ene3.png")]}
        un_enemigo = Enemigo(self.diccionario_animaciones, x=680 + 50)
        otro_enemigo = Enemigo(self.diccionario_animaciones, x=self.plataforma_flotante_x + 50)

        otro_enemigo.rectangulo_principal.bottom = self.plataforma_flotante.rectangulo.top
        un_enemigo.rectangulo_principal.bottom = self.piso.rectangulo.top

        d = {"aplasta": self.diccionario_animaciones["aplasta"]}
        reescalar_imagenes = (d, 50, 20)
        lista_enemigo = [un_enemigo, otro_enemigo]

        # Crear monedas
        monedas_flotante_1 = [
            Moneda(self.plataforma_flotante.rectangulo.x + 50, self.plataforma_flotante.rectangulo.top - 30, puntos=10, imagenes=moneda_img),
            Moneda(self.plataforma_flotante.rectangulo.x + 150, self.plataforma_flotante.rectangulo.top - 30, puntos=10, imagenes=moneda_img),
            ]

        monedas_flotante_2 = [
            Moneda(self.plataforma_flotante_2.rectangulo.x + 100, self.plataforma_flotante_2.rectangulo.top - 30, puntos=10, imagenes=moneda_img),
            Moneda(self.plataforma_flotante_2.rectangulo.x + 200, self.plataforma_flotante_2.rectangulo.top - 30, puntos=10, imagenes=moneda_img),
            ]

        grupo_monedas = pygame.sprite.Group(*monedas_flotante_1, *monedas_flotante_2)

        vidas_extra = [
            VidaExtra(self.plataforma_flotante_3.rectangulo.x + 20, self.plataforma_flotante_3.rectangulo.top - 20, vidas = 1 , 
                    imagenes=[pygame.transform.scale(self.corazon_imagen, (40, 30))])
            ]
        
        grupo_vidas = pygame.sprite.Group(*vidas_extra)

        self.personaje = personaje
        self.lista_enemigo = lista_enemigo
        self.grupo_monedas = grupo_monedas
        self.grupo_vidas = grupo_vidas

        self.personaje.puntuacion_nivel = 0 


    def manejar_eventos(self):
        manejar_eventos_personaje(self.personaje, self.grupo_proyectiles) 
        if self.plataforma_movible_horizontal.rectangulo.colliderect(self.personaje.rectangulo_pies):
            self.personaje.rectangulo_principal.x += self.plataforma_movible_horizontal.velocidad
            self.personaje.rectangulo_pies.x += self.plataforma_movible_horizontal.velocidad
            self.personaje.rectangulo_cabeza.x += self.plataforma_movible_horizontal.velocidad
            self.personaje.rectangulo_brazo_derecho.x += self.plataforma_movible_horizontal.velocidad
            self.personaje.rectangulo_brazo_izquierdo.x += self.plataforma_movible_horizontal.velocidad


    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.pantalla.blit(self.plataforma_movible.superficie, self.plataforma_movible.rectangulo)
        self.pantalla.blit(self.plataforma_flotante.superficie, self.plataforma_flotante.rectangulo)
        self.pantalla.blit(self.plataforma_flotante_2.superficie, self.plataforma_flotante_2.rectangulo)
        self.pantalla.blit(self.plataforma_flotante_3.superficie, self.plataforma_flotante_3.rectangulo)
        self.pantalla.blit(self.plataforma_movible_horizontal.superficie, self.plataforma_movible_horizontal.rectangulo)
        
        self.pantalla.blit(self.pausa_imagen, (750, 10))

        tiempo_redondeado = round(self.tiempo_restante)
        tiempo_texto = pygame.font.Font(None, 36).render(f"Tiempo: {tiempo_redondeado}", True, "white")
        self.pantalla.blit(tiempo_texto, (500 - 150, 10))

        
        if self.puerta_abierta:
            self.pantalla.blit(self.puerta_abierta_img, self.posicion_puerta)
        else:
            self.pantalla.blit(self.puerta_cerrada_img, self.posicion_puerta)

        for vidas in self.grupo_vidas:
            vidas.actualizar(self.pantalla)
            vidas.verificar_colision_y_eliminar(self.personaje)

        for moneda in self.grupo_monedas:
            moneda.actualizar(self.pantalla)
            moneda.verificar_colision_y_eliminar(self.personaje)

        puntuacion_texto = pygame.font.Font(None, 36).render(f"Puntuación: {self.personaje.puntuacion}", True, "white")
        self.pantalla.blit(puntuacion_texto, (10, 10)) 

        self.personaje.verificar_colision_enemigo(self.lista_enemigo)
        self.personaje.actualizar(self.pantalla, self.plataformas)
        self.personaje.dibujar_vidas(self.pantalla, self.corazon_imagen)

        self.grupo_proyectiles.update()
        self.grupo_proyectiles.draw(self.pantalla)

        for proyectil in self.grupo_proyectiles:
            proyectil.actualizar_proyectil()
            proyectil.verificar_colision_proyectil_enemigo(self.lista_enemigo, self.pantalla)

        for enemigo in self.lista_enemigo:
            enemigo.actualizar(self.pantalla)
        if obtener_modo():
            pygame.draw.rect(self.pantalla, "red", self.personaje.rectangulo_principal, 3)
            pygame.draw.rect(self.pantalla, "blue", self.personaje.rectangulo_pies.inflate(10, 10), 3)
            pygame.draw.rect(self.pantalla, "green", self.personaje.rectangulo_cabeza.inflate(10, 10), 3)
            pygame.draw.rect(self.pantalla, "orange", self.personaje.rectangulo_brazo_derecho.inflate(10, 10), 3)
            pygame.draw.rect(self.pantalla, "purple", self.personaje.rectangulo_brazo_izquierdo.inflate(10, 10), 3)
            pygame.draw.rect(self.pantalla, "purple", self.rectangulo_puerta, 3)

            for plataforma in self.plataformas:
                plataforma.dibujar(self.pantalla)

            for enemigo in self.lista_enemigo:
                pygame.draw.rect(self.pantalla, "blue", enemigo.rectangulo_principal, 3)

            for proyectil in self.grupo_proyectiles:
                pygame.draw.rect(self.pantalla, "red", proyectil, 3)

            for plataforma in self.plataformas:
                pygame.draw.rect(self.pantalla, "yellow", plataforma.limite_izquierdo.rect, 3)
                pygame.draw.rect(self.pantalla, "yellow", plataforma.limite_derecho.rect, 3)
                plataforma.dibujar(self.pantalla)

            for moneda in self.grupo_monedas:
                pygame.draw.rect(self.pantalla, "yellow", moneda.rect, 3)    

    def actualizar(self):
        if not self.juego_pausado:
            for plataforma in self.plataformas:
                for enemigo in self.lista_enemigo:
                    if enemigo.rectangulo_principal.colliderect(plataforma.limite_izquierdo.rect):
                        enemigo.cambiar_direccion()
                    elif enemigo.rectangulo_principal.colliderect(plataforma.limite_derecho.rect):
                        enemigo.cambiar_direccion()

            for i in range(len(self.lista_enemigo)):
                if self.lista_enemigo[i].esta_muerto:
                    self.lista_enemigo[i].eliminar()
                    del self.lista_enemigo[i]
                    break
            self.plataforma_movible_horizontal.mover_horizontalmente()

    def decrementar_tiempo(self, tiempo_transcurrido):
        if not self.juego_pausado:
            self.tiempo_restante -= tiempo_transcurrido
            if self.tiempo_restante < 0:
                self.tiempo_restante = 0

    def pausar_juego(self):
        self.juego_pausado = True
        self.estado_pausado = {
            'enemigos': [(enemigo.rectangulo_principal.x, enemigo.rectangulo_principal.y) for enemigo in self.lista_enemigo],
            'tiempo_restante': self.tiempo_restante,
            'posicion_personaje': (self.personaje.rectangulo_principal.x, self.personaje.rectangulo_principal.y)
            }

    def reanudar_juego(self):
        if self.estado_pausado is None:
            return

        self.juego_pausado = False
        self.lista_enemigo = [Enemigo(self.diccionario_animaciones, x=x, y=y) for x, y in self.estado_pausado.get('enemigos', [])]
        self.tiempo_restante = self.estado_pausado.get('tiempo_restante', 0)
        posicion_personaje = self.estado_pausado.get('posicion_personaje', (0, 0))
        self.personaje.rectangulo_principal.x, self.personaje.rectangulo_principal.y = posicion_personaje

    def pasar_nivel(self):
        if len(self.lista_enemigo) == 0:
            self.puerta_abierta = True
            self.personaje.puntuacion_total += self.personaje.puntuacion_nivel  # Sumar puntuación del nivel actual
            self.personaje.puntuacion_nivel = 0