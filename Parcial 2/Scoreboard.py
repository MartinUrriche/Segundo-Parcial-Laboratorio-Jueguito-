import sqlite3
import pygame

def inicializar_base_de_datos():
    conexion = sqlite3.connect("puntajes.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puntajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iniciales TEXT,
            puntaje INTEGER
        )
    """)

    conexion.commit()  
    conexion.close()

def actualizar_puntaje(iniciales, puntaje):
    conexion = sqlite3.connect("puntajes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM puntajes WHERE iniciales = ?", (iniciales,))
    jugador_existente = cursor.fetchone()

    if jugador_existente:
        if puntaje > jugador_existente[2]:
            cursor.execute("UPDATE puntajes SET puntaje = ? WHERE iniciales = ?", (puntaje, iniciales))
    else:
        # Si no existe, inserta un nuevo registro
        cursor.execute("INSERT INTO puntajes (iniciales, puntaje) VALUES (?, ?)", (iniciales, puntaje))

    conexion.commit()  
    conexion.close()

def obtener_puntajes():
    conexion = sqlite3.connect("puntajes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT iniciales, puntaje FROM puntajes ORDER BY puntaje DESC")
    puntajes = cursor.fetchall()
    conexion.close()
    return puntajes
def mostrar_scoreboard():
    pantalla_scoreboard = pygame.display.set_mode((800, 600))
    clock_scoreboard = pygame.time.Clock()

    fondo_scoreboard = pygame.image.load(r"Parcial 2\img_menus\fondo_menu_principal.png").convert_alpha()
    fondo_scoreboard = pygame.transform.scale(fondo_scoreboard, (800, 600))

    conexion = sqlite3.connect("puntajes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT iniciales, puntaje FROM puntajes ORDER BY puntaje DESC")
    scoreboard = cursor.fetchall()
    conexion.close()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        pantalla_scoreboard.blit(fondo_scoreboard, (0, 0))

        # Dibujar encabezado
        font_encabezado = pygame.font.Font(None, 36)
        encabezado_surface = font_encabezado.render("Siglas:    Puntuación:", True, "red")
        pantalla_scoreboard.blit(encabezado_surface, (50, 50))

        # Dibujar datos del scoreboard
        font_score = pygame.font.Font(None, 28)
        y = 100
        for siglas, puntaje in scoreboard:
            datos_surface = font_score.render(f"{siglas}         {puntaje}", True, "red")
            pantalla_scoreboard.blit(datos_surface, (50, y))
            y += 30

        pygame.display.flip()
        clock_scoreboard.tick(30)