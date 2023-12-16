from Configuraciones import *

class Enemigo:
    def __init__(self, animaciones, x=0, y=0) -> None:
        """
        Brief: Constructor de la clase Enemigo.

        Parameters:
            - animaciones (dict): Un diccionario que contiene las animaciones del enemigo para diferentes direcciones.
            - x (int): La posición horizontal inicial del enemigo en la pantalla (por defecto, 0).
            - y (int): La posición vertical inicial del enemigo en la pantalla (por defecto, 0).
        """
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, 50,50)
        self.rectangulo_principal = self.animaciones['izquierda'][0].get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y

        self.esta_muerto = False
        self.pasos = 0
        self.animacion_actual = self.animaciones['izquierda']
        self.muriendo = False
        self.direccion = "izquierda"

    def avanzar(self):
        """
        Brief: Avanza la posición del enemigo en la dirección actual.

        """
        if self.direccion == "izquierda":
            self.rectangulo_principal.x -= 5
        else:
            self.rectangulo_principal.x += 5

    def animar(self, pantalla):
        """
        Brief: Realiza la animación del enemigo en la pantalla.

        Parameters:
            - pantalla (Surface): La superficie de la pantalla donde se realiza la animación.

        """
        largo = len(self.animacion_actual)
        
        if self.pasos >= largo:
            self.pasos = 0

        pantalla.blit(self.animacion_actual[self.pasos], self.rectangulo_principal)
        self.pasos += 1

        if self.muriendo and self.pasos == largo:
            self.esta_muerto = True

    def cambiar_direccion(self):
        """
        Brief: Cambia la dirección del enemigo entre izquierda y derecha.
        """
        if self.direccion == "izquierda":
            self.direccion = "derecha"
        else:
            self.direccion = "izquierda"

    def actualizar(self, pantalla):
        """
        Brief: Actualiza el estado del enemigo en la pantalla.

        Parameters:
            - pantalla (Surface): La superficie de la pantalla donde se actualiza el enemigo.

        """
        if self.esta_muerto == False:
            self.animar(pantalla)
            self.avanzar()
    
    def eliminar(self):
        """
        Brief: Elimina los atributos principales del objeto Enemigo.

        """
        del self.rectangulo_principal
        del self.animaciones
        del self.esta_muerto
        del self.pasos
        del self.animacion_actual
        del self.muriendo
        del self 

