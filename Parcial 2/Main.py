import pygame
import threading
import sys
from Scoreboard import *
from Class_menu import *
from Modo import *
from Manejo_de_eventos import *
from Class_musica import *
from Nivel1 import Nivel1
from Nivel2 import Nivel2
from Nivel3 import Nivel3


pygame.init()

W, H = 800, 600
FPS = 18

try:
    RELOJ = pygame.time.Clock()
except pygame.error as e:
    print(f"Error al crear el reloj: {e}")
    sys.exit()

RELOJ.tick(FPS)
tiempo_transcurrido = RELOJ.get_time() / 1000

try:
    PANTALLA = pygame.display.set_mode((W, H))
except pygame.error as e:
    print(f"Error al crear la pantalla: {e}")
    sys.exit()

try:
    font = pygame.font.Font(None, 36)
except pygame.error as e:
    print(f"Error al crear la fuente: {e}")
    sys.exit()

try:
    inicializar_base_de_datos()
except sqlite3.Error as e:
    print(f"Error al inicializar la base de datos: {e}")
    sys.exit()

def mostrar_game_over():
    try:
        game_over_imagen = pygame.image.load(r"Parcial 2\img game over\game over.png").convert_alpha()
        game_over_imagen = pygame.transform.scale(game_over_imagen, (W, H))
        PANTALLA.blit(game_over_imagen, (0, 0))
        pygame.display.flip()

        pygame.time.delay(3000)
    except pygame.error as e:
        print(f"Error al cargar la imagen de Game Over: {e}")

def mostrar_pantalla_felicitaciones(RELOJ = RELOJ,pantalla = (W,H)):
    try:
        pantalla_felicitaciones = pygame.display.set_mode(pantalla)

        # Fondo de pantalla para la pantalla de felicitaciones
        fondo_felicitaciones = pygame.image.load(r"Parcial 2\img felicitaciones\good end.png").convert_alpha()
        fondo_felicitaciones = pygame.transform.scale(fondo_felicitaciones, (pantalla))

        tiempo_mostrado = 0
        tiempo_maximo_mostrado = 4000  # 5000 milisegundos (5 segundos)

        while tiempo_mostrado < tiempo_maximo_mostrado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pantalla_felicitaciones.blit(fondo_felicitaciones, (0, 0))
            pygame.display.flip()

            tiempo_mostrado += RELOJ.tick(30)
    except pygame.error as e:
        print(f"Error al cargar la imagen de felicitaciones: {e}")


def input_siglas(clock, font):
    try:
        input_box = pygame.Rect(100, 100, 140, 32)
        color_inactivo = pygame.Color('red')
        color = color_inactivo
        click = False
        texto = ''
        texto_surface = font.render('Ingresa su AKA: ', True, "white")
        width = max(200, texto_surface.get_width() + 10)
        input_box.w = width

        fondo_menu = pygame.image.load(r"Parcial 2\img_menus\fondo_menu_principal.png").convert_alpha()
        fondo_menu = pygame.transform.scale(fondo_menu, (W, H))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = input_box.collidepoint(event.pos)
                if event.type == pygame.KEYDOWN and click:
                    if event.key == pygame.K_RETURN:
                        return texto
                    elif event.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        texto += event.unicode
                    texto_surface = font.render('Ingresa tus siglas(Solo 3 letras): ' + texto, True, "white")
                    input_box.w = max(200, texto_surface.get_width() + 10)

            PANTALLA.blit(fondo_menu, (0, 0))
            pygame.draw.rect(PANTALLA, color, input_box, 2)
            PANTALLA.blit(texto_surface, (input_box.x + 5, input_box.y + 5))
            pygame.display.flip()
            clock.tick(30)
    except pygame.error as e:
        print(f"Error en la entrada de siglas: {e}")


try:
    reproductor_musica = ReproductorMusica("Parcial 2/musica/03 Main Theme from Metal Slug (Stage 1).mp3")
except pygame.error as e:
    print(f"Error al crear el reproductor de música: {e}")
    sys.exit()

grupo_proyectiles = pygame.sprite.Group()

