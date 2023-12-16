import pygame

def manejar_eventos_personaje(personaje, grupo_proyectiles):
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_RIGHT]:
        personaje.que_hace = "Derecha"
        personaje.ultimo_estado = "Derecha"
    elif teclas[pygame.K_LEFT]:
        personaje.que_hace = "Izquierda"
        personaje.ultimo_estado = "Izquierda"
    elif teclas[pygame.K_SPACE]:
        personaje.que_hace = "Salta"
    elif teclas[pygame.K_z]:
        if personaje.ultimo_estado == "Izquierda":
            personaje.que_hace = "DisparaIzquierda"
            personaje.disparar(grupo_proyectiles)
        else:
            personaje.que_hace = "Dispara"
            personaje.disparar(grupo_proyectiles)
    else:
        if personaje.ultimo_estado == "Izquierda":
            personaje.que_hace = "QuietoIzquierda"
        else:
            personaje.que_hace = "Quieto"
            # if personaje.tiempo_inactivo > personaje.TIEMPO_AFK:
            #     personaje.que_hace = "AFK"

    # Retornar False si quieres salir del juego
    return True