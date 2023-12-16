import pygame

def girar_imagenes(lista_original, flip_x, flip_y):
    lista_girada = []
    
    for imagen in lista_original:
        lista_girada.append(pygame.transform.flip(imagen, flip_x, flip_y))
        
    return lista_girada

def reescalar_imagenes(diccionario_animaciones, ancho, alto):
    
    for clave in diccionario_animaciones:

        for i in range(len(diccionario_animaciones[clave])):
            img = diccionario_animaciones[clave][i]
            diccionario_animaciones[clave][i] = pygame.transform.scale(img, (ancho, alto))
            
#constructor de una clase
personaje_quieto = [pygame.image.load(r"Parcial 2\Quieto\0.png")]
personaje_quieto_izquierda = girar_imagenes(personaje_quieto, True, False)
personaje_afk = [pygame.image.load(r"Parcial 2\Quieto\1.png"),
                    pygame.image.load(r"Parcial 2\Quieto\2.png"),
                    pygame.image.load(r"Parcial 2\Quieto\3.png"),
                    pygame.image.load(r"Parcial 2\Quieto\4.png"),
                    pygame.image.load(r"Parcial 2\Quieto\5.png"),
                    pygame.image.load(r"Parcial 2\Quieto\6.png"),
                    pygame.image.load(r"Parcial 2\Quieto\7.png"),
                    pygame.image.load(r"Parcial 2\Quieto\8.png"),
                    pygame.image.load(r"Parcial 2\Quieto\9.png")]
personaje_camina_derecha = [pygame.image.load(r"Parcial 2\Quieto\1.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\2.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\2.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\3.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\4.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\5.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\6.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\7.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\8.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\9.png"),
                            pygame.image.load(r"Parcial 2\img moviendose\10.png"),]
personaje_camina_izquierda = girar_imagenes(personaje_camina_derecha, True, False)
personaje_salta = [pygame.image.load(r"Parcial 2\img saltando\01.png"),
                pygame.image.load(r"Parcial 2\img saltando\02.png"),
                pygame.image.load(r"Parcial 2\img saltando\03.png"),
                pygame.image.load(r"Parcial 2\img saltando\04.png"),
                pygame.image.load(r"Parcial 2\img saltando\05.png"),
                pygame.image.load(r"Parcial 2\img saltando\06.png")]
personaje_dispara_derecha = [pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\0c.png"),
                            pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\1c.png"),
                            pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\2c.png"),
                            pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\3c.png"),
                            pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\4c.png"),
                            pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\5c.png"),
                            pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\6c.png"),
                            pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\7c.png")]
personaje_proyectil = pygame.image.load(r"Parcial 2\img disparando\disparo_derecha\Proyectil parado derecha.png")
personaje_dispara_izquierda = girar_imagenes(personaje_dispara_derecha, True, False)

enemigo_camina = [pygame.image.load(r"Parcial 2\img enemigos\ene1.png"),
                            pygame.image.load(r"Parcial 2\img enemigos\ene2.png")]

enemigo_aplasta = [pygame.image.load(r"Parcial 2\img enemigos\ene3.png")]

moneda_img = [pygame.image.load(r"Parcial 2\img moneda\0.png"),
        pygame.image.load(r"Parcial 2\img moneda\1.png"),
        pygame.image.load(r"Parcial 2\img moneda\2.png"),
        pygame.image.load(r"Parcial 2\img moneda\3.png"),]

corazon_img = [pygame.image.load(r"Parcial 2\img corazones\corazon.png")]

pausa_img = pygame.image.load(r"Parcial 2\img pausa\boton_pausa.png")

puerta_abierta_img = pygame.image.load(r"Parcial 2\img puerta\puerta abierta.png")
puerta_cerrada_img = pygame.image.load(r"Parcial 2\img puerta\puerta cerrada.png")