menu_principal = Menu([
    OpcionMenu("Niveles", (W // 2, 200)),
    OpcionMenu("Configuraciones", (W // 2, 300)),
    OpcionMenu("Scoreboard", (W // 2, 400))
],(W, H))

menu_pausa = MenuPausa((W,H))

menu_niveles = MenuNiveles([], (W, H), 3, tamaño_boton=80)

bandera = True

puntuacion_global = 0


menu_principal_activo = True
menu_niveles_activo = True
menu_pausa_activo = True

while bandera:
    RELOJ.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            bandera = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
        elif evento.type == MOUSEBUTTONDOWN:
            if evento.button == 1:
                if menu_principal_activo:
                    for opcion in menu_principal:
                        if opcion.rect.collidepoint(evento.pos):
                            if opcion.texto == "Niveles":
                                menu_principal_activo = False
                            elif opcion.texto == "Scoreboard":
                                menu_principal_activo = False
                                mostrar_scoreboard()

                elif menu_niveles_activo:
                    numero_nivel = menu_niveles.manejar_evento_clic(evento)
                    if numero_nivel is not None:
                        print(f"Iniciando Nivel {numero_nivel}")
                        if numero_nivel == 1:
                            menu_niveles_activo = False
                            nivel_actual = Nivel1(PANTALLA, grupo_proyectiles)
                        elif numero_nivel == 2:
                            menu_niveles_activo = False
                            nivel_actual = Nivel2(PANTALLA, grupo_proyectiles)
                        elif numero_nivel == 3:
                            menu_niveles_activo = False
                            nivel_actual = Nivel3(PANTALLA,grupo_proyectiles)

                elif nivel_actual is not None:
                    if not reproductor_musica.reproduciendo:
                        threading.Thread(target=reproductor_musica.iniciar_musica).start()
                    clic_x, clic_y = evento.pos
                    distancia = ((clic_x - nivel_actual.centro_circulo[0]) ** 2 + (clic_y - nivel_actual.centro_circulo[1]) ** 2) ** 0.5
                    if distancia <= nivel_actual.radio_circulo:
                        nivel_actual.juego_pausado = True
                        nivel_actual.pausar_juego()
                        reproductor_musica.pausar_musica()
                        menu_pausa_activo = True
                        menu_pausa.mostrar(PANTALLA)
                    else:
                        reproductor_musica.reanudar_musica()
                        nivel_actual.reanudar_juego()

    
    if menu_principal_activo:
        menu_principal.mostrar(PANTALLA)
    elif menu_niveles_activo:
        menu_niveles.mostrar(PANTALLA)
    elif nivel_actual is not None and not nivel_actual.juego_pausado:
        nivel_actual.dibujar()
        nivel_actual.actualizar()
        nivel_actual.manejar_eventos()
        nivel_actual.decrementar_tiempo(tiempo_transcurrido)
        nivel_actual.pasar_nivel()
        puntuacion_global += nivel_actual.personaje.puntuacion_total
        if nivel_actual.personaje.vidas <= 0 or nivel_actual.tiempo_restante <= 0:
            nivel_actual = None
            mostrar_game_over()
            siglas = input_siglas(RELOJ, font)
            actualizar_puntaje(siglas, puntuacion_global)
            print("AKA ingresado:", siglas)
            pygame.time.delay(2000)
            menu_principal_activo = True
        if nivel_actual.puerta_abierta and nivel_actual.personaje.rectangulo_principal.colliderect(nivel_actual.rectangulo_puerta):
            if isinstance(nivel_actual, Nivel1):
                nivel_actual = Nivel2(PANTALLA, grupo_proyectiles)
            elif isinstance(nivel_actual, Nivel2):
                nivel_actual = Nivel3(PANTALLA, grupo_proyectiles)
            elif isinstance(nivel_actual, Nivel3):
                nivel_actual = None
                mostrar_pantalla_felicitaciones()
                siglas = input_siglas(RELOJ, font)
                actualizar_puntaje(siglas, puntuacion_global)
                print("AKA ingresado:", siglas)
                pygame.time.delay(2000)
                menu_principal_activo = True



    pygame.display.update()

pygame.quit()